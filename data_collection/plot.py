import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

os.chdir(os.path.dirname(__file__))

# Read CSV
df = pd.read_csv('asset/0524-1614.csv') 

# Filter for stop=7
df = df[df['stop']==7]
df = df.reset_index(drop=True) 

x = np.arange(0, len(df))

# Plot
fig, ax = plt.subplots()

ax.plot(x, df['eta1'], label='eta of 1st next minibus')
ax.plot(x, df['eta2'], label='eta of 2nd next minibus') 
ax.plot(x, df['eta3'], label='eta of 3rd next minibus')

plt.axvline(x=df[df['time']==161706].index, color='r', linestyle='--')
plt.axvline(x=df[df['time']==163504].index, color='r', linestyle='--')
plt.axvline(x=df[df['time']==164501].index, color='r', linestyle='--')
plt.axvline(x=df[df['time']==170100].index, color='r', linestyle='--')
plt.axvline(x=df[df['time']==171304].index, color='r', linestyle='--')
plt.axvline(x=df[df['time']==171901].index, color='r', linestyle='--')

ax.set_xlabel('time')
ax.set_ylabel('eta')
ax.legend()

plt.show()