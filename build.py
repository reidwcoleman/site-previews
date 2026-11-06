#!/usr/bin/env python3
"""v4: art direction per business (design.py) over sourced facts (data.py). Mobile-first output, inline icons, responsive images."""
import html, json, pathlib, urllib.parse
from data import L
from design import D
ROOT=pathlib.Path(__file__).parent; DOCS=ROOT/"docs"
BASE="https://reidwcoleman.github.io/site-previews"
e=html.escape
CSS=(ROOT/"site.css").read_text(); JS=(ROOT/"site.js").read_text(); IC=json.load(open(ROOT/"icons.json"))
def ic(n,c=""): return f'<svg class="i {c}" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">{IC[n]}</svg>'
def U(i,w=1600): return f"https://images.unsplash.com/photo-{i}?auto=format&fit=crop&w={w}&q=78"
def SS(i,ws=(480,768,1100,1600,2200)): return ", ".join(f"{U(i,w)} {w}w" for w in ws)
def I(i,sizes="100vw",lazy=True,cls="",ws=(480,768,1100,1600,2200)):
    a='loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    c=f' class="{cls}"' if cls else ""
    return f'<img{c} src="{U(i,1100)}" srcset="{SS(i,ws)}" sizes="{sizes}" alt="" {a}>'
def tm(m):
    h,mi=divmod(m,60); s="AM" if h<12 or h==24 else "PM"; h=h%12 or 12
    return f"{h}:{mi:02d} {s}" if mi else f"{h} {s}"
DAYS=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
def href(b,tel): return tel if b.get("cta_tel") or not b.get("form") else "#request"
def btn(b,tel,cls=""): return f'<a class="btn {cls}" href="{href(b,tel)}"><span>{e(b["cta"])}</span><b class="ic">{ic("arrow-up-right")}</b></a>'
def ghost(b,tel): return f'<a class="ghost" href="{tel}">{ic("phone")}{e(b["phone"])}</a>' if b["phone"] and not b.get("cta_tel") else ""
def hero(b,d,tel):
    tx=f'<p class="eye">{e(b["eyebrow"])}</p><h1>{e(b["head"])}</h1><p class="sub">{e(b["sub"])}</p><div class="acts">{btn(b,tel)}{ghost(b,tel)}</div>'
    h=d["hero"]; im=d["heroimg"]
    if h=="full": return f'<section class="h-full">{I(im,"100vw",False,"kb")}<div class="wrap in ld">{tx}</div></section>'
    if h=="inset": return f'<section class="h-inset"><div class="fr">{I(im,"100vw",False,"kb")}<div class="in ld">{tx}</div></div></section>'
    if h=="edge": return f'<section class="h-edge"><div class="tx ld">{tx}</div><div class="pic">{I(im,"(max-width:900px) 100vw, 50vw",False,"kb")}</div></section>'
    a=d["heroalt"]
    if h=="type": return f'<section class="h-type wrap"><div class="ld"><p class="eye">{e(b["eyebrow"])}</p><h1>{e(b["head"])}</h1><div class="row"><p class="sub">{e(b["sub"])}</p><div class="acts">{btn(b,tel)}{ghost(b,tel)}</div></div></div><div class="trio">{I(im,"(max-width:900px) 100vw, 55vw",False)}{I(a[0],"(max-width:900px) 50vw, 25vw")}{I(a[1],"(max-width:900px) 50vw, 25vw")}</div></section>'
    return f'<section class="h-casc wrap"><div class="tx ld">{tx}</div><div class="cards"><div class="bz c1">{I(im,"(max-width:900px) 100vw, 36vw",False)}</div><div class="bz c2">{I(a[0],"(max-width:900px) 50vw, 24vw")}</div><div class="bz c3">{I(a[1],"(max-width:900px) 50vw, 22vw")}</div></div></section>'
def sec_stats(b,d,tel):
    if not d["stats"]: return ""
    c="".join(f'<li><b>{e(n)}</b><span>{e(l)}</span></li>' for n,l in d["stats"])
    return f'<section class="stats wrap rv"><ul style="--n:{len(d["stats"])}">{c}</ul></section>'
def sec_scrolly(b,d,tel):
    im="".join(I(d["imgs"][i%len(d["imgs"])],"100vw",True,"on" if i==0 else "") .replace("<img",f'<img data-i="{i}"') for i in range(len(b["services"])))
    st="".join(f'<article data-i="{i}"><div class="pn"><h3>{e(t)}</h3><p>{e(x)}</p></div></article>' for i,(t,x) in enumerate(b["services"]))
    return f'<section class="sy" id="services" data-sy><div class="stick">{im}</div><div class="steps"><header><h2>{e(b["stitle"])}</h2></header>{st}</div></section>'
