#!/usr/bin/env python3
"""v3: each business gets its own hero, section order, type and palette (design.py) on top of its facts (data.py)."""
import html, json, pathlib, urllib.parse
from data import L
from design import D
ROOT=pathlib.Path(__file__).parent; DOCS=ROOT/"docs"
BASE="https://reidwcoleman.github.io/site-previews"
e=html.escape
CSS=(ROOT/"site.css").read_text(); JS=(ROOT/"site.js").read_text()
def U(i,w=1600): return f"https://images.unsplash.com/photo-{i}?auto=format&fit=crop&w={w}&q=82"
def tm(m):
    h,mi=divmod(m,60); s="AM" if h<12 or h==24 else "PM"; h=h%12 or 12
    return f"{h}:{mi:02d} {s}" if mi else f"{h} {s}"
DAYS=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
def btn(b,tel,cls=""):
    href="#request" if b.get("form") else tel
    return f'<a class="btn {cls}" href="{href}"><span>{e(b["cta"])}</span><i class="ic ph-light ph-arrow-up-right"></i></a>'
def ghost(b,tel):
    return f'<a class="ghost" href="{tel}"><i class="ph-light ph-phone"></i>{e(b["phone"])}</a>' if b["phone"] and b.get("form") else ""
def hero(b,d,tel):
    tx=f'<p class="eye">{e(b["eyebrow"])}</p><h1>{e(b["head"])}</h1><p class="sub">{e(b["sub"])}</p><div class="acts">{btn(b,tel)}{ghost(b,tel)}</div>'
    h=d["hero"]; im=d["heroimg"]
    if h=="full": return f'<section class="h-full"><img class="kb" src="{U(im,2200)}" alt="" fetchpriority="high"><div class="wrap in">{tx}</div></section>'
    if h=="inset": return f'<section class="h-inset"><div class="fr"><img class="kb" src="{U(im,2200)}" alt="" fetchpriority="high"><div class="in">{tx}</div></div></section>'
    if h=="edge": return f'<section class="h-edge"><div class="tx">{tx}</div><div class="pic"><img class="kb" src="{U(im,1500)}" alt="" fetchpriority="high"></div></section>'
    a=d["heroalt"]
    if h=="type": return f'<section class="h-type wrap"><p class="eye">{e(b["eyebrow"])}</p><h1>{e(b["head"])}</h1><div class="row"><p class="sub">{e(b["sub"])}</p><div class="acts">{btn(b,tel)}{ghost(b,tel)}</div></div><div class="trio"><img src="{U(im,1500)}" alt="" fetchpriority="high"><img src="{U(a[0],900)}" alt=""><img src="{U(a[1],900)}" alt=""></div></section>'
    return f'<section class="h-casc wrap"><div class="tx">{tx}</div><div class="cards"><div class="bz c1"><img src="{U(im,1000)}" alt="" fetchpriority="high"></div><div class="bz c2"><img src="{U(a[0],700)}" alt=""></div><div class="bz c3"><img src="{U(a[1],700)}" alt=""></div></div></section>'
def sec_stats(b,d,tel):
    if not d["stats"]: return ""
    c="".join(f'<li><b>{e(n)}</b><span>{e(l)}</span></li>' for n,l in d["stats"])
    return f'<section class="stats wrap rv"><ul style="--n:{len(d["stats"])}">{c}</ul></section>'
def sid(i): return ' id="services"' if i else ""
def sec_board(b,d,tel):
    r="".join(f'<li class="rv"><div class="ln"><h3>{e(t)}</h3><span></span></div><p>{e(x)}</p></li>' for t,x in b["services"])
    return f'<section class="board wrap" id="services"><div class="bz pic"><img src="{U(d["imgs"][0],1100)}" alt="" loading="lazy"></div><div><h2 class="rv">{e(b["stitle"])}</h2><ol>{r}</ol></div></section>'
