
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ADICAO ATE ATRIBUICAO DCOLCHE DESIGUAL DIVISAO DOISPONTOS DPAREN ECOLCHE ELOGICO ENTAO EPAREN ESCREVA FIM FLUTUANTE ID IGUAL INTEIRO LEIA MAIORIGUAL MAIORQ MENORIGUAL MENORQ MULTIPLICACAO NEGACAO NUM_CIENTIFICO NUM_FLUTUANTE NUM_INTEIRO OULOGICO REPITA RETORNA SE SENAO SUBTRACAO VIRGULAprograma : lista_declaracoeslista_declaracoes : lista_declaracoes declaracao\n                         | declaracao declaracao : declaracao_variaveis\n                  | inicializacao_variaveis\n                  | declaracao_funcao\n    declaracao_variaveis : tipo DOISPONTOS lista_variaveisdeclaracao_variaveis : tipo DOISPONTOS errorinicializacao_variaveis : atribuicaolista_variaveis : lista_variaveis VIRGULA var \n                       | var\n    var : ID\n           | ID indice\n    indice : indice ECOLCHE expressao DCOLCHE\n              | ECOLCHE expressao DCOLCHE\n    indice : indice ECOLCHE error DCOLCHE\n              | ECOLCHE error DCOLCHE\n    tipo : INTEIRO\n            | FLUTUANTE\n    declaracao_funcao : tipo cabecalho \n\t\t\t\t\t\t\t\t\t\t\t\t | cabecalho\n    cabecalho : ID EPAREN lista_parametros DPAREN corpo FIM\n    lista_parametros : lista_parametros VIRGULA parametro\n\t\t\t\t\t\t\t\t\t\t\t\t| parametro\n\t\t\t\t\t\t\t\t\t\t\t\t| vazio\n    parametro : tipo DOISPONTOS ID\n\t\t\t\t\t\t\t\t |  parametro ECOLCHE DCOLCHE\n    corpo : corpo acao \n\t\t\t\t\t\t | vazio\n    acao : expressao\n\t\t\t\t\t\t| declaracao_variaveis\n\t\t\t\t\t\t| se\n\t\t\t\t\t\t| repita\n\t\t\t\t\t\t| leia\n\t\t\t\t\t\t| escreva\n\t\t\t\t\t\t| retorna\n    se : SE expressao ENTAO corpo FIM\n\t\t\t\t\t| SE expressao ENTAO corpo SENAO corpo FIM\n    se : SE error ENTAO corpo FIM\n\t\t\t\t\t| SE error ENTAO corpo SENAO corpo FIM\n    repita : REPITA corpo ATE expressao\n    atribuicao : var ATRIBUICAO expressao\n    leia : LEIA EPAREN var DPAREN\n    escreva : ESCREVA EPAREN expressao DPARENretorna : RETORNA EPAREN expressao DPAREN\n    expressao : expressao_logica\n\t\t\t\t\t\t\t\t | atribuicao\n    expressao_logica : expressao_simples\n\t\t\t\t\t\t\t\t\t\t\t\t| expressao_logica operador_logico expressao_simples\n    expressao_simples : expressao_aditiva\n\t\t\t\t\t\t\t\t\t\t\t\t | expressao_simples operador_relacional expressao_aditiva\n    expressao_aditiva : expressao_multiplicativa\n\t\t\t\t\t\t\t\t\t\t\t\t | expressao_aditiva operador_soma expressao_multiplicativa\n    expressao_multiplicativa : expressao_unaria\n\t\t\t\t\t\t\t\t| expressao_multiplicativa operador_multiplicacao expressao_unaria\n    expressao_unaria : fator\n                        | operador_soma fator\n                        | operador_negacao fator\n    operador_relacional : MENORQ\n                            | MAIORQ \n                            | IGUAL \n                            | DESIGUAL \n                            | MENORIGUAL\n                            | MAIORIGUAL\n    operador_soma : ADICAO\n\t\t\t\t\t | SUBTRACAO\n    operador_logico : ELOGICO\n                        | OULOGICO\n    operador_negacao : NEGACAO\n    operador_multiplicacao : MULTIPLICACAO\n              \t\t\t\t\t\t\t\t| DIVISAO\n    fator : EPAREN expressao DPAREN\n\t\t\t\t\t\t | var\n\t\t\t\t\t\t | chamada_funcao\n\t\t\t\t\t\t | numero\n    numero : NUM_INTEIRO\n\t\t\t\t\t\t\t| NUM_FLUTUANTE\n\t\t\t\t\t\t\t| NUM_CIENTIFICO\n    chamada_funcao : ID EPAREN lista_argumentos DPAREN\n    lista_argumentos : lista_argumentos VIRGULA expressao\n\t\t\t\t\t\t\t\t\t\t\t\t| expressao\n\t\t\t\t\t\t\t\t\t\t\t\t| vazio\n    vazio : '
    