def sec_stack(b,d,tel):
    r="".join(f'<article style="--i:{i}"><div class="t"><h3>{e(t)}</h3><p>{e(x)}</p></div>{I(d["imgs"][i%len(d["imgs"])],"(max-width:900px) 84vw, 55vw")}</article>' for i,(t,x) in enumerate(b["services"]))
    return f'<section class="stack wrap" id="services"><h2 class="rv">{e(b["stitle"])}</h2><div class="deck">{r}</div></section>'
def sec_bento(b,d,tel):
    n=len(b["services"]); P={3:["c7 r2 im","c5 tn","c5 im"],4:["c7 im","c5 tn","c5 im","c7 im"]}[n]
    icn=d.get("icons") or []; cells=""
    for i,(t,x) in enumerate(b["services"]):
        k=P[i]
        if "im" in k: cells+=f'<article class="cell {k}">{I(d["imgs"][i%len(d["imgs"])],"(max-width:900px) 84vw, 58vw")}<div><h3>{e(t)}</h3><p>{e(x)}</p></div></article>'
        else: cells+=f'<article class="cell {k}">{ic(icn[i],"big") if i<len(icn) else ""}<div><h3>{e(t)}</h3><p>{e(x)}</p></div></article>'
    return f'<section class="bento wrap" id="services"><h2 class="rv">{e(b["stitle"])}</h2><div class="grid deck">{cells}</div></section>'
def sec_hover(b,d,tel):
    items="".join(f'<li data-i="{i}" tabindex="0"{" class=on" if i==0 else ""}>{I(d["imgs"][i%len(d["imgs"])],"84vw",True,"mob",(480,768))}<h3>{e(t)}</h3><p>{e(x)}</p></li>' for i,(t,x) in enumerate(b["services"]))
    pane="".join(I(d["imgs"][i%len(d["imgs"])],"45vw",True,"on" if i==0 else "",(768,1100,1600)).replace("<img",f'<img data-i="{i}"') for i in range(len(b["services"])))
    return f'<section class="hov wrap" id="services"><div><h2 class="rv">{e(b["stitle"])}</h2><ul class="deck" data-hover>{items}</ul></div><div class="bz pane"><div>{pane}</div></div></section>'
def sec_strips(b,d,tel):
    r="".join(f'<article tabindex="0">{I(d["imgs"][i%len(d["imgs"])],"(max-width:900px) 84vw, 45vw")}<div><h3>{e(t)}</h3><p>{e(x)}</p></div></article>' for i,(t,x) in enumerate(b["services"]))
    return f'<section class="strips wrap" id="services"><h2 class="rv">{e(b["stitle"])}</h2><div class="row deck">{r}</div></section>'
def sec_numeral(b,d,tel): return f'<section class="numeral"><div class="big" aria-hidden="true">{e(d["num"])}</div><div class="wrap rv"><h2>{e(b["story"][0])}</h2><p>{e(b["story"][1])}</p></div></section>'
def sec_statement(b,d,tel): return f'<section class="statement wrap rv"><h2>{e(b["story"][0])}</h2><p>{e(b["story"][1])}</p></section>'
def sec_photo(b,d,tel):
    i=d.get("photo") or d["imgs"][-1]
    return f'<section class="photo wrap"><div class="bz rv">{I(i,"(max-width:900px) 100vw, 50vw")}</div><div class="rv"><h2>{e(b["story"][0])}</h2><p>{e(b["story"][1])}</p></div></section>'
def sec_mosaic(b,d,tel): return '<section class="mosaic wrap rv">'+"".join(I(i,"(max-width:900px) 100vw, 50vw") for i in d["mosaic"])+'</section>'
def sec_scroll(b,d,tel): return '<section class="gs" tabindex="0" aria-label="Photos"><div>'+"".join(I(i,"(max-width:900px) 78vw, 40vw",True,"",(480,768,1100)) for i in d["gallery"])+'</div></section>'
def sec_praise(b,d,tel):
    p=d.get("praise")
    if not p: return ""
    stars=ic("star")
    c="".join(f'<li class="rv"><div class="st5">{stars}</div><p>{e(x)}</p></li>' for x in p)
    return f'<section class="praise wrap"><h2 class="rv">What customers say on Google</h2><ul class="deck">{c}</ul></section>'
