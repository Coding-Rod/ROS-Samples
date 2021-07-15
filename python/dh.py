import pandas as pd
import numpy as np
import clipboard
from sympy import *

df = pd.read_csv('dh_param.csv')

st = ''
st2 = ''
for i in range(len(df['theta'])):
    st += f"T{i}{i+1}=dh_matrix({df['theta'][i]},{df['d'][i]},{df['a'][i]},{df['alpha'][i]})\n"
    st2 += f'T0{i+2}=T0{i+1}*T{i+1}{i+2}\n'

st = st+'\n'+st2
print(st)
clipboard.copy(st)
print('Copied on clipboard')
