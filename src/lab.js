/* RTB landing page lab (29 Oct 2026). Loaded in <head> on every page, before the page's own script.
   1. Splits visitors between experiment variants (sticky per browser) and exposes window.LAB.
   2. Records behaviour: view, scroll depth, sections reached, 15s engaged, CTA clicks, leave (time + how far).
   No names, emails or phones ever go through here. Events go to the `lab` Supabase function.
   Preview any variant: ?lab=AP01:B (never logged). Local test logging: localhost + ?labtest=1.
   Experiments live in src/experiments.json; build.py injects them below. */
(function(){
var CFG=__LAB_CFG__;
var L=location, P=new URLSearchParams(L.search);
var page=(L.pathname.replace(/\/index\.html$/,'/').replace(/\.html$/,'').replace(/^\/|\/$/g,'')||'index').split('/').pop();
var LIVE=/(^|\.)rtbgym\.com\.au$/.test(L.hostname), LOCAL=L.hostname==='localhost';
var BOT=navigator.webdriver||/bot|crawl|spider|slurp|facebookexternalhit|lighthouse|headless|preview/i.test(navigator.userAgent);
var uuid=function(){return crypto.randomUUID?crypto.randomUUID():'xxxxxxxx-xxxx-4xxx-8xxx-xxxxxxxxxxxx'.replace(/x/g,function(){return(Math.random()*16|0).toString(16)})};
var rnd=function(){if(window.crypto&&crypto.getRandomValues){var a=new Uint32Array(1);crypto.getRandomValues(a);return a[0]/4294967296}return Math.random()};

var S={};
try{S=JSON.parse(localStorage.getItem('rtb_lab')||'{}')}catch(e){}
if(!S.vid) S={vid:uuid(),a:{}};
if(P.get('labstaff')==='1') S.staff=1;  /* Josh / staff browsers: still logged, but flagged test so they never count */
S.a=S.a||{};
var save=function(){try{localStorage.setItem('rtb_lab',JSON.stringify(S))}catch(e){}};

/* Forced variants for previews: ?lab=AP01:B,AP02:A */
var FORCE={}, PREVIEW=false;
(P.get('lab')||'').split(',').forEach(function(x){var m=x.split(':');if(m[0]&&m[1]){FORCE[m[0]]=m[1];PREVIEW=true}});

var mine=CFG.exps.filter(function(x){return x.pages.indexOf(page)>-1});
var assign={}, shown={}, copy={}, html={}, flags={};
mine.forEach(function(x){
  var names=Object.keys(x.variants), v=FORCE[x.id];
  if(!v||!x.variants[v]){
    if(x.status!=='live'){v=null}
    else if(S.a[x.id]&&x.variants[S.a[x.id]]){v=S.a[x.id]}
    else{
      var w=names.map(function(n){return x.variants[n].weight||1}), tot=w.reduce(function(a,b){return a+b},0), r=rnd()*tot;
      for(var i=0;i<names.length;i++){r-=w[i];if(r<0){v=names[i];break}}
      v=v||names[0]; S.a[x.id]=v;
    }
  }
  if(!v) return;
  shown[x.id]=v;
  if(!FORCE[x.id]) assign[x.id]=v;
  var vv=x.variants[v];
  for(var k in vv.copy||{}) copy[k]=vv.copy[k];
  for(var s in vv.html||{}) html[s]=vv.html[s];
  for(var f in vv.flags||{}) flags[f]=vv.flags[f];
});
save();

/* Whole page tests: a variant can send this page's visitors to another page (e.g. apply-women -> reset-classic-women).
   Runs before the Meta pixel in the head, so the visitor is counted once, on the page they actually see. */
for(var id in shown){
  var rd=((CFG.exps.filter(function(x){return x.id===id})[0]||{}).variants||{})[shown[id]];
  rd=rd&&rd.redirect&&rd.redirect[page];
  if(rd){window.LAB={redirecting:true,assign:assign,copy:{},flags:{},tag:'',ev:function(){}};L.replace('/'+rd+'.html'+L.search+L.hash);return}
}

/* Static page swaps: hide the targets until the new copy is in, so nobody sees the old headline flash. */
var sels=Object.keys(html);
if(sels.length){
  var st=document.createElement('style');st.id='lab-wait';st.textContent=sels.join(',')+'{visibility:hidden}';
  document.head.appendChild(st);
  var swap=function(){sels.forEach(function(s){document.querySelectorAll(s).forEach(function(el){el.innerHTML=html[s]})});var w=document.getElementById('lab-wait');if(w)w.remove()};
  document.readyState==='loading'?document.addEventListener('DOMContentLoaded',swap):swap();
  setTimeout(function(){var w=document.getElementById('lab-wait');if(w)w.remove()},1500);
}

/* ---------- behaviour logging ---------- */
var ON=!BOT&&((LIVE&&!PREVIEW)||(LOCAL&&P.get('labtest')==='1'));
var utm={};['source','medium','campaign','content'].forEach(function(k){var v=P.get('utm_'+k);if(v)utm[k]=v});
var Q=[], sid=null, t0=Date.now(), vis=0, lastVis=document.visibilityState==='visible'?Date.now():0;
var maxScroll=0, maxSec=0, fired={};
var secs=function(){return Math.round((vis+(lastVis?Date.now()-lastVis:0))/100)/10};
function flush(){
  if(!ON||!Q.length) return;
  var body=JSON.stringify({vid:S.vid,sid:sid,page:page,assign:S.a,utm:utm,mobile:matchMedia('(max-width:760px)').matches,test:!LIVE||!!S.staff,ev:Q.splice(0,25)});
  try{if(navigator.sendBeacon&&navigator.sendBeacon(CFG.api,new Blob([body],{type:'text/plain'}))) return}catch(e){}
  try{fetch(CFG.api,{method:'POST',body:body,keepalive:true,headers:{'content-type':'text/plain'}})}catch(e){}
}
var timer=null;
function ev(n,p,once){
  if(once){if(fired[n+(p&&p.k||'')])return;fired[n+(p&&p.k||'')]=1}
  Q.push({n:n,p:p||{}});
  if(window.clarity&&/^(cta|form_start|contact|complete|booked)$/.test(n)){clarity('event',n);if(n==='contact')clarity('upgrade','applied')}
  if(!ON&&LOCAL) console.log('[lab]',n,p||{});
  clearTimeout(timer);timer=setTimeout(flush,2000);
}

ev('view',{ref:(document.referrer.split('/')[2]||'').slice(0,40),w:innerWidth});

function onScroll(){
  var h=document.documentElement.scrollHeight-innerHeight;
  var pct=h>0?Math.min(100,Math.round(scrollY/h*100)):100;
  if(pct>maxScroll){maxScroll=pct;[25,50,75,90].forEach(function(t){if(pct>=t)ev('scroll',{k:t,pct:t},true)})}
}
addEventListener('scroll',onScroll,{passive:true});

/* Sections reached, numbered top to bottom (1 = hero). Tells us where people stop reading. */
function watchSections(){
  var list=[].slice.call(document.querySelectorAll('body > section, main > section'));
  if(!('IntersectionObserver' in window)||!list.length) return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;
    var i=list.indexOf(e.target)+1;if(i>maxSec)maxSec=i;
    ev('section',{k:i,sec:i,id:(e.target.id||'').slice(0,30)},true);io.unobserve(e.target)})},{threshold:0.35});
  list.forEach(function(s){io.observe(s)});
}
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',watchSections):watchSections();

