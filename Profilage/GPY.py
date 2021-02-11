# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 10:15:27 2021

@author: ibiza
"""

import GPy
import types
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sn
import lime
import lime.lime_tabular
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
import gaussien as g

Y_train = np.array(pd.read_csv("Irnakat.csv")["total_energy_consumption"][:301]).reshape(-1,1)
X_train = np.array(pd.read_csv("Irnakat.csv")["submission_time_oar"][:301]).reshape(-1,1)

plt.plot(Y_train)

np.array(X_train).reshape(-1,1)
np.array(Y_train).reshape(-1,1)
kerns = [GPy.kern.RBF(1) ,GPy.kern.Exponential(1), GPy.kern.Matern32(1),GPy.kern.StdPeriodic(1,1), GPy.kern.Matern52(1), GPy.kern.Brownian(1), GPy.kern.Bias(1), GPy.kern.Linear(1), GPy.kern.PeriodicExponential(1), GPy.kern.White(1)]

best_models = {"ll":0,"params":0,"model":0}
for kernel in kerns :
    print(kernel)
    m = GPy.models.GPRegression(X_train,Y_train,kernel)
    m.optimize_restarts(num_restarts = 50)
    if  m.log_likelihood() > best_models["ll"] :
        best_models["ll"] = m.log_likelihood()
        best_models["params"] = m.param_array
        best_models["kernel"] = kernel
        best_models["model"] = m
print(best_models)


kernel = GPy.kern.StdPeriodic(1,1)
m = GPy.models.GPRegression(X_train,Y_train,kernel)
m.optimize_restarts(num_restarts = 50)
fig = m.plot()
print(type(m))

fig = m.plot(plot_density=True)

print(m.log_likelihood())


