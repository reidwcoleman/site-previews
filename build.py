#!/usr/bin/env python3
"""Generates one preview site per lead into docs/<slug>/index.html and leads.json."""
import html, json, pathlib, urllib.parse
ROOT = pathlib.Path(__file__).parent
DOCS = ROOT / "docs"
BASE = "https://reidwcoleman.github.io/site-previews"

M = {
 "tree": '<path d="M100 20 150 90h-24l34 48h-30l40 52H30l40-52H40l34-48H50z"/><rect x="88" y="190" width="24" height="44"/>',
 "tools": '<rect x="30" y="150" width="140" height="70" rx="6"/><path d="M100 24 186 104H14z"/><rect x="84" y="172" width="32" height="48" fill="var(--bg)"/>',
 "blades": '<path d="M100 226C60 190 34 150 40 96c34 6 52 26 60 52 8-26 26-46 60-52 6 54-20 94-60 130z"/><rect x="94" y="30" width="12" height="120" rx="6"/>',
 "stone": '<rect x="20" y="60" width="74" height="44" rx="4"/><rect x="104" y="60" width="76" height="44" rx="4"/><rect x="20" y="114" width="40" height="44" rx="4"/><rect x="70" y="114" width="110" height="44" rx="4"/><rect x="20" y="168" width="96" height="44" rx="4"/><rect x="126" y="168" width="54" height="44" rx="4"/>',
 "paw": '<ellipse cx="100" cy="160" rx="52" ry="44"/><ellipse cx="46" cy="104" rx="20" ry="28"/><ellipse cx="82" cy="66" rx="20" ry="30"/><ellipse cx="124" cy="66" rx="20" ry="30"/><ellipse cx="158" cy="104" rx="20" ry="28"/>',
 "pipe": '<path d="M20 60h96a44 44 0 0 1 44 44v110h-44V112a8 8 0 0 0-8-8H20z"/><rect x="104" y="202" width="68" height="20" rx="4"/><rect x="12" y="48" width="20" height="68" rx="4"/>',
 "roller": '<rect x="24" y="36" width="140" height="56" rx="10"/><path d="M164 58h20v58h-78v34h-12v-46h78V70h-8z"/><rect x="90" y="150" width="20" height="84" rx="6"/>',
 "razor": '<rect x="70" y="16" width="60" height="16" rx="8"/><rect x="70" y="208" width="60" height="16" rx="8"/><rect x="78" y="32" width="44" height="176"/><path d="M78 62l44-26v24L78 86zM78 112l44-26v24l-44 26zM78 162l44-26v24l-44 26z" fill="var(--bg)"/>',
 "cake": '<path d="M46 110h108l-14 112H60z"/><path d="M36 110c0-44 30-52 44-52 6-26 34-34 52-14 26 0 42 30 32 66z"/><circle cx="104" cy="28" r="14"/>',
 "wrench": '<path d="M150 22a50 50 0 0 0-58 66L24 156a24 24 0 0 0 34 34l68-68a50 50 0 0 0 66-58l-32 32-30-8-8-30z"/>',
}

