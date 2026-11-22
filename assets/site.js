/* Общие функции сайта. Всё хранится только в браузере ребёнка. */
(function(){
  var KEY_NAME='dt_name', KEY_PROG='dt_progress', KEY_GROUP='dt_group';
  var GROUPS=null; /* {"891":{"open":5}} — сколько уроков открыто группе; грузится из assets/groups.json */
  function get(k,d){try{var v=localStorage.getItem(k);return v===null?d:JSON.parse(v);}catch(e){return d;}}
  function set(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}}

  /* шаги урока: какие есть у этого урока */
  function stepsOf(l){
    var s=[];
    if(l.video) s.push('video');
    s.push('prez','doma');
    if(l.trainer) s.push('trainer');
    return s;
  }
  function lessonId(course,l){return course+'-'+l.n;}
  function prog(){return get(KEY_PROG,{});}
  function markStep(id,step){var p=prog();p[id]=p[id]||{};p[id][step]=1;set(KEY_PROG,p);}
  function unmarkStep(id,step){var p=prog();if(p[id]){delete p[id][step];set(KEY_PROG,p);}}
  function doneCount(course,l){var p=prog()[lessonId(course,l)]||{};return stepsOf(l).filter(function(s){return p[s];}).length;}
  function isDone(course,l){return doneCount(course,l)===stepsOf(l).length;}

  /* группа ребёнка: приходит по ссылке ?g=891-k7f3q9 (номер + секретный хвост) и запоминается на устройстве */
  (function(){var m=location.search.match(/[?&]g=([^&#]+)/);if(m)set(KEY_GROUP,decodeURIComponent(m[1]));})();
  function group(){return get(KEY_GROUP,'');}
  function groupName(){return String(group()).split('-')[0];}
  /* настройки группы — только если хвост ссылки совпал с секретом группы */
  function grp(){
    var g=String(group()), i=g.indexOf('-'), name=i<0?g:g.slice(0,i), code=i<0?'':g.slice(i+1);
    var o=GROUPS&&name&&GROUPS[name]; if(!o)return null;
    return (!o.code||o.code===code)?o:null;
  }
  /* устройство учителя (на нём сохранён ключ со страницы «Для учителя») видит всё */
  function isTeacher(){try{return !!localStorage.getItem('dt_teacher_key');}catch(e){return false;}}
  function openUpTo(){var o=grp();return o?(o.open|0):0;}
  function hasGroup(){return !!grp();}
  /* урок открыт, если его файлы на сайте (slug) и учитель открыл его группе */
  function isOpen(course,l){return !!l.slug&&(isTeacher()||course!=='nulevoy'||l.n<=openUpTo());}
  /* тренажёр открыт группе? */
  function trOpen(id){if(isTeacher())return true;var o=grp();return !!(o&&o.tr&&o.tr.indexOf(id)>=0);}

  /* текущий урок: первый открытый и не пройденный */
  function current(course){
    var ls=window.COURSES[course].lessons;
    for(var i=0;i<ls.length;i++){if(isOpen(course,ls[i])&&!isDone(course,ls[i]))return ls[i];}
    return null;
  }
  function stats(course){
    var ls=window.COURSES[course].lessons;
    return {total:ls.length,done:ls.filter(function(l){return isOpen(course,l)&&isDone(course,l);}).length};
  }
  /* загрузка настроек групп (свежая, мимо кэша), затем cb() */
  function load(cb){
    var base=document.querySelector('script[src$="site.js"]').getAttribute('src').replace(/site\.js$/,'');
    var done=false;function fin(){if(!done){done=true;cb();}}
    fetch(base+'groups.json?t='+Date.now(),{cache:'no-store'}).then(function(r){return r.json();})
      .then(function(j){GROUPS=j;fin();}).catch(function(){GROUPS=GROUPS||{};fin();});
    setTimeout(function(){if(!GROUPS)GROUPS={};fin();},6000);
  }

  window.DT={
    getName:function(){return get(KEY_NAME,'');},
    setName:function(n){set(KEY_NAME,n);},
    clearAll:function(){try{localStorage.removeItem(KEY_NAME);localStorage.removeItem(KEY_PROG);}catch(e){}},
    stepsOf:stepsOf,lessonId:lessonId,prog:prog,markStep:markStep,unmarkStep:unmarkStep,
    doneCount:doneCount,isDone:isDone,current:current,stats:stats,
    group:group,groupName:groupName,hasGroup:hasGroup,openUpTo:openUpTo,isOpen:isOpen,load:load,
    trOpen:trOpen,isTeacher:isTeacher
  };
})();
