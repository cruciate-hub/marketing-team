# Detect frame lines (1px, #202022-ish) and + markers in board vs staging screenshots, full resolution.
import sys
from PIL import Image
W=int(sys.argv[1]) if len(sys.argv)>1 else 1440
def near(p,c=(32,32,34),t=10): return all(abs(p[i]-c[i])<=t for i in range(3))
def hlines(path):
    im=Image.open(path).convert('RGB');w,h=im.size;px=im.load();out=[]
    for y in range(h):
        n=sum(1 for x in range(0,w,4) if near(px[x,y]))
        if n> (w/4)*0.55: out.append(y)
    # collapse consecutive rows
    res=[];
    for y in out:
        if not res or y-res[-1][1]>1: res.append([y,y])
        else: res[-1][1]=y
    return [a for a,b in res],h
def vlines(path):
    im=Image.open(path).convert('RGB');w,h=im.size;px=im.load();out=[]
    for x in range(w):
        n=sum(1 for y in range(0,h,4) if near(px[x,y]))
        if n>(h/4)*0.35: out.append(x)
    return out
for src in ('board','stage'):
    p=f'cmp-{src}-{W}.png';hl,h=hlines(p);vl=vlines(p)
    print(src,'height',h,'h-lines',len(hl),hl)
    print(src,'v-lines',vl)
