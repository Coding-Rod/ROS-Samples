#%%
import pandas as pd
import numpy as np
import os

#%% Read csv
df = pd.read_csv('dh_param.csv')
df

# ! ////////////////////////////////// FOR KIN /////////////////////////////////e/
#%% Import libraries
f = open("base/lib.txt", "r")
joint_number = int(max(df.Joint.dropna()))
if joint_number > 4:
    status = 2
else:
    status = int(joint_number/2-1)
st = f.read().split('######')[status]
f.close()
# print(st)

#%% Simbolic
for i in range(joint_number):
    st += f"t{i+1} = Symbol('t{i+1}')\n"
for i in df.variable:
    try:
        st += f"{i} = Symbol('{i.upper()}')\n"
    except:
        break
st += "\n"

#%% def dh_matrix
f = open("base/dhm.txt", "r")
st += '\n'+f.read()+'\n\n'
f.close()

#%% dh_table
aux_st = ''
for i in range(len(df['theta'])):
    st += f"T{i}{i+1}=dh_matrix({df['theta'][i]},{df['d'][i]},{df['a'][i]},{df['alpha'][i]})\n"
    if i < len(df['theta'])-1:
        aux_st += f'T0{i+2}=T0{i+1}*T{i+1}{i+2}\n'
        last_t = (i+2)
st += '\n'+aux_st


# %% print inverse kin
aux_st = ''
for i,j in enumerate(['x','y','z']):
    aux_st += f'print("p{j}= "+str(T0{last_t}[{i},3].subs('
    aux_st += str(list(zip(df.variable.dropna(),df.value.dropna()))).replace("\n","").replace("'","")
    aux_st += ')))\n'

st += '\n'+aux_st


# %% publisher
f = open("base/pub.txt", "r")
st += '\n'+f.read()
f.close()

# %% Declare joint and angles
aux_st = 'joint_msg.name = ['
for i in range(joint_number):
    aux_st += f"'joint{i+1}',"
aux_st = aux_st[:-1]+']\n'
aux_st += 'angles = ['+str('0.0,'*joint_number)[:-1]+']\n'

st += '\n'+aux_st
# %% callback
f = open("base/cll.txt", "r")
st += '\n'+f.read().split('######')[status]
f.close()
# print(aux_st)

# %% T0Xn
aux_st = f"    T0{last_t}n=T0{last_t}.subs(["
f = open("base/subs.txt", "r")
aux_st += f.read().split('######')[status]
f.close()
aux_st += str(list(zip(df.variable.dropna(),df.value.dropna())))[1:-1].replace("\n","").replace("'","")
aux_st += '])\n'
for i,j in enumerate(['x','y','z']):
    aux_st += f"    position.{j}= T0{last_t}n[{i},3] #modify variable name T0Xn\n"
st += '\n'+aux_st

# %% pos publish and main
f = open("base/maf.txt", "r")
st += f.read().replace('###node_name###',df.name[0])
f.close()

# %% Write python file
# print(st)

f = open(f"out/{df.name[0]}.py", "w")
f.write(st)
f.close()

# ! ////////////////////////////////////////////////////////////////// INVERSE KIN //////////////////////////////////////////////////////////////////
#%% Import libraries
f = open("base/ilib.txt", "r")
st = f.read() +'\n\n'
f.close()
# print(st)

#%% Simbolic
for i in range(joint_number):
    st += f"t{i+1} = Symbol('t{i+1}')\n"
st += "\n"

# %% publisher
f = open("base/ipub.txt", "r")
st += '\n'+f.read()
f.close()

# %% Declare joint and angles
aux_st = 'joint_msg.name = ['
for i in range(joint_number):
    aux_st += f"'joint{i+1}',"
aux_st = aux_st[:-1]+']\n'
aux_st += 'angles = ['+str('0.0,'*joint_number)[:-1]+']\n'

st += '\n'+aux_st+'\n'

# %% First write
f = open(f"out/{df.name[1]}.py", "w")
f.write(st)
f.close()

# %% Jacobian
# %% publisher
f = open("base/prm.txt", "r")
st = '\n'+f.read()
f.close()

st += "\nJ=Matrix([["

stx = ''
sty = ''
stz = ''
for i in range(joint_number):
    stx += f'diff(px,t{i+1}),'
    sty += f'diff(py,t{i+1}),'
    stz += f'diff(pz,t{i+1}),'
stx = stx[:-1]+'],\n          ['
sty = sty[:-1]+'],\n          ['
stz = stz[:-1]+']])\n\n'
st += stx +sty + stz
# %% Callback
st += "def callback(data): #callback function\n    target=Matrix([data.x,data.y,data.z])\n"

# %% ti matrix and for cicle
st +=f"    ti=Matrix([{str('random(),'*joint_number)[:-1]}])\n"
st +=f"    for i in range(0,iterations):\n"
# %% cp Matrix and Jsubs
st += '        cp =Matrix(['
st_aux = ''
for i in range(joint_number):
    st_aux += f"(t{i+1},ti[{i}]),"
st_aux = st_aux[:-1]
for i in ['x','y','z']:
    st += f'p{i}.subs(['+st_aux+']),'
st = st[:-1]+'])\n'
st += '        Jsubs=J.subs(['+st_aux+'])\n'
# %% e=target -cp
f = open("base/eta.txt",'r')
st += f.read() + '\n\n'
f.close()
#%% Angles
for i in range(joint_number):
    st += f'        angles[{i}] = ti[{i}]\n'

st += '\n'
# %% pub publish and main
f = open("base/imaf.txt", "r")
st += f.read().replace('###node_name###',df.name[1])
f.close()

# %% Write python file
f = open(f"out/{df.name[1]}.py", "a")
f.write(st)
f.close()
