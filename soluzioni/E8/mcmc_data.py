import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy import stats
import matplotlib.pyplot as plt
import emcee
import corner



def model_l1(params, ev):
    m, b, alpha1, e1, s1 = params
    return m*ev + b + alpha1 * np.exp(-0.5 * (ev - e1) ** 2 / s1**2)



elines = np.arange(1, 10, 0.2)
alpha1 = -5
l1 = 4.8
s1 = 0.6 #l1*0.2 #0.5

m = -0.2
b = 10

l1truth= (m, b, alpha1, l1, s1)


plt.plot(elines, model_l1(l1truth, elines))
plt.show()


sigmay_l1 = 0.6/np.sqrt( model_l1(l1truth, elines) ) #0.3

np.random.seed(1133489)
data_l1 =  model_l1(l1truth, elines) + np.random.normal(0, sigmay_l1, len(elines))

plt.errorbar(elines, data_l1, yerr=sigmay_l1, fmt='o')
plt.show()


yerr = np.ones(len(elines))*sigmay_l1

df = pd.DataFrame( data= { 'E' : elines.round(1), 'f' : data_l1.round(1), 'ferr' : yerr.round(1) })
#print(df.round(1))
print(df)

df.to_csv('absorption_line.csv', index=False)

