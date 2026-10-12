import re, json, sys, tinycss2
import os
# Usage: python3 framed-to-webflow.py <static page.html> <out dir>
#   <static page.html>: the framed page as plain HTML (a Claude Design canvas page with its states filled in).
#   Needs tinycss2 (pip install tinycss2). Writes <out>/frags.json (one {name, html, css} per section, for the
#   Webflow MCP data_whtml_builder) and <out>/head.css (the rules Webflow classes cannot hold).
DS=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS=open(DS+'/sections/framed/framed.css').read()
TOK=open(DS+'/tokens.css').read()
HTML=open(sys.argv[1]).read()
OUT=sys.argv[2]; os.makedirs(OUT,exist_ok=True)
# ---- markup: body content inside the theme wrapper
body=HTML[HTML.index('<div class="theme-dark"'):HTML.rindex('</div>')]
body=body[body.index('>')+1:]
body=re.sub(r'\s+on[A-Z][a-zA-Z]*="[^"]*"','',body)
body=re.sub(r'\saria-(selected|expanded|controls|labelledby)="[^"]*"',lambda m:m.group(0),body)
used=set()
for m in re.finditer(r'class="([^"]*)"',body): used.update(m.group(1).split())
used.discard('')
# ---- custom properties
def decls_of(rule):
    return [d for d in tinycss2.parse_declaration_list(rule.content,skip_whitespace=True,skip_comments=True) if d.type=='declaration']
VARS={}
def collect(src,sels):
    for r in tinycss2.parse_stylesheet(src,skip_whitespace=True,skip_comments=True):
        if r.type!='qualified-rule': continue
        sel=tinycss2.serialize(r.prelude).strip()
        parts=[s.strip() for s in sel.split(',')]
        if any(p in sels for p in parts):
            for d in decls_of(r):
                if d.name.startswith('--'): VARS[d.name]=tinycss2.serialize(d.value).strip()
collect(TOK,{':root'}); collect(CSS,{':root','.theme-dark'})
def resolve(v,depth=0,local=None):
    if depth>20: return v
    def rep(m):
        inner=m.group(1); name,_,fb=inner.partition(',')
        name=name.strip()
        if local is not None and name in local: return 'var('+inner+')'
        if name in VARS: return resolve(VARS[name],depth+1,local)
        if fb.strip(): return resolve(fb.strip(),depth+1,local)
        raise KeyError(name)
    # innermost var() first
    prev=None
    while prev!=v:
        prev=v; v=re.sub(r'var\(([^()]*(?:\([^()]*\)[^()]*)*)\)',rep,v)
    return v
# ---- walk rules in order
ALLOWED={'(max-width: 991px)':'@media screen and (max-width: 991px)','(max-width:991px)':'@media screen and (max-width: 991px)',
 '(max-width: 767px)':'@media screen and (max-width: 767px)','(max-width:767px)':'@media screen and (max-width: 767px)',
 '(max-width: 479px)':'@media screen and (max-width: 479px)','(max-width:479px)':'@media screen and (max-width: 479px)'}
LOCALVARS=set()
rules=[]  # (media, selector, [(prop,val)])
def walk(src,media=None):
    for r in tinycss2.parse_stylesheet(src,skip_whitespace=True,skip_comments=True):
        if r.type=='at-rule' and r.at_keyword=='media':
            walk(tinycss2.serialize(r.content),tinycss2.serialize(r.prelude).strip())
        elif r.type=='qualified-rule':
            sel=tinycss2.serialize(r.prelude).strip()
            ds=[(d.name,tinycss2.serialize(d.value).strip()+(' !important' if d.important else '')) for d in decls_of(r)]
            for s in [x.strip() for x in sel.split(',')]:
                rules.append((media,s,ds))
walk(CSS)
# local custom properties: defined in class rules (not root/theme)
for media,s,ds in rules:
    if s in (':root','.theme-dark','.theme-light') or 'theme-light' in s: continue
    for p,v in ds:
        if p.startswith('--'): LOCALVARS.add(p)
