import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng = pd.date_range('2011-02-01', periods=10, freq='H')
rng2 = pd.date_range('2011-01-01', periods=9, freq='H')
ts = pd.Series(np.random.randn(len(rng)), index=rng)
ts_2 = pd.Series(np.random.randn(len(rng2)), index=rng2)


df = pd.DataFrame(ts,columns=['col1'])
# print((ts['2011-12-01':'2012-01-01']))
print('col2' in df.keys())
#print()

f = plt.figure()
# d = df.plot()
df1 = pd.DataFrame(ts_2,columns=['teste'])
#print((df.index[1]-df.index[0]))
#print((df1.index[1]-df1.index[0]))
#print((df.index[1]-df.index[0]) > (df1.index[1]-df1.index[0]))
df2 = df1.combine_first(df)
#df2['new_col_3'] = df2['col1'].interpolate()
print(type(df2.index.values))
#print(df2.head(48))
#plt.show(block=True)
