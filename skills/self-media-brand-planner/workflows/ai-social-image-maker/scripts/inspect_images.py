#!/usr/bin/env python3
"""Read actual image files and optionally check requested dimensions; no image edits."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageOps

def inspect(paths,expected=None):
    images=[];errors=[]
    for path in paths:
        path=Path(path)
        try:
            with Image.open(path) as im:
                im.verify()
            with Image.open(path) as im:
                im.load();fmt=im.format;size=list(ImageOps.exif_transpose(im).size)
            entry={'file':path.name,'format':fmt,'dimensions':size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
            if expected and size!=list(expected):errors.append(f'{path.name}: expected {list(expected)}, actual {size}')
            images.append(entry)
        except (OSError,ValueError) as e:errors.append(f'{path.name}: {e}')
    return {'ok':not errors,'scope':'exact-size-check' if expected else 'metadata-only','target_checked':expected is not None,'delivery_ready':False,'images':images,'errors':errors,'note':'File/size validation only. Does not prove generation provenance, Style fidelity, correct text, human approval, or publication.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('images',type=Path,nargs='+');mode=p.add_mutually_exclusive_group(required=True);mode.add_argument('--expected',nargs=2,type=int,metavar=('WIDTH','HEIGHT'));mode.add_argument('--metadata-only',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args()
    if a.expected and min(a.expected)<=0:p.error('expected dimensions must be positive')
    result=inspect(a.images,a.expected);text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if a.output:
        if a.output.exists():p.error('output exists; use a new receipt path')
        a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text,encoding='utf-8')
    print(text);return 0 if result['ok'] else 1
if __name__=='__main__':raise SystemExit(main())
