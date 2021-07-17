from sympy import *l1 = Symbol('L1')
l2 = Symbol('L2')
a1 = Symbol('A1')
d1 = Symbol('D1')
l4 = Symbol('L4')
l5 = Symbol('L5')

T01=dh_matrix(pi,l1,0,pi)
T12=dh_matrix(pi+t1,0,a1,pi/2)
T23=dh_matrix(t2,0,l2,0)
T34=dh_matrix(t3-pi/2,0,d1,pi/2)
T45=dh_matrix(t4+pi,-l4,0,pi/2)
T56=dh_matrix(t5+pi,0,0,pi/2)
T67=dh_matrix(0,-l5,0,0)
T78=dh_matrix(t6,0,0,0)

T02=T01*T12
T03=T02*T23
T04=T03*T34
T05=T04*T45
T06=T05*T56
T07=T06*T67
T08=T07*T78
var = ""
var += "px= "T08[0,3].subs([(l1, 0.4), (l2, 0.455), (a1, 0.025), (d1, 0.035), (l4, 0.42), (l5, 0.08)])"
var += "py= "T08[1,3].subs([(l1, 0.4), (l2, 0.455), (a1, 0.025), (d1, 0.035), (l4, 0.42), (l5, 0.08)])"
var += "pz= "T08[2,3].subs([(l1, 0.4), (l2, 0.455), (a1, 0.025), (d1, 0.035), (l4, 0.42), (l5, 0.08)])"
f = open("nan.py",a)
f.write(temp)
f.close()