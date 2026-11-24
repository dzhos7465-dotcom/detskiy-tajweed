"""Домашняя версия «Пробного экзамена» (один ребёнок, телефон/планшет/компьютер).
   python3 tools/build_doma_proba.py  →  proba/doma/index.html
   Данные (блок ДАННЫЕ…ЭКРАНЫ) — из proba/index.html без изменений; шаблон — tools/doma_src.html;
   отличия от шаблона (вопрос у каждого примера, варианты по виду вопроса, разбор по 19 правилам) — заменами ниже."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g = open(os.path.join(ROOT, 'proba/index.html'), encoding='utf-8').read()
a = g.index('/* ===================== ДАННЫЕ'); b = g.index('/* ===================== ЭКРАНЫ')
data = g[a:b]
face = re.search(r"@font-face\{font-family:'KFGQPC Hafs'[^}]+\}", g).group(0)
s = open(os.path.join(ROOT, 'tools/doma_src.html'), encoding='utf-8').read()

HOME = r'''const HOME={
  key:'proba_home_v1',
  title:'Пробный экзамен',
  sub:'Тренажёр · подготовка к экзамену',
  rounds:[
    {type:'q', items:R1, title:'Какое правило?', how:'Нун, мим и мадд — <b>вперемешку</b>, как на экзамене.<br>Прочитай слово вслух — и выбери правило.<br><span class="gold">★ Золотое слово</span> — <b>две звезды</b>.'},
    {type:'q', items:R2, title:'Почему?', how:'Правило уже названо.<br>Найди <b>причину</b>: какая буква пришла следом или что стоит после буквы мадда.'},
    {type:'q', items:R3, title:'Сколько тянем?', how:'Мадд — <b>сколько харакатов</b>?<br>Нун и мим — <b>есть ли гунна</b>?'},
    {type:'q', items:R4, title:'Шадда · танвин · васль', how:'Немного о первых правилах:<br>шадда, танвин, хамзатуль-васль и лям в слове '+AR('ٱللَّه')+'.'},
    {type:'q', items:R5, title:'Ловушки', how:'Два примера — правило есть <b>только в одном</b>.<br>Найди его!'},
    {type:'ay', title:'Аят целиком', how:'В аяте подсвечено слово.<br>Прочитай аят вслух — и скажи, <b>какое здесь правило</b>.'}
  ]
};'''

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    if n != cnt:
        sys.exit('не найдено/не одно (%d): %r' % (n, old[:90]))
    s = s.replace(old, new)

rep('/*DATA*/', data)
rep('/*HOME*/', HOME)
rep('/*FONTFACE*/', face)
rep('<title>/*TITLE*/</title>', '<title>Пробный экзамен — дома</title>')

# ответ и варианты — по виду вопроса (как в групповой игре)
rep("""function ansOf(s){ const it=itemOf(s); if(s.t==='tw') return it.a;
  const R=HOME.rounds[s.ri]; if(R&&R.opts==='du') return RULES[it.k].du; return it.k; }""",
    """function ansOf(s){ return itemOf(s).a; }""")
i = s.index('function optsOf(s){'); j = s.index('function nameTxt()')
s = s[:i] + r'''function optsOf(s){
  const it=itemOf(s),k=it.k;
  if(k==='split') return it.o.map((t,j)=>({k:String(j),t:AR(t)}));
  if(k==='pick') return it.o.map((t,j)=>({k:String(j),t}));
  if(k==='pickar') return it.o.map((o,j)=>({k:String(j),t:AR(o.w+(o.s?'<span class="aend">۝</span>':''))}));
  return OPTS[k].map(([kk,t])=>({k:kk,t}));
}
function optCls(k,n){ return (n>4?' many':'')+(k==='split'||k==='pickar'?' arab':'')+(/^(cz_|pick$)/.test(k)?' long':''); }
/* правило вопроса — для разбора по 19 правилам */
function rkOf(it){ if(it.rk) return it.rk; return it.k==='wasl'?'ws':it.k==='lam'?'lm':it.k+':'+it.a; }
''' + s[j:]
rep("""function revealHTML(it){ if(!it||!it.k) return ''; const R=info(it.k,it.g);
  return '<span class="chip nm">'+R.nm+'</span><span class="chip cz">'+R.cz+'</span><span class="chip du">'+R.gn+'</span>'; }""",
    """function revealHTML(it){ if(!it||!it.k) return '';
  const nm=OPTS[it.k]&&!/^(cz_|du$|gn$)/.test(it.k)?'<span class="chip nm">'+LBL(it.k,it.a)+'</span>':'';
  return nm+'<span class="chip du">'+arw(it.why)+'</span>'; }""")

# экран вопроса: вопрос у каждого примера; у «Ловушек» нет рамки со словом
rep("""      h='<div class="focus'+(letter?' letter':'')+(x.done?(x.shown?' miss':' ok'):'')+'">'+
        (it.gold?'<div class="goldtag">★ '+(letter?'Золотая буква':'Золотое слово')+' · две звезды</div>':'')+W(it)+'</div>';""",
    """      h=it.k==='pickar'?(it.gold?'<div class="goldtag solo">★ Золотой вопрос · две звезды</div>':''):'<div class="focus'+(letter?' letter':'')+(x.done?(x.shown?' miss':' ok'):'')+'">'+
        (it.gold?'<div class="goldtag">★ '+(letter?'Золотая буква':'Золотое слово')+' · две звезды</div>':'')+W(it)+'</div>';
      if(it.h) h='<div class="hint2">'+it.h+'</div>'+h;""")
rep("""    if(R.ask) h='<div class="qcap">'+R.ask+'</div>'+h;""",
    """    const q_=it.q||ASK[it.k]||''; h=it.k==='pickar'?h+'<div class="qcap big2">'+q_+'</div>':h+'<div class="qcap">'+q_+'</div>';""")
rep("""'</div><div class="opts'+(opts.length>4?' many':'')+'">'""", """'</div><div class="opts'+optCls(it.k,opts.length)+'">'""")
rep("""    M.style.setProperty('--n',Math.min(opts.length,4));""",
    """    M.style.setProperty('--n',it.k==='madd'?4:/^(cz_|pick$)/.test(it.k)?Math.min(opts.length,2):Math.min(opts.length,4));""")

# итог: разбор по 19 правилам, группами
rep("""    const per={}; ORDER.forEach(k=>per[k]={a:0,b:0});
    ids.forEach(q=>{if(q.t==='tw')return; const k=itemOf(q).k; if(!per[k])return; per[k].b++; if(G.res[q.id]&&G.res[q.id].first) per[k].a++;});""",
    """    const per={}; Object.keys(RK).forEach(k=>per[k]={a:0,b:0});
    ids.forEach(q=>{const k=rkOf(itemOf(q)); if(!per[k])return; per[k].b++; if(G.res[q.id]&&G.res[q.id].first) per[k].a++;});""")
rep("""      '<div class="rmap">'+ORDER.map(k=>{const p=per[k];const cl=p.b&&p.a===p.b?' full':(p.b&&p.a/p.b<.6?' weak':'');
        return '<div class="rm'+cl+'"><div class="t">'+info(k).nm+'</div><div class="v">'+p.a+' / '+p.b+'</div></div>';}).join('')+'</div>'+""",
    """      '<div class="qcap">Что повторить перед экзаменом</div>'+GROUPS.map(([g,ks])=>'<div class="rgrp">'+g+'</div><div class="rmap">'+ks.map(k=>{const p=per[k];const cl=p.b&&p.a===p.b?' full':(p.b&&p.a<p.b?' weak':'');
        return '<div class="rm'+cl+'"><div class="t">'+RK[k]+'</div><div class="v">'+p.a+' / '+p.b+'</div></div>';}).join('')+'</div>').join('')+""")
rep("""  const n=ORDER.length; M.style.setProperty('--n',n);""", """  const n=4; M.style.setProperty('--n',n);""")

CSS = r'''
/* ---------- Пробный экзамен (дома) ---------- */
.chip{white-space:normal;max-width:100%;line-height:1.3;}
.chip .ar{font-size:1.3em;line-height:1;}
.qcap .ar,.rm .t .ar,.rtitle .ar,.rhow .ar{font-family:var(--qf);font-size:1.2em;}
.qcap.big2{font-size:clamp(22px,5.6vw,30px);margin-top:10px;}
.opt .ar{font-family:var(--qf);font-size:1.35em;line-height:1.2;}
.opts.arab .opt{font-family:var(--qf);font-size:clamp(32px,8vw,48px);line-height:1.6;padding:4px 8px;}
.opts.arab .opt .ar{font-size:1em;}
.opts.arab .aend{font-size:.75em;color:var(--gold-deep);margin-right:.15em;}
.opts.long .opt{font-size:clamp(16px,4.2vw,20px);line-height:1.25;}
.ya{font-family:'Amiri','Noto Naskh Arabic','Times New Roman',serif;}
.hint2{font-weight:800;font-size:clamp(14px,3.8vw,18px);color:var(--gold-deep);background:#fff;border:2px solid var(--gold-soft);border-radius:999px;padding:4px 16px;}
.goldtag.solo{position:static;transform:none;display:inline-block;}
.rgrp{font-weight:800;font-size:clamp(13px,3.4vw,16px);letter-spacing:1px;text-transform:uppercase;color:var(--gold-deep);margin:8px 0 -2px;}
.rm .t{font-size:clamp(13px,3.4vw,16px);}
@media (max-width:620px){ .opts.arab{grid-template-columns:1fr 1fr;} .opts.long{grid-template-columns:1fr;} }
</style>'''
rep('</style>', CSS)

s = re.sub('ّ([ً-ِ])', lambda m: m.group(1) + 'ّ', s)
assert 'آ' not in s
out = os.path.join(ROOT, 'proba/doma/index.html')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(s)
print('ok', out, len(s))
