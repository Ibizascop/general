# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 08:51:14 2021

@author: ibiza
"""

#on importe les librairies
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sn 
import pandas as pd
from sklearn.metrics import mean_squared_error as mse
from scipy.optimize import minimize
from numpy.linalg import cholesky, det, lstsq
from scipy.optimize import minimize
import scipy

def changepoint_detection(ts,percent=0.05,plot=True,num_c=4):
    import ruptures as rpt
    from pyinform.blockentropy import block_entropy
    dic = {}
    length = len(ts)
    bar = int(percent*length)
    ts = np.array(ts) [bar:-bar]
    min_val = length
    model = "l1" 
    algo = rpt.Dynp(model="normal").fit(np.array(ts))
    dic = {"best":[0,length]}
    try :
        for i in range(num_c) :
            my_bkps = algo.predict(n_bkps=i)
            if plot :
                rpt.show.display(np.array(ts), my_bkps, figsize=(10, 6))
                plt.show()
            start_borne = 0
            full_entro = 0
            for borne in my_bkps :
                val = block_entropy(ts[start_borne:borne], k=1)   
                full_entro = val + full_entro
                start_borne = borne
            if full_entro == 0 :
                break
            elif full_entro < min_val :
                #print(min_val)
                #print(i,full_entro)
                min_val = full_entro
                print(my_bkps)
                dic["best"] = [0]+my_bkps
            else :
                pass 
    except Exception as e :
        print(e)
        print("Not enough point")
        return {"best":[0,length]}
    return dic

# librairies de kernels
def dist(x1,x2):
    return abs(x1-x2)

def Exponential_kernel(data,data_2,l,plot=False):
    dim = len(data)
    cov_mat = np.zeros((dim,len(data_2)))
    for i in range(dim):
        for j in range(len(data_2)):
            cov_mat[i,j]=np.exp(-(dist(data[i],data_2[j])/2*l**2))
    if plot :
        sn.heatmap(cov_mat)
        plt.show()
    return cov_mat

def ExpQuad(data,data_2,l,plot=False):
    dim = len(data)
    cov_mat = np.zeros((dim,len(data_2)))
    for i in range(dim):
        for j in range(len(data_2)):
            dista = pow(abs(data[i]-data_2[j]),2)
            cov_mat[i,j]=np.exp(-1*(dista/2*pow(l,2)))
    if plot :
        sn.heatmap(cov_mat)
        plt.show()
    return cov_mat
    
def Lin(data,data_2,c,plot=False):
    dim = len(data)
    cov_mat = np.zeros((dim,len(data_2)))
    for i in range(dim):
        for j in range(len(data_2)):
            cov_mat[i,j]=(data[i]-c)*(data_2[j]-c)
    if plot :
        sn.heatmap(cov_mat)
        plt.show()
    return cov_mat

def Periodic(data,data_2,l,sigma,p,plot=False):
    dim = len(data)
    cov_mat = np.zeros((dim,len(data_2)))
    for i in range(dim):
        for j in range(len(data_2)):
            dista = pow(np.sin(np.pi*(abs(data[i]-data_2[j]))/p),2)
            cov_mat[i,j]=sigma**2*np.exp(-2*dista/pow(l,2))
    if plot :
        sn.heatmap(cov_mat)
        plt.show()
    return cov_mat

def Constant(data,data_2,c):
    return c*np.ones((len(data),len(data_2)))

# fonction utilitaires 
def get_values(mu_s,cov_s,nb_samples=100):
    samples = np.random.multivariate_normal(mu_s,cov_s,100)
    stdp = [np.mean(samples[:,i])+1.96*np.std(samples[:,i]) for i in range(samples.shape[1])]
    stdi = [np.mean(samples[:,i])-1.96*np.std(samples[:,i]) for i in range(samples.shape[1])]
    mean = [np.mean(samples[:,i])for i in range(samples.shape[1])]
    return mean,stdp,stdi

def get_prior(mu,cov,samples=100,plot=False):
    samples = np.random.multivariate_normal(mu,cov,samples)
    if plot :
        for i in range(samples.shape[0]) :
            plt.plot(samples[i,:])
        plt.show()
    return samples
    
def plot_gs(true_data,mean,X_train,X_s,stdp,stdi,color="blue"):
    plt.figure(figsize=(32,16), dpi=100)
    plt.plot(X_s,mean,color="green",label="Predicted values")
    plt.fill_between(X_s.reshape(-1,),stdp,stdi, facecolor=color, alpha=0.2,label="Conf I")
    plt.plot(X_train,true_data,color="red",label="True data")
    plt.legend()
    
# Calcul posterior

def compute_posterior(data,y,X_s,kernel="Exponential_kernel",l=None,c=None,sigma=None,p=None): 
    mean = np.zeros((1,len(data))).reshape(-1,)
    if kernel == "ExpQuad" :
        cov = ExpQuad(data,data,l)
        cov_s = ExpQuad(data,X_s,l)
        cov_ss = ExpQuad(X_s,X_s,l)
    elif kernel == "Exponential_kernel" :
        cov = Exponential_kernel(data,data,l)
        cov_s = Exponential_kernel(data,X_s,l)
        cov_ss = Exponential_kernel(X_s,X_s,l)
    elif kernel == "Lin" :
        cov = Lin(data,data,c)
        cov_s = Lin(data,X_s,c)
        cov_ss = Lin(X_s,X_s,c)
    elif kernel =="Periodic" :
        cov = Periodic(data,data,p,sigma,l)
        cov_s = Periodic(data,X_s,p,sigma,l)
        cov_ss = Periodic(X_s,X_s,p,sigma,l)
    elif kernel == "Constant" :
        cov = Constant(data,data,c)
        cov_s = Constant(data,X_s,c)
        cov_ss = Constant(X_s,X_s,c)
    cov_1 = np.linalg.inv(cov+0.01*np.random.rand()*np.eye((len(cov))))
    mu = np.dot(np.dot(cov_s.T,cov_1),y)
    cov_f = cov_ss - np.dot(np.dot(cov_s.T,cov_1),cov_s)
    return mu,cov_f

#Preparer les données 
def prepare_data(Y_train,split=True,test_percent=0.2):
    if split :
        X_s=np.linspace(0,len(Y_train)-1,len(Y_train))
        test_size = int(test_percent*len(Y_train))
        Y_train = Y_train[:-test_size]
        Y_test = Y_train[-test_size:]
        X_train=np.linspace(0,len(Y_train)-1,len(Y_train))
        return Y_train,X_train,X_s,Y_test
    else :
        Y_train = pd.read_csv("1.csv")["x"]
        X_s=np.linspace(0,len(Y_train)+1,len(Y_train))
        X_train=np.linspace(0,len(Y_train)-1,len(Y_train))
        return Y_train,X_train,X_s
    
def Grid_Search_periodic():
    parameters_dic_periodic = {
    "p": [1,2,3,4,5,6,7,8,9,10],
    "sigma" : [1,2,3,4,5,6,7,8,9,10],
    "l": [1,2,3,4,5,6,7,8,9,10]
    }
    for l in parameters_dic_periodic["l"] :
        for sigma in parameters_dic_periodic["sigma"] :
            for p in parameters_dic_periodic["p"] :
                mu_s, cov_s = compute_posterior(X_train,Y_train,X_s,kernel="Periodic",p=p,sigma=sigma,l=l)
                param = [p,sigma,l]
                mean,stdp,stdi=get_values(mu_s,cov_s,nb_samples=10000)
                score = mse(mean[-test_size:],Y_test)
                print(score)
                if score < np.min(best_res["score"]) : 
                    best_res["parameters"]=param 
                    best_res["score"]=score
    return best_res

def cov_ll(X_train,Y_train,kernel="Exponential_kernel"):

    if kernel == "ExpQuad" :
        cov = ExpQuad(X_train,X_train,tab[0])
    elif kernel == "Exponential_kernel" :
        cov = Exponential_kernel(X_train,X_train,tab[0])
    elif kernel == "Lin" :
        cov = Lin(X_train,X_train,tab[0])
    elif kernel =="Periodic" :
        cov = Periodic(X_train,X_train,tab[0],tab[1],tab[2])
    elif kernel == "Constant" :
        cov = Constant(X_train,X_train,tab[0])
        
    def ll(tab):
        def ls(a, b):
            return lstsq(a, b, rcond=-1)[0]
        if kernel =="Periodic" :
            cov = Periodic(X_train,X_train,tab[0],tab[1],tab[2])
        elif kernel == "Exponential_kernel" :
            cov = Exponential_kernel(X_train,X_train,tab[0])
        elif kernel == "ExpQuad":
            cov = ExpQuad(X_train,X_train,tab[0])
        elif kernel == "Lin" :
            cov = Lin(X_train,X_train,tab[0])
        elif kernel == "Constant" :
            cov = Constant(X_train,X_train,tab[0])
        cov =cov + 0.01*np.random.rand()*np.eye(len(cov))
        try :
            L = scipy.linalg.cholesky(cov,lower=True)
            return np.sum(np.log(np.diagonal(L))) + 0.5 * Y_train.dot(ls(L.T, ls(L, Y_train))) + 0.5 * len(X_train) * np.log(2*np.pi)
        except Exception as e :
            return np.random.rand()*1000
    return ll

def optimize(X_train,Y_train,kernel="Periodic",num_restart=10,bounds=10,method="Nelder-Mead",disp=False):
    extremum = 1000000000
    for i in range(num_restart) :
        x,y,z = np.random.rand()*bounds,np.random.rand()*bounds,np.random.rand()*bounds
        print("Roound n° ",str(i)+"/"+str(num_restart),"started at point : ",x,y,z)
        tab = [x,y,z]
        res = minimize(cov_ll(X_train, Y_train,kernel),tab,
                       bounds=((0.1,bounds),(0.1,bounds),(0.1,bounds)),method=method,options={'disp': disp})
        if res.fun < extremum :
            p,sigma,l = res.x
        print("            score :",res.fun)
        print("            ended at point :",res.x)
    return p,sigma,l

def optimize_one(X_train,Y_train,kernel="ExpQuad",num_restart=10,bounds=10,method="Nelder-Mead",disp=False):
    extremum = 1000000000
    for i in range(num_restart) :
        x = np.random.rand()*bounds
        print("Roound n° ",str(i)+"/"+str(num_restart),"started at point : ",x)
        tab = [x]
        res = minimize(cov_ll(X_train, Y_train,kernel),tab,
                       bounds=((0.1,bounds),),method=method,options={'disp': disp})
        if res.fun < extremum :
            p = res.x
        print("            score :",res.fun)
        print("            ended at point :",res.x)
    return p






