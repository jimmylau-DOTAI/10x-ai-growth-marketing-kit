#!/usr/bin/env python3
"""Export an ordered, file-based handoff; never generate or approve images."""
import argparse,json,re,subprocess,sys
from pathlib import Path

def export(root,output,draft=False):
    root=root.resolve();output=output.resolve()
    text=(root/'content-plan.md').read_text(encoding='utf-8')
    approved=bool(re.search(r'(?m)^Status:\s*`?CAROUSEL_PLAN_APPROVED`?\s*$',text))
    if not draft and not approved:raise ValueError('complete plan approval is required; --draft exports review material only')
    check=subprocess.run([sys.executable,str(Path(__file__).with_name('validate_project.py')),'--project-dir',str(root),'--strict'],capture_output=True,text=True)
    if check.returncode:raise ValueError(check.stdout)
    rows=[]
    for line in text.splitlines():
        if re.match(r'^\|\s*\d{1,2}\s*\|',line):
            cells=[c.strip() for c in line.strip('|').split('|')]
            if len(cells)!=6 or any(not c or c in {'TBC','TODO','—','-'} for c in cells):raise ValueError('incomplete card row')
            rows.append(cells)
    if output.exists():raise ValueError('output already exists; choose a new version')
    preferences=(root/'PREFERENCES.md').read_text(encoding='utf-8')
    jobs=[]
    for cells in rows:
        number,role,lead,body,visual,handoff=cells;cid=f'C{int(number):02d}'
        job={'schema_version':1,'id':cid,'status':'DRAFT' if draft else 'CONTENT_REVIEW_RECORDED','dimensions':[1080,1350],'role':role,'visible_copy':{'lead':lead,'body':body},'visual_direction':visual,'source_note':handoff,'preferences':preferences,'render_route':'ai-social-image-maker owns the complete image: generate all visible copy natively using the selected Style references; use the built-in image tool by default or the user-requested available API. Preserve requested Logo intent: choose a clean low-detail corner among all four, record its box, and place the supplied original Logo when requested. Verify the final 1080x1350 canvas; a Logo-pending native preview is not a finished branded card.','approval_note':'Demo/review export; no human approval inferred.' if draft else 'Plan records approval; consuming agent must check actual user approval and version.','publish':False}
        folder=output/cid;folder.mkdir(parents=True)
        (folder/'job.json').write_text(json.dumps(job,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (folder/'CONTENT-JOB.md').write_text(f'# {cid} Image handoff\n\nStatus: {job["status"]}\nDimensions: 1080x1350\n\n## Visible copy\n\n{lead}\n\n{body}\n\n## Visual direction\n\n{visual}\n\n## Source and claim boundary\n\n{handoff}\n\n## Render route\n\n{job["render_route"]}\n\n## Style / Design\n\n{preferences}\n\n## Approval\n\n{job["approval_note"]}\n\nC01 review is required before producing the remaining images. Never publish automatically.\n',encoding='utf-8')
        jobs.append(f'{cid}/CONTENT-JOB.md')
    (output/'manifest.json').write_text(json.dumps({'schema_version':1,'jobs':jobs,'status':'DRAFT' if draft else 'CONTENT_REVIEW_RECORDED','note':'CONTENT-JOB is the downstream creative handoff; legacy validate_pilot_job applies only to optional completed pilot receipts.'},indent=2)+'\n')
    return jobs

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--draft',action='store_true');a=p.parse_args()
    try:print(json.dumps({'ok':True,'jobs':export(a.project_dir,a.output,a.draft)}));return 0
    except (OSError,ValueError) as e:print(json.dumps({'ok':False,'errors':[str(e)]}));return 1
if __name__=='__main__':raise SystemExit(main())