_lr_action_items = {'$end':([2,4,5,6,9,11,12,13,16,19,21,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,51,52,53,64,65,66,67,68,87,88,89,93,94,95,96,97,112,114,],[-9,-6,-21,0,-5,-1,-4,-3,-13,-20,-2,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,-7,-8,-11,-73,-58,-15,-17,-57,-49,-55,-53,-72,-51,-14,-16,-10,-22,-79,]),'ELOGICO':([16,26,27,33,34,35,37,38,39,40,42,45,46,47,64,65,66,67,68,87,88,89,93,94,95,96,114,],[-13,59,-52,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-73,-58,-15,-17,-57,-49,-55,-53,-72,-51,-14,-16,-79,]),'ENTAO':([16,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,64,65,66,67,68,87,88,89,93,94,95,96,114,119,120,],[-13,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-73,-58,-15,-17,-57,-49,-55,-53,-72,-51,-14,-16,-79,126,127,]),'DIVISAO':([16,27,33,34,35,37,38,40,42,46,47,64,65,66,67,68,88,89,93,95,96,114,],[-13,63,-74,-56,-73,-76,-54,-12,-78,-75,-77,-73,-58,-15,-17,-57,-55,63,-72,-14,-16,-79,]),'DCOLCHE':([16,26,27,28,30,32,33,34,35,37,38,39,40,42,45,46,47,49,56,64,65,66,67,68,79,80,87,88,89,93,94,95,96,114,],[-13,-46,-52,-47,66,67,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,85,-73,-58,-15,-17,-57,95,96,-49,-55,-53,-72,-51,-14,-16,-79,]),'INTEIRO':([0,2,4,5,9,11,12,13,14,16,19,21,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,51,52,53,54,55,64,65,66,67,68,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,111,112,114,117,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[1,-9,-6,-21,-5,1,-4,-3,1,-13,-20,-2,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,-7,-8,-11,1,-83,-73,-58,-15,-17,-57,1,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,-31,-22,-79,1,-83,-83,-44,-45,-41,-43,1,1,-83,-37,-83,-39,1,1,-38,-40,]),'IGUAL':([16,27,33,34,35,37,38,39,40,42,45,46,47,64,65,66,67,68,87,88,89,93,94,95,96,114,],[-13,-52,-74,-56,-73,-76,-54,-50,-12,-78,78,-75,-77,-73,-58,-15,-17,-57,78,-55,-53,-72,-51,-14,-16,-79,]),'EPAREN':([3,15,16,17,18,26,27,28,29,31,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,58,59,60,61,62,63,64,65,66,67,68,69,70,72,73,74,75,76,77,78,83,84,87,88,89,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,110,111,113,114,115,116,117,124,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[14,43,-13,43,14,-46,-52,-47,43,-65,-74,-56,-73,43,-76,-54,-50,70,-66,-78,43,-69,-48,-75,-77,43,-42,-12,-7,-8,-11,-83,43,-67,-68,43,-70,-71,-73,-58,-15,-17,-57,43,43,-59,43,-63,-62,-60,-64,-61,43,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,115,-30,116,-83,118,-32,-35,-33,-36,43,-31,43,-79,43,43,43,43,-83,-83,-44,-45,-41,-43,43,43,-83,-37,-83,-39,43,43,-38,-40,]),'MENORQ':([16,27,33,34,35,37,38,39,40,42,45,46,47,64,65,66,67,68,87,88,89,93,94,95,96,114,],[-13,-52,-74,-56,-73,-76,-54,-50,-12,-78,72,-75,-77,-73,-58,-15,-17,-57,72,-55,-53,-72,-51,-14,-16,-79,]),'ECOLCHE':([3,16,23,40,50,66,67,82,85,86,95,96,],[15,48,56,15,15,-15,-17,56,-27,-26,-14,-16,]),'OULOGICO':([16,26,27,33,34,35,37,38,39,40,42,45,46,47,64,65,66,67,68,87,88,89,93,94,95,96,114,],[-13,60,-52,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-73,-58,-15,-17,-57,-49,-55,-53,-72,-51,-14,-16,-79,]),'ADICAO':([15,16,17,26,27,28,31,33,34,35,37,38,39,40,41,42,43,45,46,47,48,49,50,51,52,53,55,58,59,60,61,62,63,64,65,66,67,68,69,70,72,73,74,75,76,77,78,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,110,111,113,114,115,116,117,124,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[31,-13,31,-46,-52,-47,-65,-74,-56,-73,-76,-54,31,-12,-66,-78,31,-48,-75,-77,31,-42,-12,-7,-8,-11,-83,31,-67,-68,31,-70,-71,-73,-58,-15,-17,-57,31,31,-59,31,-63,-62,-60,-64,-61,31,-29,-49,-55,-53,-72,31,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,31,-31,31,-79,31,31,31,31,-83,-83,-44,-45,-41,-43,31,31,-83,-37,-83,-39,31,31,-38,-40,]),'ATE':([16,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,51,52,53,64,65,66,67,68,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,111,114,117,128,129,130,131,135,137,140,141,],[-13,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,-7,-8,-11,-73,-58,-15,-17,-57,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,-31,-79,124,-44,-45,-41,-43,-37,-39,-38,-40,]),'SUBTRACAO':([15,16,17,26,27,28,31,33,34,35,37,38,39,40,41,42,43,45,46,47,48,49,50,51,52,53,55,58,59,60,61,62,63,64,65,66,67,68,69,70,72,73,74,75,76,77,78,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,110,111,113,114,115,116,117,124,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[41,-13,41,-46,-52,-47,-65,-74,-56,-73,-76,-54,41,-12,-66,-78,41,-48,-75,-77,41,-42,-12,-7,-8,-11,-83,41,-67,-68,41,-70,-71,-73,-58,-15,-17,-57,41,41,-59,41,-63,-62,-60,-64,-61,41,-29,-49,-55,-53,-72,41,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,41,-31,41,-79,41,41,41,41,-83,-83,-44,-45,-41,-43,41,41,-83,-37,-83,-39,41,41,-38,-40,]),'DESIGUAL':([16,27,33,34,35,37,38,39,40,42,45,46,47,64,65,66,67,68,87,88,89,93,94,95,96,114,],[-13,-52,-74,-56,-73,-76,-54,-50,-12,-78,75,-75,-77,-73,-58,-15,-17,-57,75,-55,-53,-72,-51,-14,-16,-79,]),'RETORNA':([16,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,51,52,53,55,64,65,66,67,68,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,111,114,117,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[-13,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,-7,-8,-11,-83,-73,-58,-15,-17,-57,102,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,-31,-79,102,-83,-83,-44,-45,-41,-43,102,102,-83,-37,-83,-39,102,102,-38,-40,]),'SE':([16,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,51,52,53,55,64,65,66,67,68,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,111,114,117,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[-13,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,-7,-8,-11,-83,-73,-58,-15,-17,-57,110,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,-31,-79,110,-83,-83,-44,-45,-41,-43,110,110,-83,-37,-83,-39,110,110,-38,-40,]),'MULTIPLICACAO':([16,27,33,34,35,37,38,40,42,46,47,64,65,66,67,68,88,89,93,95,96,114,],[-13,62,-74,-56,-73,-76,-54,-12,-78,-75,-77,-73,-58,-15,-17,-57,-55,62,-72,-14,-16,-79,]),'MAIORIGUAL':([16,27,33,34,35,37,38,39,40,42,45,46,47,64,65,66,67,68,87,88,89,93,94,95,96,114,],[-13,-52,-74,-56,-73,-76,-54,-50,-12,-78,77,-75,-77,-73,-58,-15,-17,-57,77,-55,-53,-72,-51,-14,-16,-79,]),'MENORIGUAL':([16,27,33,34,35,37,38,39,40,42,45,46,47,64,65,66,67,68,87,88,89,93,94,95,96,114,],[-13,-52,-74,-56,-73,-76,-54,-50,-12,-78,74,-75,-77,-73,-58,-15,-17,-57,74,-55,-53,-72,-51,-14,-16,-79,]),'SENAO':([16,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,51,52,53,64,65,66,67,68,84,87,88,89,93,94,95,96,97,98,99,101,105,106,107,108,111,114,126,127,128,129,130,131,132,133,135,137,140,141,],[-13,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,-7,-8,-11,-73,-58,-15,-17,-57,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-32,-35,-33,-36,-31,-79,-83,-83,-44,-45,-41,-43,134,136,-37,-39,-38,-40,]),'FLUTUANTE':([0,2,4,5,9,11,12,13,14,16,19,21,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,51,52,53,54,55,64,65,66,67,68,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,111,112,114,117,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[10,-9,-6,-21,-5,10,-4,-3,10,-13,-20,-2,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,-7,-8,-11,10,-83,-73,-58,-15,-17,-57,10,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,-31,-22,-79,10,-83,-83,-44,-45,-41,-43,10,10,-83,-37,-83,-39,10,10,-38,-40,]),'VIRGULA':([14,16,22,23,24,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,51,53,64,65,66,67,68,70,82,85,86,87,88,89,90,91,92,93,94,95,96,97,114,121,],[-83,-13,54,-24,-25,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,81,-11,-73,-58,-15,-17,-57,-83,-23,-27,-26,-49,-55,-53,-82,-81,113,-72,-51,-14,-16,-10,-79,-80,]),'error':([15,20,48,110,],[32,52,80,120,]),'MAIORQ':([16,27,33,34,35,37,38,39,40,42,45,46,47,64,65,66,67,68,87,88,89,93,94,95,96,114,],[-13,-52,-74,-56,-73,-76,-54,-50,-12,-78,76,-75,-77,-73,-58,-15,-17,-57,76,-55,-53,-72,-51,-14,-16,-79,]),'REPITA':([16,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,51,52,53,55,64,65,66,67,68,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,111,114,117,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[-13,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,-7,-8,-11,-83,-73,-58,-15,-17,-57,103,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,-31,-79,103,-83,-83,-44,-45,-41,-43,103,103,-83,-37,-83,-39,103,103,-38,-40,]),'LEIA':([16,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,51,52,53,55,64,65,66,67,68,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,111,114,117,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[-13,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,-7,-8,-11,-83,-73,-58,-15,-17,-57,104,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,-31,-79,104,-83,-83,-44,-45,-41,-43,104,104,-83,-37,-83,-39,104,104,-38,-40,]),'NUM_INTEIRO':([15,16,17,26,27,28,29,31,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,58,59,60,61,62,63,64,65,66,67,68,69,70,72,73,74,75,76,77,78,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,110,111,113,114,115,116,117,124,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[37,-13,37,-46,-52,-47,37,-65,-74,-56,-73,37,-76,-54,-50,-12,-66,-78,37,-69,-48,-75,-77,37,-42,-12,-7,-8,-11,-83,37,-67,-68,37,-70,-71,-73,-58,-15,-17,-57,37,37,-59,37,-63,-62,-60,-64,-61,37,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,37,-31,37,-79,37,37,37,37,-83,-83,-44,-45,-41,-43,37,37,-83,-37,-83,-39,37,37,-38,-40,]),'DOISPONTOS':([1,8,10,25,109,],[-18,20,-19,57,20,]),'ESCREVA':([16,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,51,52,53,55,64,65,66,67,68,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,111,114,117,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[-13,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,-7,-8,-11,-83,-73,-58,-15,-17,-57,100,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,-31,-79,100,-83,-83,-44,-45,-41,-43,100,100,-83,-37,-83,-39,100,100,-38,-40,]),'FIM':([16,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,51,52,53,55,64,65,66,67,68,83,84,87,88,89,93,94,95,96,97,98,99,101,105,106,107,108,111,114,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[-13,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,-7,-8,-11,-83,-73,-58,-15,-17,-57,112,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-32,-35,-33,-36,-31,-79,-83,-83,-44,-45,-41,-43,135,137,-83,-37,-83,-39,140,141,-38,-40,]),'NUM_CIENTIFICO':([15,16,17,26,27,28,29,31,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,58,59,60,61,62,63,64,65,66,67,68,69,70,72,73,74,75,76,77,78,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,110,111,113,114,115,116,117,124,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[42,-13,42,-46,-52,-47,42,-65,-74,-56,-73,42,-76,-54,-50,-12,-66,-78,42,-69,-48,-75,-77,42,-42,-12,-7,-8,-11,-83,42,-67,-68,42,-70,-71,-73,-58,-15,-17,-57,42,42,-59,42,-63,-62,-60,-64,-61,42,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,42,-31,42,-79,42,42,42,42,-83,-83,-44,-45,-41,-43,42,42,-83,-37,-83,-39,42,42,-38,-40,]),'ATRIBUICAO':([3,7,16,35,40,66,67,95,96,],[-12,17,-13,17,-12,-15,-17,-14,-16,]),'ID':([0,1,2,4,5,8,9,10,11,12,13,15,16,17,19,20,21,26,27,28,29,31,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,57,58,59,60,61,62,63,64,65,66,67,68,69,70,72,73,74,75,76,77,78,81,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,110,111,112,113,114,115,116,117,118,124,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[3,-18,-9,-6,-21,18,-5,-19,3,-4,-3,40,-13,40,-20,50,-2,-46,-52,-47,40,-65,-74,-56,-73,40,-76,-54,-50,-12,-66,-78,40,-69,-48,-75,-77,40,-42,-12,-7,-8,-11,-83,86,40,-67,-68,40,-70,-71,-73,-58,-15,-17,-57,40,40,-59,40,-63,-62,-60,-64,-61,50,40,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,40,-31,-22,40,-79,40,40,40,50,40,-83,-83,-44,-45,-41,-43,40,40,-83,-37,-83,-39,40,40,-38,-40,]),'NEGACAO':([15,16,17,26,27,28,31,33,34,35,37,38,39,40,41,42,43,45,46,47,48,49,50,51,52,53,55,58,59,60,61,62,63,64,65,66,67,68,69,70,72,73,74,75,76,77,78,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,110,111,113,114,115,116,117,124,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[44,-13,44,-46,-52,-47,-65,-74,-56,-73,-76,-54,-50,-12,-66,-78,44,-48,-75,-77,44,-42,-12,-7,-8,-11,-83,44,-67,-68,44,-70,-71,-73,-58,-15,-17,-57,44,44,-59,44,-63,-62,-60,-64,-61,44,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,44,-31,44,-79,44,44,44,44,-83,-83,-44,-45,-41,-43,44,44,-83,-37,-83,-39,44,44,-38,-40,]),'DPAREN':([14,16,22,23,24,26,27,28,33,34,35,37,38,39,40,42,45,46,47,49,50,64,65,66,67,68,70,71,82,85,86,87,88,89,90,91,92,93,94,95,96,114,121,122,123,125,],[-83,-13,55,-24,-25,-46,-52,-47,-74,-56,-73,-76,-54,-50,-12,-78,-48,-75,-77,-42,-12,-73,-58,-15,-17,-57,-83,93,-23,-27,-26,-49,-55,-53,-82,-81,114,-72,-51,-14,-16,-79,-80,128,129,131,]),'NUM_FLUTUANTE':([15,16,17,26,27,28,29,31,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,58,59,60,61,62,63,64,65,66,67,68,69,70,72,73,74,75,76,77,78,83,84,87,88,89,93,94,95,96,97,98,99,101,103,105,106,107,108,110,111,113,114,115,116,117,124,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,],[47,-13,47,-46,-52,-47,47,-65,-74,-56,-73,47,-76,-54,-50,-12,-66,-78,47,-69,-48,-75,-77,47,-42,-12,-7,-8,-11,-83,47,-67,-68,47,-70,-71,-73,-58,-15,-17,-57,47,47,-59,47,-63,-62,-60,-64,-61,47,-29,-49,-55,-53,-72,-51,-14,-16,-10,-28,-34,-30,-83,-32,-35,-33,-36,47,-31,47,-79,47,47,47,47,-83,-83,-44,-45,-41,-43,47,47,-83,-37,-83,-39,47,47,-38,-40,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'fator':([15,17,29,36,43,48,58,61,69,70,73,83,110,113,115,116,117,124,132,133,138,139,],[34,34,65,68,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'expressao_logica':([15,17,43,48,70,83,110,113,115,116,117,124,132,133,138,139,],[26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,]),'acao':([83,117,132,133,138,139,],[98,98,98,98,98,98,]),'repita':([83,117,132,133,138,139,],[107,107,107,107,107,107,]),'expressao_multiplicativa':([15,17,43,48,58,69,70,73,83,110,113,115,116,117,124,132,133,138,139,],[27,27,27,27,27,89,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'leia':([83,117,132,133,138,139,],[99,99,99,99,99,99,]),'operador_negacao':([15,17,43,48,58,61,69,70,73,83,110,113,115,116,117,124,132,133,138,139,],[29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,]),'programa':([0,],[6,]),'vazio':([14,55,70,103,126,127,134,136,],[24,84,90,84,84,84,84,84,]),'expressao':([15,17,43,48,70,83,110,113,115,116,117,124,132,133,138,139,],[30,49,71,79,91,101,119,121,122,123,101,130,101,101,101,101,]),'declaracao_funcao':([0,11,],[4,4,]),'indice':([3,40,50,],[16,16,16,]),'cabecalho':([0,8,11,],[5,19,5,]),'atribuicao':([0,11,15,17,43,48,70,83,110,113,115,116,117,124,132,133,138,139,],[2,2,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,]),'lista_variaveis':([20,],[51,]),'chamada_funcao':([15,17,29,36,43,48,58,61,69,70,73,83,110,113,115,116,117,124,132,133,138,139,],[33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,]),'corpo':([55,103,126,127,134,136,],[83,117,132,133,138,139,]),'parametro':([14,54,],[23,82,]),'var':([0,11,15,17,20,29,36,43,48,58,61,69,70,73,81,83,110,113,115,116,117,118,124,132,133,138,139,],[7,7,35,35,53,64,64,35,35,64,64,64,35,64,97,35,35,35,35,35,35,125,35,35,35,35,35,]),'tipo':([0,11,14,54,83,117,132,133,138,139,],[8,8,25,25,109,109,109,109,109,109,]),'se':([83,117,132,133,138,139,],[105,105,105,105,105,105,]),'inicializacao_variaveis':([0,11,],[9,9,]),'operador_soma':([15,17,39,43,48,58,61,69,70,73,83,94,110,113,115,116,117,124,132,133,138,139,],[36,36,69,36,36,36,36,36,36,36,36,69,36,36,36,36,36,36,36,36,36,36,]),'operador_multiplicacao':([27,89,],[61,61,]),'expressao_unaria':([15,17,43,48,58,61,69,70,73,83,110,113,115,116,117,124,132,133,138,139,],[38,38,38,38,38,88,38,38,38,38,38,38,38,38,38,38,38,38,38,38,]),'lista_declaracoes':([0,],[11,]),'declaracao_variaveis':([0,11,83,117,132,133,138,139,],[12,12,111,111,111,111,111,111,]),'expressao_aditiva':([15,17,43,48,58,70,73,83,110,113,115,116,117,124,132,133,138,139,],[39,39,39,39,39,39,94,39,39,39,39,39,39,39,39,39,39,39,]),'lista_argumentos':([70,],[92,]),'lista_parametros':([14,],[22,]),'retorna':([83,117,132,133,138,139,],[108,108,108,108,108,108,]),'escreva':([83,117,132,133,138,139,],[106,106,106,106,106,106,]),'operador_logico':([26,],[58,]),'expressao_simples':([15,17,43,48,58,70,83,110,113,115,116,117,124,132,133,138,139,],[45,45,45,45,87,45,45,45,45,45,45,45,45,45,45,45,45,]),'declaracao':([0,11,],[13,21,]),'numero':([15,17,29,36,43,48,58,61,69,70,73,83,110,113,115,116,117,124,132,133,138,139,],[46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,46,]),'operador_relacional':([45,87,],[73,73,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programa","S'",1,None,None,None),
  ('programa -> lista_declaracoes','programa',1,'p_programa','yacc_tzora.py',13),
  ('lista_declaracoes -> lista_declaracoes declaracao','lista_declaracoes',2,'p_lista_declaracoes','yacc_tzora.py',22),
  ('lista_declaracoes -> declaracao','lista_declaracoes',1,'p_lista_declaracoes','yacc_tzora.py',23),
  ('declaracao -> declaracao_variaveis','declaracao',1,'p_declaracao','yacc_tzora.py',33),
  ('declaracao -> inicializacao_variaveis','declaracao',1,'p_declaracao','yacc_tzora.py',34),
  ('declaracao -> declaracao_funcao','declaracao',1,'p_declaracao','yacc_tzora.py',35),
  ('declaracao_variaveis -> tipo DOISPONTOS lista_variaveis','declaracao_variaveis',3,'p_declaracao_variaveis','yacc_tzora.py',42),
  ('declaracao_variaveis -> tipo DOISPONTOS error','declaracao_variaveis',3,'p_declaracao_variaveis_error','yacc_tzora.py',48),
  ('inicializacao_variaveis -> atribuicao','inicializacao_variaveis',1,'p_inicializacao_variaveis','yacc_tzora.py',52),
  ('lista_variaveis -> lista_variaveis VIRGULA var','lista_variaveis',3,'p_lista_variaveis','yacc_tzora.py',59),
  ('lista_variaveis -> var','lista_variaveis',1,'p_lista_variaveis','yacc_tzora.py',60),
  ('var -> ID','var',1,'p_var','yacc_tzora.py',70),
  ('var -> ID indice','var',2,'p_var','yacc_tzora.py',71),
  ('indice -> indice ECOLCHE expressao DCOLCHE','indice',4,'p_indice','yacc_tzora.py',81),
  ('indice -> ECOLCHE expressao DCOLCHE','indice',3,'p_indice','yacc_tzora.py',82),
  ('indice -> indice ECOLCHE error DCOLCHE','indice',4,'p_indice_error','yacc_tzora.py',92),
  ('indice -> ECOLCHE error DCOLCHE','indice',3,'p_indice_error','yacc_tzora.py',93),
  ('tipo -> INTEIRO','tipo',1,'p_tipo','yacc_tzora.py',99),
  ('tipo -> FLUTUANTE','tipo',1,'p_tipo','yacc_tzora.py',100),
  ('declaracao_funcao -> tipo cabecalho','declaracao_funcao',2,'p_declaracao_funcao','yacc_tzora.py',107),
  ('declaracao_funcao -> cabecalho','declaracao_funcao',1,'p_declaracao_funcao','yacc_tzora.py',108),
  ('cabecalho -> ID EPAREN lista_parametros DPAREN corpo FIM','cabecalho',6,'p_cabecalho','yacc_tzora.py',118),
  ('lista_parametros -> lista_parametros VIRGULA parametro','lista_parametros',3,'p_lista_parametros','yacc_tzora.py',125),
  ('lista_parametros -> parametro','lista_parametros',1,'p_lista_parametros','yacc_tzora.py',126),
  ('lista_parametros -> vazio','lista_parametros',1,'p_lista_parametros','yacc_tzora.py',127),
  ('parametro -> tipo DOISPONTOS ID','parametro',3,'p_parametro','yacc_tzora.py',139),
  ('parametro -> parametro ECOLCHE DCOLCHE','parametro',3,'p_parametro','yacc_tzora.py',140),
  ('corpo -> corpo acao','corpo',2,'p_corpo','yacc_tzora.py',150),
  ('corpo -> vazio','corpo',1,'p_corpo','yacc_tzora.py',151),
  ('acao -> expressao','acao',1,'p_acao','yacc_tzora.py',161),
  ('acao -> declaracao_variaveis','acao',1,'p_acao','yacc_tzora.py',162),
  ('acao -> se','acao',1,'p_acao','yacc_tzora.py',163),
  ('acao -> repita','acao',1,'p_acao','yacc_tzora.py',164),
  ('acao -> leia','acao',1,'p_acao','yacc_tzora.py',165),
  ('acao -> escreva','acao',1,'p_acao','yacc_tzora.py',166),
  ('acao -> retorna','acao',1,'p_acao','yacc_tzora.py',167),
  ('se -> SE expressao ENTAO corpo FIM','se',5,'p_se','yacc_tzora.py',181),
  ('se -> SE expressao ENTAO corpo SENAO corpo FIM','se',7,'p_se','yacc_tzora.py',182),
  ('se -> SE error ENTAO corpo FIM','se',5,'p_se_error','yacc_tzora.py',192),
  ('se -> SE error ENTAO corpo SENAO corpo FIM','se',7,'p_se_error','yacc_tzora.py',193),
  ('repita -> REPITA corpo ATE expressao','repita',4,'p_repita','yacc_tzora.py',198),
  ('atribuicao -> var ATRIBUICAO expressao','atribuicao',3,'p_atribuicao','yacc_tzora.py',205),
  ('leia -> LEIA EPAREN var DPAREN','leia',4,'p_leia','yacc_tzora.py',212),
  ('escreva -> ESCREVA EPAREN expressao DPAREN','escreva',4,'p_escreva','yacc_tzora.py',219),
  ('retorna -> RETORNA EPAREN expressao DPAREN','retorna',4,'p_retorna','yacc_tzora.py',225),
  ('expressao -> expressao_logica','expressao',1,'p_expressao','yacc_tzora.py',232),
  ('expressao -> atribuicao','expressao',1,'p_expressao','yacc_tzora.py',233),
  ('expressao_logica -> expressao_simples','expressao_logica',1,'p_expressao_logica','yacc_tzora.py',240),
  ('expressao_logica -> expressao_logica operador_logico expressao_simples','expressao_logica',3,'p_expressao_logica','yacc_tzora.py',241),
  ('expressao_simples -> expressao_aditiva','expressao_simples',1,'p_expressao_simples','yacc_tzora.py',251),
  ('expressao_simples -> expressao_simples operador_relacional expressao_aditiva','expressao_simples',3,'p_expressao_simples','yacc_tzora.py',252),
  ('expressao_aditiva -> expressao_multiplicativa','expressao_aditiva',1,'p_expressao_aditiva','yacc_tzora.py',262),
  ('expressao_aditiva -> expressao_aditiva operador_soma expressao_multiplicativa','expressao_aditiva',3,'p_expressao_aditiva','yacc_tzora.py',263),
  ('expressao_multiplicativa -> expressao_unaria','expressao_multiplicativa',1,'p_expressao_multiplicativa','yacc_tzora.py',273),
  ('expressao_multiplicativa -> expressao_multiplicativa operador_multiplicacao expressao_unaria','expressao_multiplicativa',3,'p_expressao_multiplicativa','yacc_tzora.py',274),
  ('expressao_unaria -> fator','expressao_unaria',1,'p_expressao_unaria','yacc_tzora.py',284),
  ('expressao_unaria -> operador_soma fator','expressao_unaria',2,'p_expressao_unaria','yacc_tzora.py',285),
  ('expressao_unaria -> operador_negacao fator','expressao_unaria',2,'p_expressao_unaria','yacc_tzora.py',286),
  ('operador_relacional -> MENORQ','operador_relacional',1,'p_operador_relacional','yacc_tzora.py',297),
  ('operador_relacional -> MAIORQ','operador_relacional',1,'p_operador_relacional','yacc_tzora.py',298),
  ('operador_relacional -> IGUAL','operador_relacional',1,'p_operador_relacional','yacc_tzora.py',299),
  ('operador_relacional -> DESIGUAL','operador_relacional',1,'p_operador_relacional','yacc_tzora.py',300),
  ('operador_relacional -> MENORIGUAL','operador_relacional',1,'p_operador_relacional','yacc_tzora.py',301),
  ('operador_relacional -> MAIORIGUAL','operador_relacional',1,'p_operador_relacional','yacc_tzora.py',302),
  ('operador_soma -> ADICAO','operador_soma',1,'p_operador_soma','yacc_tzora.py',307),
  ('operador_soma -> SUBTRACAO','operador_soma',1,'p_operador_soma','yacc_tzora.py',308),
  ('operador_logico -> ELOGICO','operador_logico',1,'p_operador_logico','yacc_tzora.py',313),
  ('operador_logico -> OULOGICO','operador_logico',1,'p_operador_logico','yacc_tzora.py',314),
  ('operador_negacao -> NEGACAO','operador_negacao',1,'p_operador_negacao','yacc_tzora.py',319),
  ('operador_multiplicacao -> MULTIPLICACAO','operador_multiplicacao',1,'p_operador_multiplicacao','yacc_tzora.py',324),
  ('operador_multiplicacao -> DIVISAO','operador_multiplicacao',1,'p_operador_multiplicacao','yacc_tzora.py',325),
  ('fator -> EPAREN expressao DPAREN','fator',3,'p_fator','yacc_tzora.py',330),
  ('fator -> var','fator',1,'p_fator','yacc_tzora.py',331),
  ('fator -> chamada_funcao','fator',1,'p_fator','yacc_tzora.py',332),
  ('fator -> numero','fator',1,'p_fator','yacc_tzora.py',333),
  ('numero -> NUM_INTEIRO','numero',1,'p_numero','yacc_tzora.py',344),
  ('numero -> NUM_FLUTUANTE','numero',1,'p_numero','yacc_tzora.py',345),
  ('numero -> NUM_CIENTIFICO','numero',1,'p_numero','yacc_tzora.py',346),
  ('chamada_funcao -> ID EPAREN lista_argumentos DPAREN','chamada_funcao',4,'p_chamada_funcao','yacc_tzora.py',352),
  ('lista_argumentos -> lista_argumentos VIRGULA expressao','lista_argumentos',3,'p_lista_argumentos','yacc_tzora.py',359),
  ('lista_argumentos -> expressao','lista_argumentos',1,'p_lista_argumentos','yacc_tzora.py',360),
  ('lista_argumentos -> vazio','lista_argumentos',1,'p_lista_argumentos','yacc_tzora.py',361),
  ('vazio -> <empty>','vazio',0,'p_vazio','yacc_tzora.py',381),
]
