import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from datetime import datetime 
import sys 
np.set_printoptions(threshold=sys.maxsize)


data_users=pd.read_csv("data/oar/job_oar_sample.csv")
data_users["time_job"] =   data_users["stop_time"] - data_users["start_time"]
data_users["real_start_job"] = [datetime.fromtimestamp(int(data_users["submission_time"][i]))for i in range(len(data_users))]
data_users["real_start_job_day"] = [datetime.fromtimestamp(int(data_users["submission_time"][i])).strftime('%w') for i in range(len(data_users))]
data_users["real_start_job_hours"] = [datetime.fromtimestamp(int(data_users["submission_time"][i])).strftime('%H') for i in range(len(data_users))]
data_users["real_start_job_day_hours"] = [datetime.fromtimestamp(int(data_users["submission_time"][i])).strftime('%w:%H') for i in range(len(data_users))]
print(data_users)
users = data_users.job_user.unique()
dicts=[]
dict = {}
user_time_job_array = []
std_time_job_array = []
minis =[]
maxis = []
for user in users :
    new_data = data_users[data_users["job_user"]==user].groupby(["job_id","job_user","time_job"])
    mean_jobs_times = data_users[data_users["job_user"]== user]["time_job"].mean()
    std_jobs_times = data_users[data_users["job_user"]== user]["time_job"].std()
    mini = data_users[data_users["job_user"]== user]["time_job"].min()
    maxi = data_users[data_users["job_user"]== user]["time_job"].max()
    print(user,mean_jobs_times,std_jobs_times,mini,maxi)
    user_time_job_array.append(mean_jobs_times)
    std_time_job_array.append(std_jobs_times)
    minis.append(mini)
    maxis.append(maxi)
    jobs = list(new_data.job_id.unique())    
    dict.update({user:jobs})


print("helo")
df=pd.DataFrame(dict.items(), columns=['job_user', 'job_id'])
nb_jobs = [len(np.asarray(df[df["job_user"]==user]["job_id"])[0]) for user in users]
df["nb_jobs"] = nb_jobs
df["mean_jobs_times"] = user_time_job_array
df["std_jobs_times"] = std_time_job_array
df["mini_jobs_times"] = minis
df["maxi_jobs_times"] = maxis
print(df)


data_time_mean = data_users.groupby(['real_start_job_day_hours']).mean().reset_index()
data_time_std = data_users.groupby(["real_start_job_day_hours"]).std().reset_index()
data_time_mean["data_time_std"] = data_time_std["time_job"]

data_time_mean_count = data_time_mean
data_time_mean_count['count']=[1]*len(data_time_mean_count)
data_time_mean_count = data_time_mean_count.groupby(["real_start_job_day_hours"]).sum().reset_index()
print(data_time_mean_count["count"])
data_time_mean['count'] = data_time_mean_count["count"]*2000

print(data_time_mean)

data_time_mean.plot.bar(x="real_start_job_day_hours", y=["time_job","count"], rot=70, title="Mean times job by hours")
plt.show(block=True)