def sec_stack(b,d,tel):
    r="".join(f'<article style="--i:{i}"><div class="t"><h3>{e(t)}</h3><p>{e(x)}</p></div><img src="{U(d["imgs"][i%len(d["imgs"])],1200)}" alt="" loading="lazy"></article>' for i,(t,x) in enumerate(b["services"]))
    return f'<section class="stack wrap" id="services"><h2 class="rv">{e(b["stitle"])}</h2>{r}</section>'
def sec_bento(b,d,tel):
    n=len(b["services"]); P={2:["c7 im","c5 im"],3:["c7 r2 im","c5 tn","c5 im"],4:["c7 im","c5 tn","c5 im","c7 im"]}[n]
    ic=d.get("icons") or []
    cells=""
    for i,(t,x) in enumerate(b["services"]):
        k=P[i]
        if "im" in k: cells+=f'<article class="cell rv {k}"><img src="{U(d["imgs"][i%len(d["imgs"])],1300)}" alt="" loading="lazy"><div><h3>{e(t)}</h3><p>{e(x)}</p></div></article>'
        else:
            icon=f'<i class="ph-light ph-{ic[i]}"></i>' if i<len(ic) else ""
            cells+=f'<article class="cell rv {k}">{icon}<div><h3>{e(t)}</h3><p>{e(x)}</p></div></article>'
    return f'<section class="bento wrap" id="services"><h2 class="rv">{e(b["stitle"])}</h2><div class="grid">{cells}</div></section>'
def sec_hover(b,d,tel):
    items="".join(f'<li data-i="{i}" tabindex="0"{" class=on" if i==0 else ""}><h3>{e(t)}</h3><p>{e(x)}</p><img class="mob" src="{U(d["imgs"][i%len(d["imgs"])],900)}" alt="" loading="lazy"></li>' for i,(t,x) in enumerate(b["services"]))
    pane="".join(f'<img{" class=on" if i==0 else ""} data-i="{i}" src="{U(d["imgs"][i%len(d["imgs"])],1200)}" alt="" loading="lazy">' for i in range(len(b["services"])))
    return f'<section class="hov wrap" id="services"><div><h2 class="rv">{e(b["stitle"])}</h2><ul data-hover>{items}</ul></div><div class="bz pane"><div>{pane}</div></div></section>'
def sec_strips(b,d,tel):
    r="".join(f'<article tabindex="0"><img src="{U(d["imgs"][i%len(d["imgs"])],1200)}" alt="" loading="lazy"><div><h3>{e(t)}</h3><p>{e(x)}</p></div></article>' for i,(t,x) in enumerate(b["services"]))
    return f'<section class="strips wrap" id="services"><h2 class="rv">{e(b["stitle"])}</h2><div class="row rv">{r}</div></section>'
def sec_numeral(b,d,tel):
    return f'<section class="numeral"><div class="big" aria-hidden="true">{e(d["num"])}</div><div class="wrap rv"><h2>{e(b["story"][0])}</h2><p>{e(b["story"][1])}</p></div></section>'
def sec_statement(b,d,tel):
    return f'<section class="statement wrap rv"><h2>{e(b["story"][0])}</h2><p>{e(b["story"][1])}</p></section>'
def sec_photo(b,d,tel):
    i=d["imgs"][-1]
    return f'<section class="photo wrap"><div class="bz rv"><img src="{U(i,1200)}" alt="" loading="lazy"></div><div class="rv"><h2>{e(b["story"][0])}</h2><p>{e(b["story"][1])}</p></div></section>'
def sec_mosaic(b,d,tel):
    im=d["imgs"][-4:] if len(d["imgs"])>=4 else d["imgs"]
    return '<section class="mosaic wrap rv">'+"".join(f'<img src="{U(i,1200)}" alt="" loading="lazy">' for i in im)+'</section>'
def sec_scroll(b,d,tel):
    im=d["imgs"]+[d["heroimg"]]
    return '<section class="gs" tabindex="0" aria-label="Photos"><div>'+"".join(f'<img src="{U(i,1000)}" alt="" loading="lazy">' for i in im)+'</div></section>'
def sec_marquee(b,d,tel):
    w="".join(f'<li>{e(t)}<i class="ph-light ph-star"></i></li>' for t,_ in b["topics"])
    return f'<section class="mq" aria-label="What Google reviewers mention most"><ul>{w}{w}{w}</ul></section>'
