# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 10:30:08 2021

@author: ibiza
"""
import pandas as pd

data = pd.read_csv('Donnees.csv')
classes = pd.read_csv('Classes.csv')
data = data.join(classes["classe"])
data = data.drop(columns=['job_id','cigri_oar','psetmin','psetmax','number_of_RAPL_observation', 'max_amp_spec',
       'dom_perdiod', 'dom_freq', 'energy_mean', 'energy_var',
       'energy_coef_var', 'auto_correlation', 'significance_level','start_time_oar','stop_time_oar','job_type_oar','nb_resources'])


#Irnakat
df =data[data["job_user_oar"]=="irnakat"]

profil = df[['submission_time_oar','total_energy_consumption']]
profil.to_csv(r'C:\Users\ibiza\OneDrive\Desktop\Cours\Fil Rouge\Irnakat.csv',index=False)

#Liyub
df =data[data["job_user_oar"]=="liyub"]

profil = df[['submission_time_oar','total_energy_consumption']]
profil.to_csv(r'C:\Users\ibiza\OneDrive\Desktop\Cours\Fil Rouge\Liyub.csv',index=False)

#Hewg
df =data[data["job_user_oar"]=="hewg"]

profil = df[['submission_time_oar','total_energy_consumption']]
profil.to_csv(r'C:\Users\ibiza\OneDrive\Desktop\Cours\Fil Rouge\Hewg.csv',index=False)

#Glesur
df =data[data["job_user_oar"]=="glesur"]

profil = df[['submission_time_oar','total_energy_consumption']]
profil.to_csv(r'C:\Users\ibiza\OneDrive\Desktop\Cours\Fil Rouge\Glesur.csv',index=False)