def sec_pole(b,d,tel): return '<div class="pole" aria-hidden="true"></div>'
def sec_stripes(b,d,tel): return f'<section class="stripes"><div class="wrap rv"><h2>{e(b["story"][0])}</h2><p>{e(b["story"][1])}</p></div></section>'
def sec_flavors(b,d,tel):
    tags=d["tags"]; cats=["All"]+sorted(set(tags))
    ch="".join(f'<button type="button" class="{"on" if c=="All" else ""}" data-f="{e(c)}">{e(c)}</button>' for c in cats)
    cards="".join(f'<li data-t="{e(t)}"><button type="button" class="fl" data-n="{e(n)}" data-c="{c}"><i style="--c:{c}"></i><span><h3>{e(n)}</h3><small>{e(x)}</small></span><b>{ic("check")}</b></button></li>' for (n,x),t,c in zip(b["flavors"],tags,d["colors"]))
    slots='<i class="slot"></i>'*6
    return f'''<section class="flav wrap" id="flavors"><h2 class="rv">Build your box of six</h2><p class="rv lead">Tap flavors to fill the box. The case changes every day, so call to see what is in today.</p>
<div class="boxbar" data-box><div class="slots">{slots}</div><p data-boxtxt>Pick up to 6 flavors</p><a class="btn sm" href="{tel}"><span>Call to order</span><b class="ic">{ic("arrow-up-right")}</b></a></div>
<div class="fil rv" role="group" aria-label="Filter flavors">{ch}</div><ul class="rv" data-flav>{cards}</ul></section>'''
def sec_req(b,d,tel):
    t,opts=b["form"]
    def chips(leg,os,name): return f'<fieldset><legend>{e(leg)}</legend><div class="chips">'+"".join(f'<label class="chip"><input type="radio" name="{name}" value="{e(x)}"{" checked" if i==0 else ""}><span>{e(x)}</span></label>' for i,x in enumerate(os))+'</div></fieldset>'
    g=chips("What do you need?",opts,"k1")
    if d.get("g2"): g+=chips(d["g2"][0],d["g2"][1],"k2")
    if d.get("dates"): g+='<div class="two"><label>Drop-off<input type="date" name="a"></label><label>Pick-up<input type="date" name="z"></label></div>'
    direct=f'<a class="dl" href="{tel}">{ic("phone")}{e(b["phone"])}</a>' if b["phone"] else ""
    return f'''<section class="req wrap" id="request"><div class="rv"><h2>{e(t)}</h2><p>Tell us what you need and we'll get back to you.</p>{direct}<a class="dl" href="mailto:{e(b["email"])}">{ic("envelope-simple")}{e(b["email"])}</a></div><div class="bz rv"><form data-demo>{g}<label>Your name<input name="n" autocomplete="name" enterkeyhint="next" required></label><label>Phone number<input name="c" type="tel" inputmode="tel" autocomplete="tel" enterkeyhint="next" required></label><label>Details<textarea name="d" rows="3" enterkeyhint="done"></textarea></label><button class="btn" type="submit"><span>Send request</span><b class="ic">{ic("arrow-up-right")}</b></button><p class="ok" role="status" hidden>Demo only, nothing was sent. On the live site this goes straight to {e(b["short"])}.</p></form></div></section>'''
def dirs(b): return "https://www.google.com/maps/dir/?api=1&destination="+urllib.parse.quote_plus(b["name"]+" "+b["addr"])
def sec_visit(b,d,tel):
    hrs="".join(f'<tr data-d="{i}"><th>{DAYS[i]}</th><td>{"Call to confirm" if h=="call" else "Closed" if not h else ("Open 24 hours" if h==(0,1440) else tm(h[0])+" to "+tm(h[1]))}</td></tr>' for i,h in [(x,b["hours"][x]) for x in (1,2,3,4,5,6,0)])
    hn=f'<p class="hn">{e(b["hnote"])}</p>' if b["hnote"] else ""
    maps="https://www.google.com/maps?output=embed&q="+urllib.parse.quote_plus(b["name"]+" "+b["addr"])
    return f'<section class="visit wrap" id="visit"><div class="rv"><h2>Find us</h2><p class="ad">{e(b["addr"])}</p><p class="live" data-live hidden></p><table>{hrs}</table>{hn}<a class="dirbtn" href="{dirs(b)}">{ic("navigation-arrow")}Get directions</a></div><div class="bz rv mapbox" data-map="{e(maps)}" data-t="Map to {e(b["short"])}"></div></section>'
