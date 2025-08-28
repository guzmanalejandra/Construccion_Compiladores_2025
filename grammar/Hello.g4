grammar Hello;

r  : 'hello' ID ;          // regla de ejemplo: 'hello' + identificador
ID : [a-z]+ ;              // identificador en minúsculas
WS : [ \t\r\n]+ -> skip ;  // ignora espacios
