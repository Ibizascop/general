import numpy as np 
import pandas as pd 
import os 
import h5py
import matplotlib.pyplot as plt 
from datetime import datetime 



df_data=pd.read_csv("data/oar/job_oar_sample.csv")
df_data["real_time"]=df_data["start_time"]-df_data["stop_time"]
df_data["real_time"]=df_data["start_time"]-df_data["stop_time"]
df_data["start_time_minute"]=[datetime.fromtimestamp(int(df_data["start_time"][i])*60)for i in range(len(df_data))]
df_data["stop_time_minute"]=[datetime.fromtimestamp(int(df_data["stop_time"][i])*60)for i in range(len(df_data))]

dir= "data/RAPL"
file_list = os.listdir(dir)
data_list=[]
for files in file_list :
    df=pd.read_csv(dir+"/"+files,sep=",")
    df["timestamp_minute"] = [datetime.fromtimestamp(int(df["timestamp_minute"][i])*60)for i in range(len(df))]
    df["pp0/package1"] = df["pp0/package1"]/pow(10,6)
    df["pp0/package2"] = df["pp0/package2"]/pow(10,6)
    data_list.append(df)


df_energy=pd.concat(data_list)
hostnames = df_energy.hostname.unique()

for host in hostnames :
    sub_df=df_energy[df_energy["hostname"]==host]
    sub_data_df=df_data[df_data["host"]==host]
    plt.plot(sub_df["timestamp_minute"],sub_df["pp0/package1"],label="premier groupe de cpu")
    plt.plot(sub_df["timestamp_minute"],sub_df["pp0/package2"],label="deuxième groupe de cpu")
    plt.legend()
    plt.title(host)
    plt.show()
    
