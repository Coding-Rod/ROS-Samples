#%%
import pandas as pd
import numpy as np

#%% Read csv
df = pd.read_csv('dh_param.csv')
df

# ! ////////////////////////////////// FOR KIN /////////////////////////////////e/
#%% Import libraries
f = open("base/lib.txt", "r")
joint_number = (max(df.Joint))
status = int(joint_number/2-1)
st = f.read().split('######')[status]
f.close()
print(st)

#%% Simbolic
for i in df.variable:
    try:
        st += f"{i} = Symbol('{i.upper()}')\n"
    except:
        break
st += "\n"

#%% dh_table
aux_st = ''
for i in range(len(df['theta'])):
    st += f"T{i}{i+1}=dh_matrix({df['theta'][i]},{df['d'][i]},{df['a'][i]},{df['alpha'][i]})\n"
    if i < len(df['theta'])-1:
        aux_st += f'T0{i+2}=T0{i+1}*T{i+1}{i+2}\n'
st += '\n'+aux_st
last_t = int(aux_st[-2])

# %% print inverse kin
aux_st = ''
for i,j in enumerate(['x','y','z']):
    aux_st += f'print("{j}: ")\nprint(T0{last_t}[{i},3].subs('
    aux_st += str(list(zip(df.variable.dropna(),df.value.dropna()))).replace("\n","").replace("'","")
    aux_st += '))\n'

st += '\n'+aux_st


# %% publisher
f = open("base/pub.txt", "r")
st += '\n'+f.read()
f.close()

# %% Declare joint and angles
aux_st = 'joint_msg.name = ['
for i in range(joint_number):
    aux_st += f"'joint_a{i+1}',"
aux_st += '\b]\n'
aux_st += 'angles = ['+'0.0,'*joint_number+'\b]\n'

st += '\n'+aux_st
# %% callback
f = open("base/cll.txt", "r")
st += '\n'+f.read().split('######')[status]
f.close()
# print(aux_st)

# %% T0Xn
aux_st = f"    T0{last_t}n=T0{last_t}.subs("
f = open("base/subs.txt", "r")
aux_st += f.read().split('######')[status]
f.close()
aux_st += str(list(zip(df.variable.dropna(),df.value.dropna()))).replace("\n","").replace("'","")
aux_st += '\n'
for i,j in enumerate(['x','y','z']):
    aux_st += f"    position.{j}= T08n[{i},3] #modify variable name T0Xn\n"
st += '\n'+aux_st

# %% pos publish and main
f = open("base/maf.txt", "r")
st += f.read().replace('###node_name###',df.name[0])
f.close()

#region Debug
print(st)

f = open("out/for_kin.py", "w")
f.write(st)
f.close()
#endregion Debug

# %%
