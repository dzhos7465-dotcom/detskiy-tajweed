# Вписывает метатеги превью во все страницы из og_pages.py. Запускать из корня репозитория после любой пересборки:
#   python3 tools/og_apply.py
import os,re,html,sys
sys.path.insert(0,os.path.dirname(__file__))
from og_pages import BASE,PAGES
for path,(img,title,desc,*_) in PAGES.items():
    if not os.path.exists(path): print('нет файла',path); continue
    s=open(path,encoding='utf8').read()
    s=re.sub(r'\n?<!-- og -->.*?<!-- /og -->','',s,flags=re.S)
    url='' if path.startswith('nulevoy/0') else BASE+path.replace('index.html','')
    e=lambda x:html.escape(x,quote=True)
    tags=['<!-- og -->',
      '<meta name="description" content="%s">'%e(desc),
      '<meta property="og:type" content="website">',
      '<meta property="og:site_name" content="Детский таджвид">',
      '<meta property="og:title" content="%s">'%e(title),
      '<meta property="og:description" content="%s">'%e(desc),
      '<meta property="og:image" content="%sassets/og/%s.jpg">'%(BASE,img),
      '<meta property="og:image:width" content="1200">','<meta property="og:image:height" content="630">',
      '<meta property="og:locale" content="ru_RU">',
      '<meta name="twitter:card" content="summary_large_image">']
    if url: tags.insert(5,'<meta property="og:url" content="%s">'%url)
    tags.append('<!-- /og -->')
    s=re.sub(r'(</title>)',r'\1\n'+'\n'.join(tags).replace('\\','\\\\'),s,count=1)
    open(path,'w',encoding='utf8').write(s); print('ok',path)
