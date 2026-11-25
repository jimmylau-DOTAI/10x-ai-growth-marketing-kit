#!/usr/bin/env python3
"""Pixel diagnostics only; not a semantic/style similarity percentage."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageChops,ImageStat

def compare(first,second,threshold=16):
    with Image.open(first) as im:a=im.convert('RGB')
    with Image.open(second) as im:b=im.convert('RGB')
    if a.size != b.size:raise ValueError('dimensions differ; no automatic resizing for comparison')
    delta=ImageChops.difference(a,b);stat=ImageStat.Stat(delta)
    pixels=list(delta.getdata()); changed=sum(max(pixel)>threshold for pixel in pixels)/len(pixels)
    return {'dimensions':list(a.size),'mean_absolute_channel_error_0_255':sum(stat.mean)/3,'fraction_pixels_over_threshold':changed,'threshold_0_255':threshold,'note':'Not match %, perceptual similarity, text accuracy, or rights clearance. Large backgrounds can dominate the result.'},delta

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('reference',type=Path);p.add_argument('rebuild',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--threshold',type=int,default=16);a=p.parse_args()
    try:
        if not 0<=a.threshold<=255:raise ValueError('threshold must be 0..255')
        if a.output.exists():raise ValueError('output directory exists; choose a new one')
        result,diff=compare(a.reference,a.rebuild,a.threshold);a.output.mkdir(parents=True);diff.save(a.output/'difference.png');(a.output/'comparison.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
    except (OSError,ValueError) as e: print(json.dumps({'ok':False,'errors':[str(e)]}));return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
