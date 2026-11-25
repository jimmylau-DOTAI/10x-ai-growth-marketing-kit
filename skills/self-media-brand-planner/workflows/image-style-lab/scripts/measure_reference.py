#!/usr/bin/env python3
"""Measure user/vision-selected raster regions; does not infer semantic layers or fonts."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageOps


def measure(path, regions):
    with Image.open(path) as source:
        image=ImageOps.exif_transpose(source).convert('RGB')
    w,h=image.size;result=[]
    for region in regions:
        box=region.get('box')
        if not isinstance(box,list) or len(box)!=4 or any(type(v)!=int for v in box):
            raise ValueError('box must contain integer x,y,width,height')
        x,y,bw,bh=box
        if min(x,y)<0 or min(bw,bh)<=0 or x+bw>w or y+bh>h:raise ValueError('region outside image')
        crop=image.crop((x,y,x+bw,y+bh));counts=Counter(crop.getdata())
        top=counts.most_common(5)
        result.append({'id':region.get('id'),'box_px':box,'box_pct':[round(v/d*100,3) for v,d in zip(box,[w,h,w,h])], 'exact_pixel_colours':[{'hex':'#%02X%02X%02X'%rgb,'coverage':n/(bw*bh)} for rgb,n in top], 'dominant_colour_is_flat':top[0][1]/(bw*bh)>0.5})
    return {'dimensions':[w,h],'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'regions':result,'note':'Region boundaries supplied by human/vision, not detected automatically. Exact observed colours are not automatically brand palette roles. Font names/sizes remain estimates.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('image',type=Path);p.add_argument('--regions',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    try:
        result=measure(a.image,json.loads(a.regions.read_text(encoding='utf-8')))
        if a.output.exists():raise ValueError('output exists; choose new path')
        a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'ok':True,'output':str(a.output)},ensure_ascii=False))
    except (OSError,ValueError,TypeError) as e:
        print(json.dumps({'ok':False,'errors':[str(e)]}));return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
