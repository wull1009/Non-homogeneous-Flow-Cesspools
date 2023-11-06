import numpy as np
import pandas as pd

raw_data1 = np.array(pd.read_csv('./30天.csv').values.tolist()).T
b = raw_data1.ravel()

raw_data2 = np.loadtxt('./24小时均值.csv')

# 根据沉积时间设定排出量
c = []
for i in range(30):
    for j in range(24):
        c.append(raw_data2[j])
a = 0
d = []
for i in range(720):
    a = a + b[i] - c[i]
    d.append(a)

e = d - min(d)
print(max(e))

dataframe = pd.DataFrame({'0': d, 'c': e, 'out': c, 'in': b})
dataframe.to_csv("test1.csv", index=False, sep=',')
