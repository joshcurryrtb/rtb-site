#!/usr/bin/env python3
"""Assemble docs/*.html from src/*.src.html + partials. Run: python3 build.py"""
import pathlib,re,shutil
root=pathlib.Path(__file__).parent; src=root/'src'; docs=root/'docs'; docs.mkdir(exist_ok=True)
head=(src/'_head.html').read_text(); foot=(src/'_footer.html').read_text()
shutil.copy(src/'site.css',docs/'site.css')
# Landing page lab (29 Oct 2026): experiments.json is baked into docs/lab.js. Drafts ship too so ?lab=ID:V previews work; only `live` ones split traffic.
import json
LAB=json.loads((src/'experiments.json').read_text())
lab_cfg={'api':'https://lilmmmxgoprrvsnrzppb.supabase.co/functions/v1/lab','exps':[{k:x[k] for k in ('id','status','pages','variants')} for x in LAB['experiments'] if x['status'] in ('draft','live')]}
for x in lab_cfg['exps']:
    for v in x['variants'].values(): v.pop('note',None)
(docs/'lab.js').write_text((src/'lab.js').read_text().replace('__LAB_CFG__',json.dumps(lab_cfg,separators=(',',':'))))
# Apply landing pages: one template, three audiences. Women + men are ad only pages; `apply` is the
# gender neutral one for Instagram bios and Google. The gym comes from ?gym=windsor|chelsea.
APPLY={'apply':('all','Apply for the 21 Day Strength Reset | RTB Gym','Stronger and leaner with zero cardio. Coached strength training capped at 12, in Windsor and Chelsea Heights. Apply for the 21 Day Strength Reset.'),
 'apply-women':('women','Apply for the 21 Day Strength Reset | RTB Gym','Leaner, tighter and twice as strong with zero cardio. Coached strength training for women, capped at 12. Apply for the 21 Day Strength Reset.'),
 'apply-men':('men','Apply for the 21 Day Strength Reset | RTB Gym','Stronger, leaner and built to last with zero cardio. Coached strength training for men, capped at 12. Apply for the 21 Day Strength Reset.')}
tpl=(src/'_apply.tpl.html').read_text()
sources=[(f.name.replace('.src.html',''),f.read_text()) for f in sorted(src.glob('*.src.html'))]
# 30 Oct 2026 (Josh): the classic page is now THE landing page on every lead source URL. The old quiz page lives on at
# apply-quiz / apply-quiz-women / apply-quiz-men (noindex) for rollback or a future test.
sources=[s for s in sources if s[0]!='reset-chelsea']  # reset-chelsea.src.html kept for history; classic replaces it
sources+=[(pg.replace('apply','apply-quiz',1),tpl.replace('__G__',g).replace('__T__',t).replace('__D__',d)) for pg,(g,t,d) in APPLY.items()]
# Classic pages (30 Oct 2026): the May to Aug Squarespace 21 day page rebuilt. 1 Nov 2026 (Josh): calendar first again,
# no quiz in front of it. Uses the apply template's styles only (sticky bar etc).
CLASSIC={'apply':('all',''),'apply-women':('women',''),'apply-men':('men',''),'reset-chelsea':('all','chelsea')}  # page: (audience, default gym)
# V2 pages (1 Nov 2026): Undeniable workshop page structure with RTB content. Visitors reach them only through the AP05 redirect.
V2={'apply-v2':('all',''),'apply-v2-women':('women',''),'apply-v2-men':('men',''),'reset-chelsea-v2':('all','chelsea')}
V2_COPY={
 'all':{'bar':'For anyone in Windsor &amp; Chelsea Heights who wants to get <b>strong</b>. Small group coaching.',
        'h1':'Stronger and leaner in <span class="hl">21 days</span>. With a coach on every rep.',
        'faqq':'Will I lose my fitness without cardio?','faqa':'Strength work gets your heart going. Most members say daily life feels easier within weeks.'},
 'women':{'bar':'For anyone in Windsor &amp; Chelsea Heights who wants to get <b>strong</b>. Small group coaching.',
        'h1':'Stronger, leaner and more confident in <span class="hl">21 days</span>.',
        'faqq':'Will lifting make me bulky?','faqa':'No. Building real size takes years of eating and training for it. In 21 days you get stronger, firmer and more confident.'},
 'men':{'bar':'For anyone in Windsor &amp; Chelsea Heights who wants to get <b>strong</b>. Small group coaching.',
        'h1':'Stronger, leaner and built to last. <span class="hl">21 days</span> to prove it.',
        'faqq':'Will I lose my fitness without cardio?','faqa':'Strength work gets your heart going. Most members say daily life feels easier within weeks.'}}
