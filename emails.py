#!/usr/bin/env python3
"""Writes emails.json: one personalized email per lead, signed Reid, for sending from reidwcoleman@gmail.com."""
import json
L=json.load(open('leads.json'))
out=[]
for b in L:
    nm=b['name'].replace(' LLC','').replace(', LLC','').rstrip(',')
    if b['slug']=='head-to-tail-grooming': nm='Head to Tail'
    if b['why']=='old':
        subj=f"A fresh website for {nm}"
        gap="I noticed your website is on a free Wix address with the Wix ad bar across the top, and it's still thanking customers for 2020, so I made a new one for you to check out:"
    else:
        subj=f"I made a website for {nm}"
        gap="I noticed you guys don't have a website"+(", just your Facebook page," if b['why']=='fb' else ",")+" so I made one for you to check out:"
    body=f"""Hi there,

My name is Reid. I came across {nm} on Google Maps and liked seeing {b['hook']}. {gap}

{b['url']}

It already has your services, hours, a map and a request form. The photos are samples until yours go in, and anything can be changed.

If you like it, what would you be willing to pay for it? Any number helps, and there's no obligation at all.

Thanks,
Reid Coleman
reidwcoleman@gmail.com

{{ADDRESS}}
If you'd rather not hear from me, just reply "no thanks" and I won't email you again."""
    out.append(dict(to=b['email'],subject=subj,body=body,slug=b['slug']))
json.dump(out,open('emails.json','w'),indent=1,ensure_ascii=False)
print(len(out)); print(out[0]['subject']); print(out[0]['body'][:330])
