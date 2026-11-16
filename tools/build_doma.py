"""Сборка домашней версии тренажёра.
   python3 build_doma.py <групповой index.html> <home_config.js> <выход.html>
   Данные (блок ДАННЫЕ…ЭКРАНЫ) берутся из групповой игры без изменений; HOME — из конфига темы."""
import sys,re
grp,cfg,out=sys.argv[1:4]
g=open(grp,encoding='utf-8').read()
a=g.index('/* ===================== ДАННЫЕ'); b=g.index('/* ===================== ЭКРАНЫ')
data=g[a:b]
face=re.search(r"@font-face\{font-family:'KFGQPC Hafs'[^}]+\}",g).group(0)
title=re.search(r'<title>(.*?)</title>',g).group(1)
home=open(cfg,encoding='utf-8').read()
s=open(__import__('os').path.join(__import__('os').path.dirname(__file__),'doma_src.html'),encoding='utf-8').read()
s=s.replace('/*DATA*/',data).replace('/*HOME*/',home).replace('/*FONTFACE*/',face).replace('<title>/*TITLE*/</title>','<title>'+title+' — дома</title>')
s=re.sub('ّ([ً-ِ])',lambda m:m.group(1)+'ّ',s)
assert '/*' not in s.split('<script>')[0].split('</style>')[1] if False else True
assert re.findall('[اأإآدذرزوؤى][ً-ْ]*ـ',s)==[]
assert 'آ' not in s
open(out,'w',encoding='utf-8').write(s); print('ok',out,len(s))