V2_YES={'all':['You want to get stronger and leaner without living on a treadmill','You want someone to tell you exactly what to do and check you do it right',
  "You've worked hard before and want to finally see it show",'You like a small group, not a packed class of 40','You can train 2 to 5 times a week for 21 days',"You're coachable and ready to follow a plan"],
 'women':['You want to look toned and feel strong, not just smaller','You want someone to tell you exactly what to do and check you do it right',
  "You've done the classes and the cardio and want to finally see it show",'You like a small group, not a packed class of 40','You can train 2 to 5 times a week for 21 days',"You're coachable and ready to follow a plan"],
 'men':['You want to get strong and drop the gut without endless cardio','You want a coach checking your form so you lift heavy without getting hurt',
  "You've trained on and off for years and want a plan that actually adds up",'You like a small group, not a packed class of 40','You can train 2 to 5 times a week for 21 days',"You're coachable and ready to follow a plan"]}
c_style=tpl[:tpl.index('</style>')+8]
CAL_ID='8KzUE6BBWRni8g9f0wd5'
def cal_block(gym,dark):
    q='?which_location_are_you_interested_in=Chelsea+Heights' if gym=='chelsea' else ''
    h='color:#fff' if dark else ''
    return f'''<div id="apply" class="calbox"><div class="wrap">
    <h2 style="text-align:center;{h}">Pick a time for your free call.</h2>
    <p class="lede" style="text-align:center;margin:16px auto 0;{'color:#ccc' if dark else ''}">15 minutes with the RTB team. Your goals, your times, and whether the Reset fits. No hard sell.</p>
    <div class="card" style="background:#fff;border-radius:12px;padding:8px;margin:32px auto 0;max-width:900px"><div id="calwrap"><iframe src="https://grow-api.hapana.com/widget/booking/{CAL_ID}{q}" allow="payment" scrolling="no" title="Book your free call" id="{CAL_ID}_page"></iframe></div></div>
  </div></div>'''
CAL_JS='''<script>
(function(){
if(!window._rtbEmbed){window._rtbEmbed=1;var s=document.createElement('script');s.src='https://grow-api.hapana.com/js/form_embed.js';document.body.appendChild(s)}
var box=document.getElementById('apply'),cal=box.querySelector('iframe');
/* Clicks inside the calendar can't be seen; the page losing focus to it is the tell. Counts as starting the booking. */
addEventListener('blur',function(){setTimeout(function(){if(document.activeElement===cal&&window.LAB)LAB.ev('form_start',{src:'calendar'})},0)});
/* Hide the sticky bar while the calendar is on screen. */
if('IntersectionObserver' in window)new IntersectionObserver(function(es){document.body.classList.toggle('inapply',es[0].isIntersecting)},{threshold:0.05}).observe(box);
})();
</script>
'''
cb=(src/'_classic.body.html').read_text()
for pg,(g,gym) in CLASSIC.items():
    body='<!-- title:21 Day Strength Reset | RTB Gym|desc:Coached strength training capped at 12 in Windsor and Chelsea Heights. 21 days, $150, all inclusive. -->\n'+c_style+cb.replace('<!--APPLY-->',cal_block(gym,True))+CAL_JS
    sources.append((pg,body))
vb=(src/'_v2.body.html').read_text()
for pg,(g,gym) in V2.items():
    b=vb.replace('<!--CAL-->',cal_block(gym,True)).replace('{{yes}}',''.join(f'<li>{x}</li>' for x in V2_YES[g]))
    for k,v in V2_COPY[g].items(): b=b.replace('{{'+k+'}}',v)
    sources.append((pg,'<!-- title:21 Day Strength Reset | RTB Gym|desc:Coached strength training capped at 12 in Windsor and Chelsea Heights. 21 days, $150, all inclusive. -->\n'+c_style+b+CAL_JS))
