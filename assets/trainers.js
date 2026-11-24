/* Список тренажёров. Учитель открывает и закрывает их для каждой группы (assets/groups.json → "tr").
   kind: 'class' — командная игра на уроке (Zoom), 'home' — тренажёр для одного ребёнка дома. */
window.TRAINERS=[
  {id:'proba',     href:'proba/',     t:'Пробный экзамен',  kind:'class'},
  {id:'povtor',    href:'povtor/',    t:'Повторяем всё',    kind:'class'},
  {id:'mim',       href:'mim/',       t:'Охота за мимами',  kind:'class'},
  {id:'nun',       href:'nun/',       t:'Охота за нунами',  kind:'class'},
  {id:'madd',      href:'madd/',      t:'Охота за маддами', kind:'class'},
  {id:'mim-doma',  href:'mim/doma/',  t:'Мимы дома',        kind:'home'},
  {id:'nun-doma',  href:'nun/doma/',  t:'Нуны дома',        kind:'home'},
  {id:'madd-doma', href:'madd/doma/', t:'Мадды дома',       kind:'home'},
  {id:'proba-doma', href:'proba/doma/', t:'Пробный экзамен дома', kind:'home'}
];