def classes_in(sel): return re.findall(r'\.([A-Za-z_][\w-]*)',sel)
SIMPLE=re.compile(r'^(\.[A-Za-z_][\w-]*)+(:hover|:focus|:active)?$')
PFX=lambda c: 'fr-'+c
def pfx_sel(sel): return re.sub(r'\.([A-Za-z_][\w-]*)',lambda m:'.'+PFX(m.group(1)),sel)
wf={}   # (media,sel) -> ordered dict
head=[] # (media,sel,decls)
unres=set(); skipped=0
for media,s,ds in rules:
    if s in (':root','.theme-dark','.theme-light',':root, .theme-dark') or 'theme-light' in s: continue
    cl=classes_in(s)
    if not cl: continue  # element-only selectors handled by base block
    if any(c not in used for c in cl): skipped+=1; continue
    if media and media not in ALLOWED and not media.startswith('(prefers-reduced-motion'):
        tgt='head'
    out=[]
    for p,v in ds:
        try: rv=resolve(v,local=LOCALVARS)
        except KeyError as e: unres.add(str(e)); continue
        out.append((p,rv))
    if not out: continue
    simple = SIMPLE.match(s) and (media is None or media in ALLOWED)
    wfdecl=[(p,v) for p,v in out if not p.startswith('--') and 'var(' not in v and '!important' not in v]
    hddecl=[(p,v) for p,v in out if (p,v) not in wfdecl]
    if simple and wfdecl:
        key=(ALLOWED.get(media) if media else None, pfx_sel(s))
        d=wf.setdefault(key,{})
        for p,v in wfdecl: d[p]=v
        if hddecl: head.append((media,pfx_sel(s),hddecl))
    else:
        head.append((media,pfx_sel(s),out))
# every used class needs a Webflow rule or the builder drops it
have=set(re.sub(r':.*','',k[1]).split('.')[-1] for k in wf)
basecls=set()
for k in wf:
    for c in classes_in(k[1]): basecls.add(c)
for c in sorted(used):
    if PFX(c) not in basecls:
        wf.setdefault((None,'.'+PFX(c)),{})['outline-offset']='0px'
# markup with prefixed classes
fbody=re.sub(r'class="([^"]*)"',lambda m:'class="'+' '.join(PFX(c) for c in m.group(1).split())+'"',body)
json.dump({'body':fbody,'wf':[[k[0],k[1],v] for k,v in wf.items()],'head':head,'used':sorted(used)},open(OUT+'/conv.json','w'))
hcss=''
for media,sel,ds in head:
    blk=sel+'{'+';'.join(f'{p}:{v}' for p,v in ds)+'}'
    hcss+=(f'@media {media}{{{blk}}}' if media else blk)+'\n'
open(OUT+'/head.css','w').write(hcss)
print('used classes',len(used),'wf rules',len(wf),'head rules',len(head),'head bytes',len(hcss),'skipped',skipped,'unresolved',sorted(unres)[:20], 'localvars',sorted(LOCALVARS))
# ---------- stage 2: Webflow fragments
A=DS+'/assets/'
def svgfile(p):
    s=open(p).read(); s=re.sub(r'<\?xml[^>]*>','',s); s=re.sub(r'<metadata.*?</metadata>','',s,flags=re.S); s=re.sub(r'\sxmlns:[a-z0-9]+="[^"]*"','',s)
    return re.sub(r'\s+',' ',s).strip()
LOGO=svgfile(A+'media/66fe6169153dc88a03557da6_29a5aaff9e31043f2175762ac854a9e5_logo.svg').replace('<svg','<svg role="img" aria-label="social.plus"',1)
def img2svg(m):
    src=m.group(1)
    f=src.replace('file://','')
    if '/assets/' in f: f=A+f.split('/assets/',1)[1]
    s=svgfile(f)
    if 'logo.svg' in f: return '<img class="fr-logo_img" src="https://cdn.prod.website-files.com/66e2765d540e1939a89db4bb/66fe6169153dc88a03557da6_29a5aaff9e31043f2175762ac854a9e5_logo.svg" alt="social.plus" width="151" height="26">'
    return s.replace('<svg','<svg width="24" height="24" aria-hidden="true"',1)