for page,body in sources:
    m=re.search(r'<!--\s*title:(.*?)\|desc:(.*?)-->',body,re.S)
    title=m.group(1).strip() if m else 'RTB Gym'; desc=m.group(2).strip() if m else ''
    out=head.replace('__TITLE__',title).replace('__DESC__',desc).replace('__PAGE__',page)+body+foot
    QUIZ=['apply-quiz'+k[5:] for k in APPLY]
    if page=='reset' or page in QUIZ or page in CLASSIC or page in V2 or page.startswith('reset-') or page.startswith('experience-'):  # ad landing page: no way off the page except booking
        out=re.sub(r'<a href="index.html">(<img class="logo"[^>]*>)</a>',r'\1',out)
        out=re.sub(r'\s*<button class="burger".*?</button>','',out,flags=re.S)
        out=re.sub(r'\s*<div class="links">.*?</div>','',out,count=1,flags=re.S)
        if page in CLASSIC or page in V2:
            out=out.replace('href="apply.html#apply"','href="#apply"').replace('href="apply.html"','href="#apply"')
            if page in V2: out=out.replace('<nav class="nav" id="nav">','<nav class="nav" id="nav">\n  <div class="qbar">'+V2_COPY[V2[page][0]]['bar']+'</div>',1)
            if page!='apply': out=out.replace('<meta property="og:type"','<meta name="robots" content="noindex">\n<meta property="og:type"',1)
        if page in QUIZ:
            out=out.replace('<a class="cta" href="apply.html#apply">Book a free call</a>','<a class="cta" href="#apply">Explore my options</a>')
            out=out.replace('href="apply.html#apply"','href="#apply"').replace('href="apply.html"','href="#apply"')
            if page!='apply': out=out.replace('<meta property="og:type"','<meta name="robots" content="noindex">\n<meta property="og:type"',1)
        out=out.replace('href="reset.html#book"','href="#book"')
        if (page.startswith('reset-') or page.startswith('experience-')) and page not in CLASSIC and page not in V2:  # gym specific ad pages (22 Oct 2026): ad only, every CTA stays on the page
            out=out.replace('<meta property="og:type"','<meta name="robots" content="noindex">\n<meta property="og:type"',1)
            out=out.replace('href="apply.html#apply"','href="#book"').replace('href="apply.html"','href="#book"')
            if page.startswith('experience-'): out=out.replace('>Book a free call</a>','>Claim your free pass</a>')  # free pass page, no call
        f0,f1=out.index('<footer>'),out.index('</footer>')+9
        ft=out[f0:f1]
        ft=re.sub(r'\s*<div>\s*<h4>Start here</h4>.*?</div>','',ft,flags=re.S)
        ft=re.sub(r'<li><a [^>]*>.*?</a></li>\s*','',ft)
        ft=re.sub(r' &middot; <a [^>]*>.*?</a>','',ft)
        out=out[:f0]+ft+out[f1:]
    if page.startswith('bf-'): out=out.replace('<meta property="og:type"','<meta name="robots" content="noindex">\n<meta property="og:type"',1)  # Black Friday 2026 email pages, not for Google
    if page=='index': out=out.replace('https://rtbgym.com.au/index.html','https://rtbgym.com.au/')
    if page=='reset':  # 6 Oct 2026: the neutral apply page replaced the old 21 Day Reset page. The URL stays alive as a redirect for old ads, bios and Google.
        out='<!DOCTYPE html><html><head><meta charset="utf-8"><title>21 Day Strength Reset | RTB Gym</title><link rel="canonical" href="https://rtbgym.com.au/apply.html"><meta http-equiv="refresh" content="0;url=/apply.html"><script>location.replace("/apply.html"+location.search+(location.hash==="#book"?"#apply":location.hash))</script></head><body><a href="/apply.html">Continue to the 21 Day Strength Reset</a></body></html>'
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