L = [
 dict(slug="mailes-tree-service", name="Mailes Tree Service", email="mailestreeservice@gmail.com", phone="(417) 849-6883", addr="4714 N Peace Church Ave, Joplin, MO", city="Joplin, Missouri",
      head="Need a tree removed?", sub="Get a free quote today. Fully licensed, bonded and insured.", items=["Tree removal","Free quotes","Licensed, bonded and insured"], rating="4.9", reviews=31,
      motif="tree", layout="split", font="Bitter", bg="#F3F0E4", ink="#1E2A1F", accent="#2F5D3A", on="#FFFFFF", tint="#E3E3CF",
      why="no-site", hook="your 4.9 stars on Google"),
 dict(slug="rooneys-renovating", name="Rooney's Renovating LLC", email="RooneysRenovating@gmail.com", phone="(419) 595-0506", addr="Brookville, OH", city="Brookville, Ohio",
      head="Maintenance, turns and full rehabs.", sub="Rooney's Renovating handles maintenance requests, unit turns and full rehabs out of Brookville, Ohio.", items=["Maintenance requests","Unit turns","Full rehabs"], rating=None, reviews=0,
      motif="tools", layout="poster", font="Archivo", bg="#14202E", ink="#EEF2F6", accent="#F2913D", on="#14202E", tint="#1F2F42",
      why="fb", hook="the maintenance, unit turn and rehab work you do"),
 dict(slug="holder-lawn-service", name="Holder Lawn Service", email="holderlawnservice@gmail.com", phone="(662) 523-5922", addr="745 CR 931, Tupelo, MS", city="Northeast Mississippi",
      head="Get your yard back.", sub="Lawn maintenance across Northeast Mississippi, from routine mowing to reclaiming your yard from heavy growth or debris.", items=["Routine mowing","Reclaiming overgrown yards","Debris cleanup"], rating=None, reviews=0,
      motif="blades", layout="split", font="Rubik", bg="#EEF4E4", ink="#1D2B16", accent="#3F7A22", on="#FFFFFF", tint="#DCE8CC",
      why="fb", hook="your lawn work around Northeast Mississippi"),
 dict(slug="precision-landscaping", name="Precision Landscaping", email="theprecisionlandscaping@yahoo.com", phone="(785) 829-7401", addr="1413 Beverly Dr, Salina, KS 67401", city="Salina, Kansas",
      head="Hardscape done with precision.", sub="A hardscape landscaping company based in Salina, Kansas.", items=["Hardscape","Landscaping"], rating="4.5", reviews=13,
      motif="stone", layout="ledger", font="Libre Franklin", bg="#F1EDE6", ink="#2A2622", accent="#8A4B2A", on="#FFFFFF", tint="#E2DBD0",
      why="fb", hook="your hardscape work in Salina"),
 dict(slug="el-rancho-kennels", name="El Rancho Kennels", email="Elranchokennels@gmail.com", phone="(207) 825-3242", addr="418 Johnson Mill Rd, Orrington, ME 04474", city="Orrington, Maine",
      head="Boarding, daycare and grooming.", sub="A small, family owned and operated business in Orrington, Maine.", items=["Boarding","Daycare","Grooming"], rating="4.9", reviews=92,
      motif="paw", layout="split", font="Vollkorn", bg="#FBF1E3", ink="#3A1F17", accent="#A63A24", on="#FFFFFF", tint="#F3DFC6",
      why="fb", hook="your 4.9 stars from 92 Google reviews"),
 dict(slug="wells-septic-installation", name="Wells Septic Installation, LLC", email="Wellsseptic21@gmail.com", phone="(601) 419-1014", addr="117 S High School Ave, Columbia, MS 39429", city="Columbia, Mississippi",
      head="Septic installation in Columbia.", sub="Wells Septic Installation, LLC, at 117 S High School Ave in Columbia, Mississippi.", items=["Septic installation"], rating=None, reviews=0,
      motif="pipe", layout="poster", font="Barlow", bg="#10292B", ink="#E9F3F1", accent="#4FC2B0", on="#10292B", tint="#183A3D",
      why="fb", hook="your septic installation business in Columbia"),
 dict(slug="ck-precision-painting", name="C&K Precision Painting LLC", email="ckprecisionpainting@gmail.com", phone="(218) 221-2446", addr="3167 Midway Rd, Proctor, MN 55810", city="the Twin Ports",
      head="Painting with pride and passion.", sub="Exterior and interior painting for businesses and homes across the Twin Ports for 22-plus years. Locally owned and family run.", items=["Exterior painting","Interior painting","Business and residential","Free estimates"], rating="5.0", reviews=11,
      motif="roller", layout="ledger", font="Work Sans", bg="#F5F4F0", ink="#1F2433", accent="#2B4BB5", on="#FFFFFF", tint="#E4E5E8",
      why="fb", hook="your 22-plus years painting around the Twin Ports"),
 dict(slug="mayos-barber-shop", name="Mayo's Barber Shop", email="mayosbarbershop@gmail.com", phone="(251) 473-4321", addr="1868 Airport Blvd, Mobile, AL 36606", city="Mobile, Alabama",
      head="Hot towels and straight razors.", sub="Established in 1960 and going strong ever since. Like it should be.", items=["Hot towel shaves","Straight razor work","Est. 1960"], rating="4.8", reviews=126,
      motif="razor", layout="poster", font="Abril Fatface", bg="#191613", ink="#F4EBDD", accent="#D9A441", on="#191613", tint="#2A2520",
      why="fb", hook="a shop going strong since 1960 with 4.8 stars from 126 Google reviews"),
 dict(slug="elidas-bakery", name="Elida's Bakery", email="elidasbakery@gmail.com", phone=None, addr="2128 S Riverside Dr #99, Iowa City, IA 52246", city="Iowa City, Iowa",
      head="Custom cakes, cupcakes and more.", sub="A licensed home bakery in Iowa City. Curbside pickup available. Se habla español.", items=["Custom cakes","Cupcakes","Curbside pickup"], rating="4.9", reviews=58,
      motif="cake", layout="split", font="Fraunces", bg="#FCEFEF", ink="#3D1B2C", accent="#9C2F60", on="#FFFFFF", tint="#F6DCE0",
      why="fb", hook="your custom cakes and 4.9 stars from 58 Google reviews"),
 dict(slug="shepros-auto-repair", name="Shepro's Auto Repair", email="sheprosautorepair@gmail.com", phone="(906) 753-5823", addr="S955 US Highway 41, Stephenson, MI", city="Stephenson, Michigan",
      head="Auto repair on Highway 41.", sub="Find Shepro's Auto Repair on Highway 41 in Stephenson, Michigan.", items=["Auto repair"], rating="4.9", reviews=74,
      motif="wrench", layout="ledger", font="Oswald", bg="#EFEFEC", ink="#1C1E20", accent="#C2281E", on="#FFFFFF", tint="#DEDFDB",
      why="none", hook="your 4.9 stars from 74 Google reviews"),
 dict(slug="erikas-dog-gone-grooming", name="Erika's Dog-Gone Grooming Salon", email="doggonegroomingsalon22@gmail.com", phone="(615) 675-4189", addr="895 South Water Ave, Gallatin, TN", city="Gallatin, Tennessee",
      head="One-on-one grooming for senior dogs.", sub="A one-on-one dog groomer specializing in senior dogs, located in Gallatin, Tennessee.", items=["One-on-one grooming","Senior dog specialist"], rating=None, reviews=0,
      motif="paw", layout="split", font="Nunito", bg="#EAF3F5", ink="#14323B", accent="#17697C", on="#FFFFFF", tint="#D5E7EB",
      why="none", hook="your one-on-one grooming for senior dogs"),
 dict(slug="head-to-tail-grooming", name="Head to Tail Professional Pet Grooming", email="headtotailvt@icloud.com", phone="(802) 772-4556", addr="144 Grove St, Rutland, VT", city="Rutland, Vermont",
      head="Professional pet grooming in Rutland.", sub="Head to Tail, at 144 Grove Street in Rutland, Vermont.", items=["Professional pet grooming"], rating="4.8", reviews=106,
      motif="paw", layout="ledger", font="Lora", bg="#F0F1EA", ink="#23291F", accent="#56663A", on="#FFFFFF", tint="#E0E3D4",
      why="fb", hook="your 4.8 stars from 106 Google reviews"),
 dict(slug="margies-mixing-bowl", name="Margie's Mixing Bowl", email="info@margiesmixingbowl.com", phone="(601) 207-0111", addr="4920 Poplar Springs Dr, Meridian, MS", city="Meridian, Mississippi",
      head="Gourmet cupcakes, cakes and macarons.", sub="For birthday parties, weddings, showers, client gifts, a meeting, or a special treat for you.", items=["Gourmet cupcakes","Custom cakes","Macarons","Meridian Star Readers' Choice, 2016 to 2022"], rating="4.6", reviews=78,
      motif="cake", layout="poster", font="Playfair Display", bg="#3A1626", ink="#FBEEF2", accent="#F4A9C0", on="#3A1626", tint="#4E2135",
      why="old", hook="all those Readers' Choice wins"),
]

