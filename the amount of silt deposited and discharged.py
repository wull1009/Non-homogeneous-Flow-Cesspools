import numpy as np
import pandas as pd

# 定义含泥量
p = 0.05
q = 1 - p
# 存储体积
V = []
# 存储排放量
out = []
# 存储三项价格
f = []
s = []
t = []

# for sed_hour in range(23, 24):
for sed_hour in range(12, 25):


    # 存入数据和均值
    raw_data1 = np.array(pd.read_csv('./30天.csv').values.tolist()).T
    b = raw_data1.ravel()

    raw_data2 = np.loadtxt('./24小时均值.csv')

    # 根据沉积时间设定排出量
    c = []
    for i in range(30):
        for j in range(24):
            c.append(((24-sed_hour)/24*p+q)*raw_data2[j])
    # 建模

    a = [0] * 720
    # 创建list d用于存入各个小时的体积，取最大值
    d = []
    sm = []
    sed = 0
    sedi = []
    for i in range(720):
        if i < sed_hour - 1:
            a[i] = b[i]
        else:
            a[i] = b[i]
            # 判断a第一个非零值的角标
            x = np.nonzero(a)
            index = x[0][0]
            while c[i - sed_hour] > 0:
                if i - index >= 24:
                    if q * a[index] > c[i - sed_hour]:
                        a[index] = (q * a[index] - c[i - sed_hour])/q
                        sed = sed + p*c[i - sed_hour]
                        c[i - sed_hour] = 0
                    else:
                        c[i - sed_hour] = c[i - sed_hour] - q * a[index]
                        sed = sed + p * a[index]
                        a[index] = 0
                        index = index + 1
                else:
                    pp = ((i - index) / 24) * p
                    qq = 1 - pp
                    if qq * a[index] > c[i - sed_hour]:
                        a[index] = (qq * a[index] - c[i - sed_hour]) / qq
                        sed = sed + pp * c[i - sed_hour]
                        c[i - sed_hour] = 0
                    else:
                        c[i - sed_hour] = c[i - sed_hour] - qq * a[index]
                        sed = sed + pp * a[index]
                        a[index] = 0
                        index = index + 1
        d.append(sum(a) + sed)
        sm.append(sum(a))
        sedi.append(sed)

    print('沉积小时=' + str(sed_hour) + '时容积为：' + str(max(d)))
    V.append(max(d))
    print(' 沉积了：' + str(sed))
    print(' 排出了：' + str(p * sum(b) - sed))
    out.append(p * sum(b) - sed)
    # 设计容积多25%
    Q = 1.25 * max(d)
    print('设计容积：' + str(Q))
    # 均流池深度为10m
    l = (700*10/3*Q/10/(500*10/3)) ** 0.5
    w = Q/10/l
    S = 340*l*w + 250*10/3*(2*l+w)+450*10/3*w
    T = 0.25 * sed
    X = 1.5 * (p * sum(b) - sed)
    f.append(60 * X)
    t.append(60 * T)
    s.append(S)
    # print('l的长度：' + str(l))
    # print('w的长度：' + str(w))
    # print('造价：' + str(S))
    # print('修价：' + str(X))
    # print('掏价：' + str(T) + '\n')
    print('和：' + str(60 * T+60 * X+S) + '\n')


# print(V)
# print(out)

# dataframe = pd.DataFrame({'浆': sm, '泥': sedi})
# dataframe.to_csv("test.csv", index=False, sep=',')

dataframe = pd.DataFrame({'fix': f, 'dig': t, 'build': s})
dataframe.to_csv("test2.csv", index=False, sep=',')


