import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

rng = pd.date_range('2011-01-01', periods=72, freq='D')
rng2 = pd.date_range('2011-01-01', periods=350, freq='H')
ts = pd.Series(np.random.randn(len(rng)), index=rng)
ts_2 = pd.Series(np.random.randn(len(rng2)), index=rng2)



df = pd.DataFrame(ts,columns=['col1'])

print()

f = plt.figure()
# d = df.plot()
df1 = pd.DataFrame(ts_2,columns=['teste'])

df2 = df1.combine_first(df)
df2['new_col_3'] = df2['col1'].interpolate()
df2.plot()

print(df2.head(48))
plt.show(block=True)
