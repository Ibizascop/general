import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import os



"""dir = "cleaned_df/"
file_list = os.listdir(dir)

for i,element in enumerate(file_list) :
    print(i)
    df=pd.read_csv(dir+str(element))
    plt.plot(df["engergy"])
    plt.title(str(element))
    plt.savefig("./img/"+element.replace(".csv",".png"))
    plt.close()
"""

"""for i in range(1,26):
    series = pd.read_csv("centroid_class_"+str(i)+".csv")
    plt.plot(series)
    plt.show()"""

list_R  = np.array(pd.read_csv("res.csv")["x"])
elements = os.listdir("../classes")
Mat = {}
for element in elements :
    new_mat = []
    dirs = os.listdir("../classes/"+element)
    for dir in dirs :
        if dir[-3 :] == "png" :
            new_mat.append(int(dir.replace(".png","")))
    Mat[int(element.replace("class_",""))] = new_mat


matrix= np.zeros((18,18))
for key, value in Mat.items():
    for num in value :
        print(key,num,list_R[num-1]-1)
        matrix[key-1,list_R[num-1]-1] = matrix[key-1,list_R[num-1]-1] + 1

print(matrix)

import itertools
import sys

import munkres
import numpy as np
import seaborn as sn 

def permute_cols(a, inds):
    """
    Permutes the columns of matrix `a` given
    a list of tuples `inds` whose elements `(from, to)` describe how columns
    should be permuted.
    """

    p = np.zeros_like(a)
    for i in inds:
        p[i] = 1
    return np.dot(a, p)

def maximize_trace(a):
    """
    Maximize trace by minimizing the Frobenius norm of 
    `np.dot(p, a)-np.eye(a.shape[0])`, where `a` is square and
    `p` is a permutation matrix. Returns permuted version of `a` with
    maximal trace.
    """

    assert a.shape[0] == a.shape[1]
    d = np.zeros_like(a)
    n = a.shape[0]
    b = np.eye(n, dtype=int)
    for i, j in itertools.product(range(n), range(n)):
        d[j, i] = sum((b[j, :]-a[i, :])**2)
    m = munkres.Munkres()
    inds = m.compute(d)
    return permute_cols(a, inds)

new_m = maximize_trace(matrix)

print(new_m)

plt.figure(figsize = (10,7))
sn.heatmap(new_m, annot=True)
plt.show()