def sec_cloud(b,d,tel):
    if not b["topics"]: return ""
    mx=max(c for _,c in b["topics"])
    w="".join(f'<li style="--s:{0.72+0.9*c/mx:.2f}">{e(t)}</li>' for t,c in b["topics"])
    return f'<section class="cloud wrap rv"><h2>What reviewers keep saying</h2><ul>{w}</ul></section>'
def sec_band(b,d,tel):
    return f'<section class="band"><img src="{U(d["imgs"][-1],2000)}" alt="" loading="lazy"><div class="wrap rv"><h2>{e(d["band"])}</h2>{btn(b,tel)}</div></section>'
def sec_stripes(b,d,tel):
    return f'<section class="stripes"><div class="wrap rv"><h2>{e(b["story"][0])}</h2><p>{e(b["story"][1])}</p></div></section>'
def sec_flavors(b,d,tel):
    tags=d["tags"]; cats=["All"]+sorted(set(tags))
    ch="".join(f'<button type="button" class="{"on" if c=="All" else ""}" data-f="{e(c)}">{e(c)}</button>' for c in cats)
    cards="".join(f'<li data-t="{e(t)}"><h3>{e(n)}</h3><p>{e(x)}</p></li>' for (n,x),t in zip(b["flavors"],tags))
    return f'<section class="flav wrap" id="flavors"><h2 class="rv">The flavors people drive for</h2><p class="rv lead">A different selection every day. Here are some favorites.</p><div class="fil rv" role="group" aria-label="Filter flavors">{ch}</div><ul class="rv" data-flav>{cards}</ul></section>'
def sec_req(b,d,tel):
    t,opts=b["form"]; o="".join(f'<label class="chip"><input type="radio" name="kind" value="{e(x)}"{" checked" if i==0 else ""}><span>{e(x)}</span></label>' for i,x in enumerate(opts))
    direct=f'<a class="dl" href="{tel}"><i class="ph-light ph-phone"></i>{e(b["phone"])}</a>' if b["phone"] else ""
    return f'''<section class="req wrap" id="request"><div class="rv"><h2>{e(t)}</h2><p>Tell us what you need and we'll get back to you.</p>{direct}<a class="dl" href="mailto:{e(b["email"])}"><i class="ph-light ph-envelope-simple"></i>{e(b["email"])}</a></div><div class="bz rv"><form data-demo><fieldset><legend>What do you need?</legend><div class="chips">{o}</div></fieldset><label>Your name<input name="n" autocomplete="name" required></label><label>Phone or email<input name="c" required></label><label>Details<textarea name="d" rows="3"></textarea></label><button class="btn" type="submit"><span>Send request</span><i class="ic ph-light ph-arrow-up-right"></i></button><p class="ok" role="status" hidden>Demo only, nothing was sent. On the live site this goes straight to {e(b["short"])}.</p></form></div></section>'''
def sec_visit(b,d,tel):
    hrs="".join(f'<tr data-d="{i}"><th>{DAYS[i]}</th><td>{"Call to confirm" if h=="call" else "Closed" if not h else ("Open 24 hours" if h==(0,1440) else tm(h[0])+" to "+tm(h[1]))}</td></tr>' for i,h in [(x,b["hours"][x]) for x in (1,2,3,4,5,6,0)])
    hn=f'<p class="hn">{e(b["hnote"])}</p>' if b["hnote"] else ""
    maps="https://www.google.com/maps?output=embed&q="+urllib.parse.quote_plus(b["name"]+" "+b["addr"])
    return f'<section class="visit wrap" id="visit"><div class="rv"><h2>Find us</h2><p class="ad">{e(b["addr"])}</p><p class="live" data-live hidden></p><table>{hrs}</table>{hn}</div><div class="bz rv"><iframe title="Map to {e(b["short"])}" src="{maps}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div></section>'
