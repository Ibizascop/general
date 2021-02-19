import numpy as np 
import pandas as pd 
import os 
import matplotlib.pyplot as plt 
from datetime import datetime 



df_data=pd.read_csv("data/oar/job_oar_sample.csv")
df_data["real_time"]=df_data["start_time"]-df_data["stop_time"]
df_data["real_time"]=df_data["start_time"]-df_data["stop_time"]
df_data["start_time_minute"]=[datetime.fromtimestamp(int(df_data["start_time"][i]))for i in range(len(df_data))]
df_data["stop_time_minute"]=[datetime.fromtimestamp(int(df_data["stop_time"][i]))for i in range(len(df_data))]
df_data_old = df_data 
#print(df_data.columns)
df_data.groupby('job_id',as_index=False)

#print(df_data)
for jb in df_data.job_id.unique():
    df_data[df_data['job_id']==jb]["job_user"] = df_data_old[df_data_old['job_id']==jb].iloc[0]


dir= "data/RAPL"
file_list = os.listdir(dir)
data_list=[]
i=0
for files in file_list :
    if i <  1 :
        df=pd.read_csv(dir+"/"+files,sep=",")
        #df["timestamp_minute"] = [datetime.fromtimestamp(int(df["timestamp_minute"][i])*60)for i in range(len(df))]
        df["pp0/package1"] = df["pp0/package1"]/pow(10,7)
        df["pp0/package2"] = df["pp0/package2"]/pow(10,7)
        #df=df[np.abs(df["pp0/package1"] - df["pp0/package1"].mean()) <= (3*df["pp0/package1"].std())]
        #df=df[np.abs(df["pp0/package2"] - df["pp0/package2"].mean()) <= (3*df["pp0/package2"].std())]
        df=df[df["pp0/package1"]>0]
        df=df[df["pp0/package2"]>0]
        df=df[np.abs(df["pp0/package1"] - df["pp0/package1"].mean()) <= (3*df["pp0/package1"].std())]
        df=df[np.abs(df["pp0/package2"] - df["pp0/package2"].mean()) <= (3*df["pp0/package2"].std())]
        df=df.sort_values(by="timestamp_minute",ascending=True)
        data_list.append(df)
        i=i+1



df_energy=pd.concat(data_list,axis=0)
hostnames = df_energy.hostname.unique()

print(df_energy)
for host in hostnames :
    sub_df=df_energy[df_energy["hostname"]==host].reset_index().sort_values(by="timestamp_minute")
    print(sub_df.timestamp_minute.max())
    print(sub_df.timestamp_minute.min())
    sub_df = sub_df.set_index("timestamp_minute")
    sub_df=sub_df.reindex(np.arange(sub_df.index.min(), sub_df.index.max() + 1,1)).fillna(0)
    #df["timestamp_minute"] = [datetime.fromtimestamp(int(df["timestamp_minute"][i])*60)for i in range(len(df))]
    plt.plot(sub_df.index,sub_df["pp0/package1"],label="premier groupe de cpu")
    plt.plot(sub_df.index,sub_df["pp0/package2"],label="deuxième groupe de cpu")
    sub_data_df=df_data[df_data["host"]==host]
    print("================================")
    print(sub_df)
    print(sub_df.describe())
    print("==================================")
    plt.legend()
    plt.title(host)
    plt.show()
        
