# Рисует картинки превью 1200×630 (assets/og/*.jpg) по данным og_pages.py.
#   python3 tools/og_make.py [папка_со_шрифтами_nunito]
# Нужны: playwright + Chrome (/usr/bin/google-chrome), Pillow; шрифт Nunito — файлы @fontsource/nunito (npm i @fontsource/nunito).
import os,sys,base64,asyncio,io
sys.path.insert(0,os.path.dirname(__file__))
from og_pages import PAGES
from playwright.async_api import async_playwright
from PIL import Image
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUN=sys.argv[1] if len(sys.argv)>1 else '/root/node_modules/@fontsource/nunito/files'
b64=lambda p:base64.b64encode(open(p,'rb').read()).decode()
FONTS=''.join("@font-face{font-family:'Nunito';font-weight:%d;src:url(data:font/woff2;base64,%s)format('woff2');unicode-range:%s}"%(w,b64(f'{NUN}/nunito-{sub}-{w}-normal.woff2'),r)
  for w in (700,800) for sub,r in (('cyrillic','U+0400-04FF'),('latin','U+0000-00FF,U+2000-206F,U+00AB,U+00BB')))
FONTS+="@font-face{font-family:'Hafs';src:url(data:font/woff2;base64,%s)format('woff2')}"%b64(ROOT+'/assets/hafs.woff2')
COL={'teal':'#1E8A80','violet':'#7A5BA6','navy':'#2C3A78','blue':'#3E8FD0','gold':'#A9822B'}
PAT="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='90' height='90'%3E%3Cg fill='none' stroke='%2314726C' stroke-width='1.6'%3E%3Crect x='22' y='22' width='46' height='46'/%3E%3Crect x='22' y='22' width='46' height='46' transform='rotate(45 45 45)'/%3E%3C/g%3E%3C/svg%3E"
def page(title,desc,badge,ar,col):
    c=COL[col]; n=len(ar.replace(' ',''))
    fs=190 if n<=4 else (150 if n<=7 else 112)
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>{FONTS}
*{{box-sizing:border-box;margin:0}}body{{width:1200px;height:630px;background:#F5F1E7;font-family:Nunito}}
.f{{position:absolute;inset:22px;background:#FCFBF7;border:3px solid #C6A24A;border-radius:28px;overflow:hidden}}
.f::before{{content:'';position:absolute;inset:0;opacity:.06;background-image:url("{PAT}")}}
.f::after{{content:'';position:absolute;inset:10px;border:1.5px solid #BFE0DC;border-radius:20px}}
.l{{position:absolute;left:70px;top:0;bottom:0;width:560px;display:flex;flex-direction:column;justify-content:center;gap:22px}}
.b{{align-self:flex-start;background:{c};color:#fff;font-weight:800;font-size:26px;border-radius:999px;padding:7px 26px}}
.t{{font-weight:800;font-size:{80 if len(title)<=12 else (72 if len(title)<=13 else 60)}px;line-height:1.02;color:#2C3A78}}
.d{{font-weight:700;font-size:29px;line-height:1.35;color:#1C2B2A;opacity:.85}}
.s{{display:flex;align-items:center;gap:14px;font-weight:800;font-size:24px;color:#A9822B;margin-top:6px}}
.s i{{width:12px;height:12px;background:#C6A24A;transform:rotate(45deg)}}
.c{{position:absolute;right:70px;top:50%;transform:translateY(-50%);width:380px;height:380px;border-radius:50%;background:#fff;
  border:4px solid #C6A24A;box-shadow:0 0 0 14px #EAF5F3,0 0 0 17px #BFE0DC;display:flex;align-items:center;justify-content:center}}
.a{{font-family:Hafs;direction:rtl;font-size:{fs}px;line-height:1.9;padding-top:.1em;background:linear-gradient(120deg,#1E8A80,#2C3A78);
  -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;white-space:nowrap}}
</style></head><body><div class="f"><div class="l"><div class="b">{badge}</div><div class="t">{title}</div><div class="d">{desc}</div>
<div class="s"><i></i>Детский таджвид</div></div><div class="c"><div class="a">{ar}</div></div></div></body></html>'''
async def main():
    async with async_playwright() as p:
        br=await p.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await br.new_page(viewport={'width':1200,'height':630})
        done=set()
        for path,(img,title,desc,badge,ar,col) in PAGES.items():
            if img in done: continue
            done.add(img)
            await pg.set_content(page(title,desc,badge,ar,col)); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(200)
            await pg.evaluate("(()=>{const a=document.querySelector('.a');let f=parseFloat(getComputedStyle(a).fontSize);while(a.scrollWidth>290&&f>40){f-=4;a.style.fontSize=f+'px';}})()")
            png=await pg.screenshot()
            Image.open(io.BytesIO(png)).convert('RGB').save(f'{ROOT}/assets/og/{img}.jpg',quality=86,optimize=True)
            print(img, os.path.getsize(f'{ROOT}/assets/og/{img}.jpg')//1024,'KB')
        await br.close()
asyncio.run(main())