F=dict(stats=sec_stats,board=sec_board,stack=sec_stack,bento=sec_bento,hover=sec_hover,strips=sec_strips,numeral=sec_numeral,statement=sec_statement,photo=sec_photo,mosaic=sec_mosaic,scroll=sec_scroll,marquee=sec_marquee,cloud=sec_cloud,band=sec_band,stripes=sec_stripes,flavors=sec_flavors,req=sec_req,visit=sec_visit)
def fonts(d):
    def q(f,w):
        return "family="+urllib.parse.quote_plus(f)+w
    single=("Gloock","DM Serif Display","Young Serif")
    disp=d["disp"]
    if disp=="Archivo": a=q(disp,":wdth,wght@125,800")
    elif disp=="Bricolage Grotesque": a=q(disp,":opsz,wght@12..96,700;12..96,800")
    elif disp in single: a=q(disp,"")
    else: a=q(disp,":wght@500;600;700;800")
    if d["body"]==disp: return a
    return a+"&"+q(d["body"],":wght@400;500;600;700")
def page(b):
    d=D[b["slug"]]
    tel="tel:+1"+"".join(c for c in (b["phone"] or "") if c.isdigit())
    links=('<a href="#flavors">Flavors</a>' if b.get("flavors") else "")+'<a href="#services">Services</a><a href="#visit">Hours</a>'
    has_form=bool(b.get("form"))
    body="".join(F[s](b,d,tel) for s in d["order"])
    hj=json.dumps([h if h=="call" else (list(h) if h else None) for h in b["hours"]])
    up="uppercase" if d.get("upper") else "none"
    dw=f'font-stretch:125%;' if d.get("dw") else ""
    mob=f'<a class="mbar" href="{tel if b["phone"] else "#request"}"><i class="ph-light ph-{"phone" if b["phone"] else "arrow-up-right"}"></i>{"Call "+e(b["phone"]) if b["phone"] else e(b["cta"])}</a>'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>{e(b["name"])} | {e(b["city"])}</title><meta name="description" content="{e(b["sub"])}">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preconnect" href="https://images.unsplash.com"><link href="https://fonts.googleapis.com/css2?{fonts(d)}&display=swap" rel="stylesheet"><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/light/style.css">
<style>:root{{--bg:{d["bg"]};--surf:{d["surf"]};--ink:{d["ink"]};--accent:{d["accent"]};--on:{d["on"]};--r:{d["r"]}px;--btn:{d["btn"]};--disp:"{d["disp"]}",Georgia,serif;--body:"{d["body"]}",system-ui,sans-serif;--case:{up}}}h1,h2,h3,.brand,.big,footer .wm,.stats b{{{dw}}}{CSS}</style></head><body>
<div class="note">Preview by Reid Coleman for {e(b["short"])}. Sample photos. Not the official site yet.</div>
<div class="navw"><header class="nav"><a class="brand" href="#top">{e(b["short"] if len(b["name"])>24 else b["name"])}</a><nav>{links}</nav>{btn(b,tel,"sm")}<button class="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span></button></header></div>
<div class="ov" hidden><a href="#services">Services</a>{'<a href="#flavors">Flavors</a>' if b.get("flavors") else ""}<a href="#visit">Hours</a>{'<a href="#request">'+e(b["cta"])+'</a>' if has_form else ""}</div>
<main id="top">{hero(b,d,tel)}{body}</main>
<footer><div class="wrap"><div class="wm">{e(b["short"])}</div><div class="fl"><span>{e(b["addr"])}</span>{f'<a href="{tel}">{e(b["phone"])}</a>' if b["phone"] else ""}<a href="mailto:{e(b["email"])}">{e(b["email"])}</a></div></div></footer>{mob}
<script>window.BIZ={{h:{hj},tz:"{b["tz"]}"}};{JS}</script></body></html>
'''
for b in L:
    d=DOCS/b["slug"]; d.mkdir(parents=True,exist_ok=True); (d/"index.html").write_text(page(b)); b["url"]=f'{BASE}/{b["slug"]}/'
(ROOT/"leads.json").write_text(json.dumps(L,indent=1,ensure_ascii=False))
print(len(L),"sites built")
