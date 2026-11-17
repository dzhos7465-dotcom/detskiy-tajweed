/* Общие функции сайта. Всё хранится только в браузере ребёнка. */
(function(){
  var KEY_NAME='dt_name', KEY_PROG='dt_progress';
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

  /* текущий урок: первый открытый и не пройденный */
  function current(course){
    var ls=window.COURSES[course].lessons;
    for(var i=0;i<ls.length;i++){if(ls[i].slug&&!isDone(course,ls[i]))return ls[i];}
    return null;
  }
  function stats(course){
    var ls=window.COURSES[course].lessons;
    return {total:ls.length,done:ls.filter(function(l){return l.slug&&isDone(course,l);}).length};
  }

  window.DT={
    getName:function(){return get(KEY_NAME,'');},
    setName:function(n){set(KEY_NAME,n);},
    clearAll:function(){try{localStorage.removeItem(KEY_NAME);localStorage.removeItem(KEY_PROG);}catch(e){}},
    stepsOf:stepsOf,lessonId:lessonId,prog:prog,markStep:markStep,unmarkStep:unmarkStep,
    doneCount:doneCount,isDone:isDone,current:current,stats:stats
  };
})();
