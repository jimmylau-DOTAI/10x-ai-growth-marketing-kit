#!/usr/bin/env python3
"""Read-only delivery gate: exact image size and version-bound local QA evidence.
The gate cannot independently establish model behavior, human judgment or provenance.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

SKILL_FILE = Path(__file__).resolve().parents[1] / 'SKILL.md'


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def local_file(root, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('local relative file path required')
    relative = Path(value)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('file must be inside the job folder')
    target = root / relative
    if any(p.is_symlink() for p in [target, *target.parents] if p != root and root in p.parents):
        raise ValueError('symlink not allowed')
    target.resolve().relative_to(root.resolve())
    if not target.is_file():
        raise ValueError('file missing: ' + value)
    return target


def evidence(root, value):
    target = local_file(root, value)
    text = target.read_text(encoding='utf-8').strip()
    if text.casefold() in {'', 'pass', 'ok', 'tbc', 'todo', 'pending'}:
        raise ValueError('evidence must describe the actual check or tool result')
    return target


def image_info(root, value):
    path = local_file(root, value)
    with Image.open(path) as im:
        im.verify()
    with Image.open(path) as im:
        im.load()
        dimensions = list(im.size)
        orientation = im.getexif().get(274, 1)
    return {'file': value, 'dimensions': dimensions, 'sha256': sha256(path), 'exif_orientation': orientation}


def verify_request(request_path):
    """Validate a pre-generation size decision; evidence truth remains owner-reviewed."""
    request_path = Path(request_path).resolve()
    errors = []
    target = None
    try:
        request = json.loads(request_path.read_text(encoding='utf-8'))
        if not isinstance(request, dict):
            raise ValueError('request must be an object')
    except (OSError, ValueError) as exc:
        request = {}
        errors.append(str(exc))
    if request.get('schema_version') != 1:
        errors.append('request schema_version must be 1')
    for field in ('platform', 'placement'):
        value = request.get(field)
        if not isinstance(value, str) or value.strip().casefold() in {'', 'tbc', 'unknown', 'pending'}:
            errors.append('ask for ' + field + ' or record an explicit custom-size request')
    dims = [request.get('width'), request.get('height')]
    if all(type(v) is int and v > 0 for v in dims):
        target = dims
    else:
        errors.append('ask for positive integer pixel width and height')
    ratio = request.get('aspect_ratio')
    if ratio is not None:
        if not isinstance(ratio, list) or len(ratio) != 2 or not all(type(v) is int and v > 0 for v in ratio):
            errors.append('aspect_ratio must be two positive integers')
        elif target and target[0] * ratio[1] != target[1] * ratio[0]:
            errors.append('pixel size conflicts with aspect_ratio; ask before generation')
    if request.get('basis') not in {'user_explicit', 'project_brief', 'user_confirmed_recommendation', 'delegated_choice'}:
        errors.append('size choice not resolved; ask user to confirm the proposed size')
    try:
        evidence(request_path.parent, request.get('evidence'))
    except (OSError, ValueError) as exc:
        errors.append('size source: ' + str(exc))
    return {'ok': not errors, 'status': 'ASK_USER' if errors else 'REQUEST_READY',
            'target': target, 'errors': errors,
            'notes': ['Request completeness only; not tool capability, proof of user approval, or permission to publish.']}


def verify(receipt_path):
    receipt_path = Path(receipt_path).resolve()
    root = receipt_path.parent
    errors = []
    actual = None
    target = None
    try:
        record = json.loads(receipt_path.read_text(encoding='utf-8'))
        if not isinstance(record, dict):
            raise ValueError('receipt must be an object')
    except (OSError, ValueError) as exc:
        record = {}
        errors.append(str(exc))
    if record.get('schema_version') != 2:
        errors.append('delivery schema_version must be 2; attach the pre-generation request')
    skill = record.get('skill', {})
    if not isinstance(skill, dict):
        skill = {}
    if skill.get('name') != 'brand-image-studio':
        errors.append('actual production Skill must be brand-image-studio')
    if skill.get('sha256') != sha256(SKILL_FILE):
        errors.append('Skill version missing or stale; read the current SKILL.md and recheck')
    requested = record.get('target', {})
    if isinstance(requested, dict):
        dims = [requested.get('width'), requested.get('height')]
        if all(type(v) is int and v > 0 for v in dims):
            target = dims
    if target is None:
        errors.append('explicit positive integer target width and height required')
    try:
        request_file = local_file(root, record.get('request_file'))
        request_result = verify_request(request_file)
        if not request_result['ok']:
            errors.extend('request: ' + error for error in request_result['errors'])
        if record.get('request_sha256') != sha256(request_file):
            errors.append('request hash missing or mismatched; target decision changed')
        if target != request_result['target']:
            errors.append('delivery target differs from the pre-generation request')
    except (OSError, ValueError) as exc:
        errors.append('request: ' + str(exc))
    operation = record.get('operation')
    if operation not in {'create', 'edit', 'add-logo', 'resize', 'recompose'}:
        errors.append('unsupported or missing operation')
    tool = record.get('tool', {})
    if not isinstance(tool, dict):
        tool = {}
    if not isinstance(tool.get('name'), str) or tool['name'].strip().casefold() in {'', 'tbc', 'todo'}:
        errors.append('actual tool name required')
    expected_mode = {'create': 'native-generate', 'edit': 'native-edit', 'add-logo': 'native-edit', 'recompose': 'native-recompose', 'resize': 'proportional-resize'}.get(operation)
    if tool.get('mode') != expected_mode or expected_mode is None:
        errors.append('tool mode must match the requested operation')
    if not isinstance(tool.get('parameters'), dict):
        errors.append('actual tool parameters must be recorded as an object; use empty object when none are exposed')
    if tool.get('size_control') not in {'structured', 'prompt_only'}:
        errors.append('working tool and size_control evidence required')
    for label, value in [('tool contract', tool.get('evidence')), ('generation evidence', record.get('generation_evidence'))]:
        try:
            evidence(root, value)
        except (OSError, ValueError) as exc:
            errors.append(f'{label}: {exc}')
    try:
        actual = image_info(root, record.get('output_image'))
        if target and actual['dimensions'] != target:
            errors.append(f"size mismatch: expected {target}, actual {actual['dimensions']}")
        if actual['exif_orientation'] != 1:
            errors.append('output has EXIF rotation; normalize through an allowed tool and recheck')
        if record.get('output_sha256') != actual['sha256']:
            errors.append('output hash mismatch or missing; output changed since receipt')
    except (OSError, ValueError, Image.DecompressionBombError) as exc:
        errors.append('output image: ' + str(exc))
    if operation in {'edit', 'add-logo', 'resize', 'recompose'}:
        try:
            original = image_info(root, record.get('input_image'))
            if record.get('input_sha256') != original['sha256']:
                errors.append('input hash missing or mismatched')
            if operation == 'resize' and actual:
                iw, ih = original['dimensions']
                ow, oh = actual['dimensions']
                if iw * oh != ih * ow:
                    errors.append('resize changed aspect ratio; stretch/crop cannot pass as proportional resize')
        except (OSError, ValueError, Image.DecompressionBombError) as exc:
            errors.append('input image: ' + str(exc))
    reviews = record.get('reviews', {})
    if not isinstance(reviews, dict):
        reviews = {}
    for kind in ('text', 'visual'):
        review = reviews.get(kind, {})
        if not isinstance(review, dict):
            review = {}
        if review.get('status') != 'pass':
            errors.append(kind + ' review is missing, pending or failed')
        if not actual or review.get('image_sha256') != actual['sha256']:
            errors.append(kind + ' review does not match the current output hash')
        try:
            evidence(root, review.get('evidence'))
        except (OSError, ValueError) as exc:
            errors.append(kind + ' review evidence: ' + str(exc))
    return {
        'ok': not errors,
        'status': 'DELIVERY_BLOCKED' if errors else 'LOCAL_QA_PASSED_REVIEW_REQUIRED',
        'target': target,
        'actual_output': actual,
        'errors': errors,
        'notes': [
            'Exact file/size/hash and presence of review records checked; evidence truth and taste require actual inspection.',
            'Skill hash identifies a version, not proof that the model followed it.',
            'No human approval, publication, or actual tool-call provenance is established by this gate alone.'
        ]
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('receipt', type=Path)
    p.add_argument('--output', type=Path)
    p.add_argument('--preflight', action='store_true', help='Check a request.json before any generation; no image is needed')
    a = p.parse_args()
    if a.output and a.output.exists():
        p.error('output exists; choose a new validation receipt path')
    result = verify_request(a.receipt) if a.preflight else verify(a.receipt)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(rendered, encoding='utf-8')
    print(rendered)
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
