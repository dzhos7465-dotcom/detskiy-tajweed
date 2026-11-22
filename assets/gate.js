/* Замок для тренажёров: открыт, если учитель включил его группе ребёнка (assets/groups.json → "tr").
   Устройство учителя (с ключом) видит всё. Если настройки не загрузились — не мешаем. */
(function(){
  var m=location.pathname.match(/\/(povtor|mim|nun|madd)\/(doma\/)?(index\.html)?$/);
  if(!m)return;
  var id=m[1]+(m[2]?'-doma':'');
  var d=document.documentElement; d.style.visibility='hidden';
  function show(){d.style.visibility='';}
  try{if(localStorage.getItem('dt_teacher_key')){show();return;}}catch(e){}
  var g='';try{g=JSON.parse(localStorage.getItem('dt_group')||'""')||'';}catch(e){}
  var src=(document.currentScript&&document.currentScript.getAttribute('src'))||'../assets/gate.js';
  var base=src.replace(/gate\.js.*$/,''), home=base.replace(/assets\/$/,'');
  var done=false;
  function lock(){
    if(done)return;done=true;
    function put(){
      var c=document.createElement('div');
      c.setAttribute('style','position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;padding:24px;'+
        'background:#F4F5F7;font-family:Manrope,system-ui,sans-serif;color:#25303B;text-align:center');
      c.innerHTML='<div style="max-width:380px;background:#fff;border-radius:22px;padding:26px 22px;box-shadow:0 10px 30px rgba(40,60,90,.1)">'+
        '<div style="font-size:40px">🔒</div><div style="font-weight:800;font-size:20px;margin:8px 0">Этот тренажёр сейчас закрыт</div>'+
        '<div style="font-size:15px;color:#7D8590;line-height:1.5">Учитель откроет его для твоей группы.</div>'+
        '<a href="'+home+'" style="display:inline-block;margin-top:18px;padding:12px 18px;border-radius:14px;color:#fff;font-weight:800;'+
        'text-decoration:none;background:linear-gradient(135deg,#2BA89E,#1A7C74)">На главную</a></div>';
      document.body.appendChild(c); show();
    }
    if(document.body)put();else document.addEventListener('DOMContentLoaded',put);
  }
  function open(){if(done)return;done=true;show();}
  fetch(base+'groups.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json();}).then(function(G){
    var i=g.indexOf('-'), name=i<0?g:g.slice(0,i), code=i<0?'':g.slice(i+1), o=G[name];
    if(o&&(!o.code||o.code===code)&&o.tr&&o.tr.indexOf(id)>=0)open();else lock();
  }).catch(open);
  setTimeout(open,6000);
})();
