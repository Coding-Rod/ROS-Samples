# Instructions and coordinates

## Instructions

* Count cats id = 17
* Count dogs id = 18
* Compare and place on a position

## Coordinates

* place 1:  1.408028, -0.493724, 0.017920
* place 2:  0.296930, -0.839372, -1.586309
* place 3:  -0.785485, -0.395630, -3.118760
* place 4:  -0.003255, 0.900690, 1.564504
* c = d:    3.709100, -2.707660, 1.564963
* c > d:    3.371563, -0.101304, -0.001009
* c < d:    -2.642778, 0.689771, 1.564985

## Debug

* Wolrd A: c < d
* Wolrd B: void
* Wolrd C: c > d
* Wolrd D: c < d
* Wolrd E: c = d
* Wolrd F: c > d

## Explanation [Spanish]

Iniciamente , utilizo una función  para la navigación, la cual enviando una posición x, y y un yaw envia el robot aun a posición y orientción designada utilizando la conversion a cuaterniones. Seguido de ello, tengo 2 contadores, uno para perros y uno para gatos, si detecta un gato incrementa el contador de gato y por el contrario incrementa el contador de perros. Todo esto con máquina de estados de 4 estados. Finalmente, al llegar al estado 5 tiene el condicional que compara la cantidad de perros y gatos que imprime estas cantidades y envia el robot al spotlight respectivo.