F={k[4:]:v for k,v in globals().items() if k.startswith("sec_")}
def fonts(d):
    q=lambda f,w:"family="+urllib.parse.quote_plus(f)+w
    single=("Gloock","DM Serif Display","Young Serif"); disp=d["disp"]
    if disp=="Archivo": a=q(disp,":wdth,wght@125,800")
    elif disp=="Bricolage Grotesque": a=q(disp,":opsz,wght@12..96,700;12..96,800")
    elif disp in single: a=q(disp,"")
    else: a=q(disp,":wght@500;600;700;800")
    return a if d["body"]==disp else a+"&"+q(d["body"],":wght@400;500;600;700")
def page(b):
    d=D[b["slug"]]
    tel="tel:+1"+"".join(c for c in (b["phone"] or "") if c.isdigit())
    flav=bool(b.get("flavors"))
    links=('<a href="#flavors">Flavors</a>' if flav else "")+'<a href="#services">Services</a><a href="#visit">Hours</a>'
    body="".join(F[s](b,d,tel) for s in d["order"])
    hj=json.dumps([h if h=="call" else (list(h) if h else None) for h in b["hours"]])
    up="uppercase" if d.get("upper") else "none"
    dw='font-stretch:125%;' if d.get("dw") else ""
    dock=f'<nav class="dock" aria-label="Quick actions"><a class="p" href="{tel if b["phone"] else "#request"}">{ic("phone") if b["phone"] else ic("arrow-up-right")}{"Call" if b["phone"] else e(b["cta"])}</a><a href="{dirs(b)}">{ic("navigation-arrow")}Directions</a></nav>'
    mono=e(b["short"][0]); fav="data:image/svg+xml,"+urllib.parse.quote(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{d["accent"]}"/><text x="32" y="45" font-family="Georgia,serif" font-size="38" font-weight="700" text-anchor="middle" fill="{d["on"]}">{mono}</text></svg>')
    him=d["heroimg"]; ov=('<a href="#flavors">Flavors</a>' if flav else "")+'<a href="#services">Services</a><a href="#visit">Hours</a><a href="#request">Contact</a>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="{d["bg"]}"><meta name="format-detection" content="telephone=no">
<title>{e(b["name"])} | {e(b["city"])}</title><meta name="description" content="{e(b["sub"])}"><meta property="og:title" content="{e(b["name"])}"><meta property="og:description" content="{e(b["sub"])}"><meta property="og:image" content="{U(him,1200)}"><link rel="icon" href="{fav}">
<link rel="preconnect" href="https://images.unsplash.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preload" as="image" imagesrcset="{SS(him)}" imagesizes="100vw" fetchpriority="high"><link href="https://fonts.googleapis.com/css2?{fonts(d)}&display=swap" rel="stylesheet">
<style>:root{{--bg:{d["bg"]};--surf:{d["surf"]};--ink:{d["ink"]};--accent:{d["accent"]};--on:{d["on"]};--r:{d["r"]}px;--btn:{d["btn"]};--disp:"{d["disp"]}",Georgia,serif;--body:"{d["body"]}",system-ui,sans-serif;--case:{up}}}h1,h2,h3,.brand,.big,.wm,.stats b{{{dw}}}{CSS}</style></head><body>
<div class="note">Preview by Reid Coleman, not the official site. Sample photos.</div>
<div class="navw"><header class="nav"><a class="brand" href="#top">{e(b["short"] if len(b["name"])>24 else b["name"])}</a><nav>{links}</nav>{btn(b,tel,"sm")}<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span></button></header></div>
<div class="ov" hidden>{ov}</div>
<main id="top">{hero(b,d,tel)}{body}</main>
<footer><div class="wrap"><div class="wm">{e(b["short"])}</div><div class="fl2"><span>{e(b["addr"])}</span>{f'<a href="{tel}">{e(b["phone"])}</a>' if b["phone"] else ""}<a href="mailto:{e(b["email"])}">{e(b["email"])}</a></div></div></footer>{dock}
<script>window.BIZ={{h:{hj},tz:"{b["tz"]}"}};{JS}</script></body></html>
'''
for b in L:
    p=DOCS/b["slug"]; p.mkdir(parents=True,exist_ok=True); (p/"index.html").write_text(page(b)); b["url"]=f'{BASE}/{b["slug"]}/'
(ROOT/"leads.json").write_text(json.dumps(L,indent=1,ensure_ascii=False))
print(len(L),"sites built")
