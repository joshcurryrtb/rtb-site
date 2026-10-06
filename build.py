#!/usr/bin/env python3
"""Assemble docs/*.html from src/*.src.html + partials. Run: python3 build.py"""
import pathlib,re,shutil
root=pathlib.Path(__file__).parent; src=root/'src'; docs=root/'docs'; docs.mkdir(exist_ok=True)
head=(src/'_head.html').read_text(); foot=(src/'_footer.html').read_text()
shutil.copy(src/'site.css',docs/'site.css')
# Apply landing pages: one template, three audiences. Women + men are ad only pages; `apply` is the
# gender neutral one for Instagram bios and Google. The gym comes from ?gym=windsor|chelsea.
APPLY={'apply':('all','Apply for the 21 Day Strength Reset | RTB Gym','Stronger and leaner with zero cardio. Coached strength training capped at 12, in Windsor and Chelsea Heights. Apply for the 21 Day Strength Reset.'),
 'apply-women':('women','Apply for the 21 Day Strength Reset | RTB Gym','Leaner, tighter and twice as strong with zero cardio. Coached strength training for women, capped at 12. Apply for the 21 Day Strength Reset.'),
 'apply-men':('men','Apply for the 21 Day Strength Reset | RTB Gym','Stronger, leaner and built to last with zero cardio. Coached strength training for men, capped at 12. Apply for the 21 Day Strength Reset.')}
tpl=(src/'_apply.tpl.html').read_text()
sources=[(f.name.replace('.src.html',''),f.read_text()) for f in sorted(src.glob('*.src.html'))]
sources+=[(pg,tpl.replace('__G__',g).replace('__T__',t).replace('__D__',d)) for pg,(g,t,d) in APPLY.items()]
for page,body in sources:
    m=re.search(r'<!--\s*title:(.*?)\|desc:(.*?)-->',body,re.S)
    title=m.group(1).strip() if m else 'RTB Gym'; desc=m.group(2).strip() if m else ''
    out=head.replace('__TITLE__',title).replace('__DESC__',desc).replace('__PAGE__',page)+body+foot
    if page=='reset' or page in APPLY:  # ad landing page: no way off the page except booking
        out=re.sub(r'<a href="index.html">(<img class="logo"[^>]*>)</a>',r'\1',out)
        out=re.sub(r'\s*<button class="burger".*?</button>','',out,flags=re.S)
        out=re.sub(r'\s*<div class="links">.*?</div>','',out,count=1,flags=re.S)
        if page in APPLY:
            out=out.replace('<a class="cta" href="apply.html#apply">Book a free call</a>','<a class="cta" href="#apply">Explore my options</a>')
            out=out.replace('href="apply.html#apply"','href="#apply"').replace('href="apply.html"','href="#apply"')
            if page!='apply': out=out.replace('<meta property="og:type"','<meta name="robots" content="noindex">\n<meta property="og:type"',1)
        out=out.replace('href="reset.html#book"','href="#book"')
    if page=='reset':  # 6 Oct 2026: the neutral apply page replaced the old 21 Day Reset page. The URL stays alive as a redirect for old ads, bios and Google.
        out='<!DOCTYPE html><html><head><meta charset="utf-8"><title>21 Day Strength Reset | RTB Gym</title><link rel="canonical" href="https://rtbgym.com.au/apply.html"><meta http-equiv="refresh" content="0;url=/apply.html"><script>location.replace("/apply.html"+location.search+(location.hash==="#book"?"#apply":location.hash))</script></head><body><a href="/apply.html">Continue to the 21 Day Strength Reset</a></body></html>'
        f0,f1=out.index('<footer>'),out.index('</footer>')+9
        ft=out[f0:f1]
        ft=re.sub(r'\s*<div>\s*<h4>Start here</h4>.*?</div>','',ft,flags=re.S)
        ft=re.sub(r'<li><a [^>]*>.*?</a></li>\s*','',ft)
        ft=re.sub(r' &middot; <a [^>]*>.*?</a>','',ft)
        out=out[:f0]+ft+out[f1:]
    if page=='index': out=out.replace('https://rtbgym.com.au/index.html','https://rtbgym.com.au/')
    (docs/(page+'.html')).write_text(out); print(f'  docs/{page}.html  {len(out)//1024} KB')
# old Squarespace URLs -> new pages (GitHub Pages has no server redirects, so folder stubs)
REDIRECTS={'21-day-strength-trial':'apply.html','21-day-strength':'apply.html','program':'app.html',
 'book-the-gym':'studio.html','home':'./','contact':'./#start','services':'./#start','trial':'apply.html'}
for old,new in REDIRECTS.items():
    d=docs/old; d.mkdir(exist_ok=True)
    (d/'index.html').write_text(f'<!DOCTYPE html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/{new}"><link rel="canonical" href="https://rtbgym.com.au/{new}"><title>RTB Gym</title></head><body><a href="/{new}">Continue</a></body></html>')
# /booked = the page Hapana sends people to after booking a call (GA4 key event lives on this path)
bk=docs/'booked'; bk.mkdir(exist_ok=True)
t=(docs/'thanks.html').read_text().replace("(location.search.match(/src=([a-z]+)/)||[])[1]||'unknown'","'call'").replace('href="img/','href="/img/').replace('src="img/','src="/img/').replace('href="site.css"','href="/site.css"')
for p in ['index','reset','experience','workshop','app','about','thanks','studio','call','privacy']: t=t.replace(f'href="{p}.html"',f'href="/{p}.html"')
(bk/'index.html').write_text(t)
(docs/'CNAME').write_text('rtbgym.com.au\n')
(docs/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://rtbgym.com.au/sitemap.xml\n')
pages=['','apply.html','experience.html','workshop.html','app.html','about.html','studio.html','privacy.html']
(docs/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://rtbgym.com.au/{p}</loc></url>\n' for p in pages)+'</urlset>\n')
(docs/'404.html').write_text('<!DOCTYPE html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="2;url=/"><title>RTB Gym</title><style>body{font-family:system-ui;background:#F5F5F5;color:#000;display:grid;place-items:center;height:100vh;margin:0;text-align:center}</style></head><body><div><h1>Page moved.</h1><p>Taking you to <a href="/">rtbgym.com.au</a>.</p></div></body></html>')
print('redirects, booked, CNAME, robots, sitemap, 404 written')
print('Built.')