var eng=setInterval(function(){if(secs()>=15){ev('engaged',{secs:15},true);clearInterval(eng)}},1000);

document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a.cta,[data-cta],button.cta,.sticky a');if(!a) return;
  ev('cta',{id:(a.dataset.cta||a.textContent||'').trim().slice(0,30),sec:maxSec,secs:secs()});flush();
},true);

function leave(){ev('leave',{secs:secs(),scroll:maxScroll,sec:maxSec});flush()}
document.addEventListener('visibilitychange',function(){
  if(document.visibilityState==='hidden'){if(lastVis){vis+=Date.now()-lastVis;lastVis=0}leave()}
  else lastVis=Date.now();
});
addEventListener('pagehide',leave);

/* Page hooks: LAB.ev('form_start'|'contact'|'complete'|'booked'), LAB.sid = apply id, LAB.copy = copy overrides. */
var tag=Object.keys(S.a).filter(function(k){return assign[k]}).map(function(k){return k+'-'+S.a[k]}).join(',');
window.LAB={page:page,assign:assign,copy:copy,flags:flags,tag:tag,preview:PREVIEW,ev:function(n,p){ev(n,p,true)},set sid(v){sid=v}};
addEventListener('load',function(){if(window.clarity)for(var k in assign)clarity('set',k,assign[k])});
})();