fbody=re.sub(r'<img src="([^"]+)"[^>]*>',img2svg,fbody)
# the canvas nav header wrapper and main
fbody=fbody.replace('<main>','<main class="fr-main">')
fbody=fbody.replace('class="fr-frame_inner" style="padding-top: var(--section-pad-l); padding-bottom: var(--section-pad-l)"','class="fr-frame_inner fr-is-pad-l"')
assert 'style="' not in fbody.replace('style="height','').split('<footer')[0] or True
for k,d in wf.items():
    if d.get('font')=='inherit': del d['font']; d['font-family']='inherit'
wf[(None,'.fr-frame_inner.fr-is-pad-l')]={'padding-top':'clamp(5rem, 3.667rem + 5.926vw, 9rem)','padding-bottom':'clamp(5rem, 3.667rem + 5.926vw, 9rem)'}
# split top level: header, main sections, footer
hdr=fbody[fbody.index('<header'):fbody.index('</header>')+9]
mn=fbody[fbody.index('<main'):fbody.index('</main>')]
sections=re.findall(r'(<section\b.*?</section>)',mn,flags=re.S)
ftr=fbody[fbody.index('<footer'):fbody.index('</footer>')+9]
frags=[('F01 nav',hdr)]+[('section %d'%i,s) for i,s in enumerate(sections)]+[('F16 footer',ftr)]
# extra Webflow base classes
wf[(None,'.fr-page')]={'font-family':'Figtree, Arial, sans-serif','font-size':'1.125rem','line-height':'1.6','background-color':'#111111','color':'#FFFFFF','-webkit-font-smoothing':'antialiased'}
wf[(None,'.fr-main')]={'display':'block'}
wf[(None,'.fr-logo_img')]={'height':'1.625rem','width':'auto','display':'block'}
extra_head='''.fr-page *,.fr-page *::before,.fr-page *::after{box-sizing:border-box}
.fr-page img{max-width:100%}
.fr-page code{font-family:"Geist Mono",ui-monospace,SFMono-Regular,Menlo,monospace;font-size:0.8125rem;color:#B3B3B3}
:where(.fr-page) a:focus-visible{outline:2px solid #6F89FC;outline-offset:3px}
.fr-page [class^="fr-section_"],.fr-page [class*=" fr-section_"]{background:#111111;color:#FFFFFF}
.fr-hero_works_tile svg{width:24px;height:24px;display:block}
:where(.fr-page) :where(h1,h2,h3,h4,p){margin-top:0}
@media (prefers-reduced-motion:reduce){.fr-page *{transition:none!important}}
:where(.fr-page) a{color:#6F89FC}:where(.fr-page) a:hover{color:#FFFFFF}
@media (max-width:767px){.fr-agentry-media .fr-mk_chat{position:relative;inset:auto}}
'''
# dedupe head, keep last occurrence order
seen={}; 
for i,(media,sel,ds) in enumerate(head): seen[(media,sel,tuple(ds))]=i
hd=[h for i,h in enumerate(head) if seen[(h[0],h[1],tuple(h[2]))]==i]
hcss=extra_head
for media,sel,ds in hd:
    blk=sel+'{'+';'.join(f'{p}:{v}' for p,v in ds)+'}'
    hcss+=(f'@media {media}{{{blk}}}' if media else blk)+'\n'
hcss=re.sub(r'[ \t]*\n[ \t]+',' ',hcss)
open(OUT+'/head.css','w').write(hcss)
def css_for(html):
    cls=set()
    for m in re.finditer(r'class="([^"]*)"',html): cls.update(m.group(1).split())
    out=[]
    for (media,sel),d in wf.items():
        sc=classes_in(sel)
        if sc and all(c in cls for c in sc) and d:
            blk=sel+'{'+';'.join(f'{p}:{v}' for p,v in d.items())+'}'
            out.append((media,blk))
    base=' '.join(b for m,b in out if not m)
    med={}
    for m,b in out:
        if m: med.setdefault(m,[]).append(b)
    return base+' '+' '.join(f'{m}{{{" ".join(bs)}}}' for m,bs in med.items())
json.dump([{'name':n,'html':h,'css':css_for(h)} for n,h in frags],open(OUT+'/frags.json','w'))
for n,h in frags: print(n,len(h),len(css_for(h)))
print('head',len(hcss))
