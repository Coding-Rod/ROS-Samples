#%%
import sympy as sym
import numpy as np
#%%
t = sym.Symbol('t')
t
#%%
R = sym.Matrix([[sym.cos(t),-sym.sin(t)],[sym.sin(t),sym.cos(t)]])
R

#%%
result = R.subs(t,3.14159265)
result
#%%
result = R.subs(t,np.pi)
result
#%%
result = R.subs(t,sym.pi)
result
#%%
R3x = sym.Matrix([[1,0,0],
                  [0,sym.cos(t),-sym.sin(t)],
                  [0,sym.sin(t),sym.cos(t)]])
R3x
# %%
R3y = sym.Matrix([[sym.cos(t),0,sym.sin(t)],
                  [0,1,0],
                  [-sym.sin(t),0,sym.cos(t)]])
R3y
# %%
R3z = sym.Matrix([[sym.cos(t),-sym.sin(t),0],
                  [sym.sin(t),sym.cos(t),0],
                  [0,0,1]])
R3z
#%%
print(R3x.det())
print(R3x.det().subs(t,sym.pi))
# %%
RR = R3x * R3y
RR
# %%
print(RR.det())
print(RR.det().subs(t,sym.pi))
#%%
RRR = R3x * R3y *R3z
RRR
# %%
print(RRR.det())
print(RRR.det().subs(t,sym.pi))
# %%
a = sym.Matrix([[2, 4, 5]])
a
# %%
a*R3x
# %%
(a*R3x).subs(t, sym.pi/2)
# %%
(a*R3x).subs(t, 6)
#%%
R5 = a * R3x *R3y *R3x *R3z *R3y
R5
# %%
R5.subs(t, sym.pi)
#%%
P=a*R3x.subs(t,sym.pi/2)*R3x.subs(t,sym.pi)*R3x.subs(t,sym.pi/2)
P