#!/usr/bin/env python3
"""Assemble docs/*.html from src/*.src.html + partials. Run: python3 build.py"""
import pathlib,re,shutil
root=pathlib.Path(__file__).parent; src=root/'src'; docs=root/'docs'; docs.mkdir(exist_ok=True)
head=(src/'_head.html').read_text(); foot=(src/'_footer.html').read_text()
shutil.copy(src/'site.css',docs/'site.css')
for f in sorted(src.glob('*.src.html')):
    page=f.name.replace('.src.html','')
    body=f.read_text()
    m=re.search(r'<!--\s*title:(.*?)\|desc:(.*?)-->',body,re.S)
    title=m.group(1).strip() if m else 'RTB Gym'; desc=m.group(2).strip() if m else ''
    out=head.replace('__TITLE__',title).replace('__DESC__',desc).replace('__PAGE__',page)+body+foot
    if page=='index': out=out.replace('https://rtbgym.com.au/index.html','https://rtbgym.com.au/')
    (docs/(page+'.html')).write_text(out); print(f'  docs/{page}.html  {len(out)//1024} KB')
# old Squarespace URLs -> new pages (GitHub Pages has no server redirects, so folder stubs)
REDIRECTS={'21-day-strength-trial':'reset.html','21-day-strength':'reset.html#book','program':'app.html',
 'book-the-gym':'studio.html','home':'./','contact':'./#start','services':'./#start','trial':'reset.html'}
for old,new in REDIRECTS.items():
    d=docs/old; d.mkdir(exist_ok=True)
    (d/'index.html').write_text(f'<!DOCTYPE html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/{new}"><link rel="canonical" href="https://rtbgym.com.au/{new}"><title>RTB Gym</title></head><body><a href="/{new}">Continue</a></body></html>')
# /booked = the page Hapana sends people to after booking a call (GA4 key event lives on this path)
bk=docs/'booked'; bk.mkdir(exist_ok=True)
t=(docs/'thanks.html').read_text().replace("(location.search.match(/src=([a-z]+)/)||[])[1]||'unknown'","'call'").replace('href="img/','href="/img/').replace('src="img/','src="/img/').replace('href="site.css"','href="/site.css"')
for p in ['index','reset','experience','workshop','app','about','thanks','studio','call']: t=t.replace(f'href="{p}.html"',f'href="/{p}.html"')
(bk/'index.html').write_text(t)
(docs/'CNAME').write_text('rtbgym.com.au\n')
(docs/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://rtbgym.com.au/sitemap.xml\n')
pages=['','reset.html','experience.html','workshop.html','app.html','about.html','studio.html']
(docs/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://rtbgym.com.au/{p}</loc></url>\n' for p in pages)+'</urlset>\n')
(docs/'404.html').write_text('<!DOCTYPE html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="2;url=/"><title>RTB Gym</title><style>body{font-family:system-ui;background:#F5F5F5;color:#000;display:grid;place-items:center;height:100vh;margin:0;text-align:center}</style></head><body><div><h1>Page moved.</h1><p>Taking you to <a href="/">rtbgym.com.au</a>.</p></div></body></html>')
print('redirects, booked, CNAME, robots, sitemap, 404 written')
print('Built.')