CSS = """
*{box-sizing:border-box;margin:0}
html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font:400 18px/1.55 var(--body);-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}
.note{background:var(--ink);color:var(--bg);font-size:14px;line-height:1.4;padding:8px 0}
.top{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:24px 0}
.brand{font:700 20px/1.2 var(--disp)}
.top a.tel{font-weight:600;text-decoration:none;font-variant-numeric:tabular-nums;white-space:nowrap}
.hero{display:grid;grid-template-columns:1.25fr .75fr;gap:48px;align-items:center;padding:48px 0 80px}
h1{font:700 clamp(42px,7vw,76px)/1.05 var(--disp);letter-spacing:-.01em}
.sub{margin-top:20px;max-width:34em;font-size:20px;line-height:1.5;opacity:.82}
.cta{display:inline-block;white-space:nowrap;margin-top:32px;padding:16px 32px;background:var(--accent);color:var(--on);font-weight:700;text-decoration:none;border-radius:8px;transition:transform .15s ease-out}
.cta:hover{transform:translateY(-1px)}.cta:active{transform:scale(.97)}
.cta:focus-visible,a:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
.rate{margin-top:20px;font-size:16px;font-variant-numeric:tabular-nums}
.rate b{font-weight:700}
.art{justify-self:center;width:100%;max-width:300px}
.art svg{display:block;width:100%;height:auto;fill:var(--accent)}
.band{background:var(--tint);padding:64px 0}
h2{font:700 30px/1.2 var(--disp);margin-bottom:24px}
ul.items{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:0 48px}
ul.items li{padding:16px 0;border-top:1px solid color-mix(in srgb,var(--ink) 22%,transparent);font-size:20px;font-weight:600}
.visit{padding:64px 0 80px;display:grid;grid-template-columns:1fr 1fr;gap:48px}
.visit dt{font-size:14px;letter-spacing:.06em;text-transform:uppercase;opacity:.7;margin-top:20px}
.visit dt:first-child{margin-top:0}
.visit dd{margin:4px 0 0;font-size:20px;overflow-wrap:anywhere}
footer{padding:24px 0;font-size:14px;opacity:.72;border-top:1px solid color-mix(in srgb,var(--ink) 18%,transparent)}
[data-layout=poster] .hero{grid-template-columns:1fr;padding:64px 0 96px;position:relative;overflow:hidden}
[data-layout=poster] h1{font-size:clamp(48px,10vw,116px);max-width:11em;position:relative}
[data-layout=poster] .sub,[data-layout=poster] .cta,[data-layout=poster] .rate{position:relative}
[data-layout=poster] .art{position:absolute;right:-24px;bottom:-32px;max-width:340px;opacity:.16;justify-self:auto}
[data-layout=ledger] .hero{grid-template-columns:200px 1fr;align-items:start;padding:64px 0 80px}
[data-layout=ledger] .art{max-width:160px;justify-self:start;order:-1}
@media (max-width:760px){
 body{font-size:17px}.wrap{padding:0 16px}
 .hero,[data-layout=ledger] .hero{grid-template-columns:1fr;gap:32px;padding:32px 0 56px}
 .art,[data-layout=ledger] .art{max-width:130px;justify-self:start;order:-1}
 [data-layout=poster] .art{order:0;max-width:200px}
 .visit{grid-template-columns:1fr;gap:32px;padding:48px 0 56px}.band{padding:48px 0}
 .cta{display:block;text-align:center}
}
@media (prefers-reduced-motion:reduce){.cta{transition:none}}
"""

