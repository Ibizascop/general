import numpy as np 
import tsfresh as ts 
import pandas as pd 
from tsfresh import select_features
import os 
from tsfresh.utilities.dataframe_functions import impute
from matrixprofile import *
import matplotlib.pyplot as plt 
import shutil

df=pd.DataFrame()


"""elements = os.listdir("../classes")
Mat = {}
for element in elements :
    new_mat = []
    dirs = os.listdir("../classes/"+element)
    for dir in dirs :
        if dir[-3 :] == "png" :
            new_mat.append(int(dir.replace(".png","")))
    Mat[int(element.replace("class_",""))] = new_mat"""

"""for i in range(1,797):
    x = pd.read_csv(str(i)+".csv")
    x["time"] = x.index
    x["id"] = [str(i)]*len(x)
    print(x)
    res = False
    
    df = df.append(ts.extract_features(x,column_id="id", column_sort="time"))
    df = select_features(df,res)
    print(df)

df.to_csv("features.csv")"""

"""df=pd.read_csv("features.csv")
impute(df)
y=np.zeros((1,len(df)))
for i in range(len(df)):
    for key in Mat: 
        if(i in Mat[key]): 
            y[0,i]=key

print(y.reshape(-1,1))
df = select_features(df,y.reshape(-1,1))"""



def plot_motifs(mtfs, labels, ax):

    colori = 0
    colors = 'rgbcm'
    for ms,l in zip(mtfs,labels):
        c =colors[colori % len(colors)]
        starts = list(ms)
        ends = [min(s + m,len(x)-1) for s in starts]
        ax.plot(starts, x[starts],  c +'o',  label=l)
        ax.plot(ends, x[ends],  c +'o', markerfacecolor='none')
        for nn in ms:
            ax.plot(range(nn,nn+m),x[nn:nn+m], c , linewidth=2)
        colori += 1

    ax.plot(x, 'k', linewidth=1, label="data")
    ax.legend()


"""
for i in range(1,797):
    try :
        x = np.array(pd.read_csv(str(i)+".csv")["x"])
        m=50
        mp = matrixProfile.stomp(x,m)
        mtfs ,motif_d  = motifs.motifs(x, mp, max_motifs=10)
        fig, (ax1, ax2,ax3) = plt.subplots(3,1,sharex=True,figsize=(20,10))
        ax1.plot(x)
        ax1.title.set_text("Signal réel")
        ax2.plot(mp[0])
        ax2.title.set_text("matrix profile")
        plot_motifs(mtfs, [f"{md:.3f}" for md in motif_d], ax3)
        ax3.title.set_text('Motifs')
        plt.savefig("matrix_profile_"+str(i)+"png.png", bbox_inches='tight')
    except Exception as e :
        print("Error with ",str(i))"""


elements = os.listdir("../classes")
for element in elements :
    dirs = os.listdir("../classes/"+element)
    for dir in dirs :
        if dir[-3 :] == "png" and dir[0] != "m":
            try :
                num = int(dir.replace(".png",""))
                pic = "matrix_profile_"+str(num)+"png.png"
                shutil.move("matrix_profile_"+str(num)+"png.png","../classes/"+element+"/matrix_profile_"+str(num)+".png")
            except Exception as e :
                print("Error with file ",str(num))