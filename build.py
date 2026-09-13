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
    (docs/(page+'.html')).write_text(out); print(f'  docs/{page}.html  {len(out)//1024} KB')
print('Built.')