def page(b):
    e = html.escape
    fam = urllib.parse.quote_plus(b["font"])
    wght = ":wght@400;700" if b["font"] not in ("Abril Fatface",) else ""
    maps = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote_plus(b["name"] + " " + b["addr"])
    tel = "tel:+1" + "".join(c for c in (b["phone"] or "") if c.isdigit())
    cta = f'<a class="cta" href="{tel}">Call {e(b["phone"])}</a>' if b["phone"] else f'<a class="cta" href="mailto:{e(b["email"])}">Email to order</a>'
    toptel = f'<a class="tel" href="{tel}">{e(b["phone"])}</a>' if b["phone"] else ""
    rate = f'<p class="rate"><b>{b["rating"]}</b> stars from {b["reviews"]} Google reviews</p>' if b["rating"] else ""
    items = "".join(f"<li>{e(i)}</li>" for i in b["items"])
    phone_row = f'<dt>Phone</dt><dd><a href="{tel}">{e(b["phone"])}</a></dd>' if b["phone"] else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{e(b["name"])} | {e(b["city"])}</title>
<meta name="description" content="{e(b["sub"])}">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={fam}{wght}&display=swap" rel="stylesheet">
<style>:root{{--bg:{b["bg"]};--ink:{b["ink"]};--accent:{b["accent"]};--on:{b["on"]};--tint:{b["tint"]};--disp:"{b["font"]}",Georgia,serif;--body:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}}{CSS}</style>
</head><body data-layout="{b["layout"]}">
<div class="note"><div class="wrap">Preview made by Brian Coleman for {e(b["name"])}. This is not their official website.</div></div>
<div class="wrap">
<header class="top"><div class="brand">{e(b["name"])}</div>{toptel}</header>
<section class="hero"><div><h1>{e(b["head"])}</h1><p class="sub">{e(b["sub"])}</p>{cta}{rate}</div>
<div class="art" aria-hidden="true"><svg viewBox="0 0 200 240">{M[b["motif"]]}</svg></div></section>
</div>
<section class="band"><div class="wrap"><h2>What you can count on</h2><ul class="items">{items}</ul></div></section>
<div class="wrap"><section class="visit"><div><h2>Get in touch</h2><dl>{phone_row}<dt>Email</dt><dd><a href="mailto:{e(b["email"])}">{e(b["email"])}</a></dd></dl></div>
<div><h2>Find us</h2><dl><dt>Address</dt><dd><a href="{maps}">{e(b["addr"])}</a></dd></dl></div></section>
<footer>Details come from this business's public Google and Facebook listings.</footer></div>
</body></html>
"""

DOCS.mkdir(exist_ok=True)
(DOCS / ".nojekyll").write_text("")
(DOCS / "index.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Site previews</title></head><body style="font:18px system-ui;padding:24px">Private previews. Please use the link you were sent.</body></html>\n')
(DOCS / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
for b in L:
    d = DOCS / b["slug"]; d.mkdir(exist_ok=True)
    (d / "index.html").write_text(page(b))
    b["url"] = f'{BASE}/{b["slug"]}/'
(ROOT / "leads.json").write_text(json.dumps(L, indent=1, ensure_ascii=False))
print(len(L), "sites built")
