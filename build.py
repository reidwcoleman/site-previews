#!/usr/bin/env python3
"""Builds docs/<slug>/index.html for every lead in data.py, plus leads.json."""
import html, json, pathlib, urllib.parse
from data import L
ROOT=pathlib.Path(__file__).parent; DOCS=ROOT/"docs"
BASE="https://reidwcoleman.github.io/site-previews"
e=html.escape
def img(i,w=1600): return f"https://images.unsplash.com/photo-{i}?auto=format&fit=crop&w={w}&q=80"
CSS=(ROOT/"site.css").read_text(); JS=(ROOT/"site.js").read_text()
def tm(m):
    h,mi=divmod(m,60); s="AM" if h<12 or h==24 else "PM"; h=h%12 or 12
    return f"{h}:{mi:02d} {s}" if mi else f"{h} {s}"
DAYS=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
def page(b):
    fams="&".join("family="+urllib.parse.quote_plus(f)+(":wght@400;500;600;700" if f not in("Abril Fatface","DM Serif Display","Young Serif") else "") for f in dict.fromkeys([b["font"],b["bfont"]]))
    tel="tel:+1"+"".join(c for c in (b["phone"] or "") if c.isdigit())
    has_form=bool(b.get("form"))
    primary=f'<a class="btn" href="{"#request" if has_form else tel}">{e(b["cta"])}</a>'
    second=f'<a class="btn ghost" href="{tel}">{e(b["phone"])}</a>' if b["phone"] and has_form else ""
    navcall=f'<a class="navcall" href="{tel}">{e(b["phone"])}</a>' if b["phone"] else '<a class="navcall" href="#request">Order</a>'
    ph=b["photos"]
    stars=f'<div class="stars"><b>{b["rating"]}</b><span>{b["reviews"]} Google reviews</span></div>' if b["rating"] and b["reviews"]>=10 else ""
    if b["hero"]=="immersive":
        hero=f'<section class="hero imm" style="--ph:url({img(ph[0],2000)})"><div class="wrap"><p class="eye">{e(b["eyebrow"])}</p><h1>{e(b["head"])}</h1><p class="sub">{e(b["sub"])}</p><div class="acts">{primary}{second}</div>{stars}</div></section>'
    elif b["hero"]=="split":
        hero=f'<section class="hero spl wrap"><div class="tx"><p class="eye">{e(b["eyebrow"])}</p><h1>{e(b["head"])}</h1><p class="sub">{e(b["sub"])}</p><div class="acts">{primary}{second}</div>{stars}</div><div class="pics"><img class="a" src="{img(ph[0],1100)}" alt="" fetchpriority="high"><img class="b" src="{img(ph[1],700)}" alt=""></div></section>'
    else:
        hero=f'<section class="hero frm wrap"><div class="tx"><p class="eye">{e(b["eyebrow"])}</p><h1>{e(b["head"])}</h1><div class="side"><p class="sub">{e(b["sub"])}</p><div class="acts">{primary}{second}</div></div></div><div class="big"><img src="{img(ph[0],2000)}" alt="" fetchpriority="high">{stars}</div></section>'
    facts="".join(f"<li>{e(f)}</li>" for f in b["facts"])
    svc="".join(f'<li class="rv"><span class="n">{i:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i,(t,d) in enumerate(b["services"],1))
    fl=""
    if b.get("flavors"):
        cards="".join(f'<li class="rv"><h3>{e(n)}</h3><p>{e(d)}</p></li>' for n,d in b["flavors"])
        fl=f'<section class="flav" id="flavors"><div class="wrap"><p class="eye">A different selection every day</p><h2>The flavors people drive for</h2><ul>{cards}</ul></div></section>'
    gal=f'<section class="gal wrap rv"><img src="{img(ph[1],1200)}" alt="" loading="lazy"><img src="{img(ph[2],900)}" alt="" loading="lazy"><img src="{img(ph[3],900)}" alt="" loading="lazy"></section>'
    tp=""
    if b["topics"]:
        mx=max(c for _,c in b["topics"])
        rows="".join(f'<li><span>{e(t)}</span><i style="--w:{round(c/mx*100)}%"></i><b>{c}</b></li>' for t,c in b["topics"])
        tp=f'<div class="said rv"><p class="eye">What Google reviewers mention most</p><ul>{rows}</ul></div>'
    story=f'<section class="story"><div class="wrap st"><div class="rv"><h2>{e(b["story"][0])}</h2><p>{e(b["story"][1])}</p></div>{tp}</div></section>'
    form=""
    if has_form:
        t,opts=b["form"]; o="".join(f'<label class="chip"><input type="radio" name="kind" value="{e(x)}"{" checked" if i==0 else ""}><span>{e(x)}</span></label>' for i,x in enumerate(opts))
        form=f'''<section class="req wrap" id="request"><div class="rv"><h2>{e(t)}</h2><p>Tell us what you need and we'll get back to you.</p></div><form class="rv" data-demo><fieldset><legend>What do you need?</legend><div class="chips">{o}</div></fieldset><label>Your name<input name="n" autocomplete="name" required></label><label>Phone or email<input name="c" required></label><label>Details<textarea name="d" rows="3"></textarea></label><button class="btn" type="submit">Send request</button><p class="ok" role="status" hidden>Demo only, nothing was sent. On the live site this goes straight to {e(b["short"])}.</p></form></section>'''
    hrs="".join(f'<tr data-d="{i}"><th>{DAYS[i]}</th><td>{"Closed" if not h else ("Open 24 hours" if h==(0,1440) else tm(h[0])+" to "+tm(h[1]))}</td></tr>' for i,h in [(x,b["hours"][x]) for x in (1,2,3,4,5,6,0)])
    hn=f'<p class="hn">{e(b["hnote"])}</p>' if b["hnote"] else ""
    maps="https://www.google.com/maps?output=embed&q="+urllib.parse.quote_plus(b["name"]+" "+b["addr"])
    phone_row=f'<p><a href="{tel}">{e(b["phone"])}</a></p>' if b["phone"] else ""
    hj=json.dumps([list(h) if h else None for h in b["hours"]])
    mobile=f'<a class="mbar" href="{tel if b["phone"] else "#request"}">{"Call "+e(b["phone"]) if b["phone"] else e(b["cta"])}</a>'
    links=('<a href="#flavors">Flavors</a>' if b.get("flavors") else "")+'<a href="#services">Services</a><a href="#visit">Hours</a>'+('<a href="#request">Contact</a>' if has_form else "")
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>{e(b["name"])} | {e(b["city"])}</title><meta name="description" content="{e(b["sub"])}">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preconnect" href="https://images.unsplash.com"><link href="https://fonts.googleapis.com/css2?{fams}&display=swap" rel="stylesheet">
<style>:root{{--bg:{b["bg"]};--ink:{b["ink"]};--accent:{b["accent"]};--on:{b["on"]};--tint:{b["tint"]};--line:{b["line"]};--r:{b["r"]}px;--disp:"{b["font"]}",Georgia,serif;--body:"{b["bfont"]}",system-ui,sans-serif}}{CSS}</style></head><body>
<div class="note">Preview by Reid Coleman for {e(b["short"])}. Sample photos. Not the official site yet.</div>
<header class="nav"><div class="wrap"><a class="brand" href="#top">{e(b["short"] if len(b["name"])>26 else b["name"])}</a><nav>{links}</nav>{navcall}</div></header>
<main id="top">{hero}
<ul class="facts wrap">{facts}<li class="live" data-live hidden></li></ul>
{fl}
<section class="svc wrap" id="services"><h2 class="rv">{e(b["stitle"])}</h2><ol>{svc}</ol></section>
{gal}{story}{form}
<section class="visit wrap" id="visit"><div class="rv"><h2>Visit</h2><p class="ad">{e(b["addr"])}</p>{phone_row}<p><a href="mailto:{e(b["email"])}">{e(b["email"])}</a></p><table>{hrs}</table>{hn}</div><iframe class="rv" title="Map to {e(b["short"])}" src="{maps}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></section>
</main><footer class="wrap"><span>{e(b["name"])}</span><span>{e(b["city"])}</span></footer>{mobile}
<script>window.BIZ={{h:{hj},tz:"{b["tz"]}"}};{JS}</script></body></html>
'''
for b in L:
    d=DOCS/b["slug"]; d.mkdir(parents=True,exist_ok=True); (d/"index.html").write_text(page(b)); b["url"]=f'{BASE}/{b["slug"]}/'
(ROOT/"leads.json").write_text(json.dumps(L,indent=1,ensure_ascii=False))
print(len(L),"sites built")
