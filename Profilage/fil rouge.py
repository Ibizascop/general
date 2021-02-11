# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 15:58:19 2020

@author: ibiza
"""
import types
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sb
import lime
import lime.lime_tabular
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

data = pd.read_csv(r'C:\\Users\\ibiza\\OneDrive\\Desktop\\Data\\1.csv')


data_2 = data.drop(columns=['cigri_oar','psetmin','psetmax','number_of_RAPL_observation', 'max_amp_spec',
       'dom_perdiod', 'dom_freq', 'energy_mean', 'energy_var',
       'energy_coef_var', 'auto_correlation', 'significance_level','start_time_oar','stop_time_oar','job_type_oar','nb_resources'])
data_2.head()



print(sb.pairplot(data_2,))
print(data_2.corr()["total_energy_consumption"])
hist = plt.hist(data_2["total_energy_consumption"])


def fonction_decoupage(x) :
    if x <= 2.86576685e+09 :
        return 0
    elif x <= 1.82064049e+11: 
        return 1
    elif x <= 3.61262332e+11: 
        return 2
    elif x <= 5.40460614e+11: 
        return 3
    elif x <= 7.19658896e+11: 
        return 4
    elif x <= 8.98857179e+11: 
        return 5
    elif x <= 1.07805546e+12: 
        return 6
    elif x <= 1.25725374e+12: 
        return 7
    elif x <= 1.43645203e+12: 
        return 8
    elif x <= 1.61565031e+12: 
        return 9
    else : 
        return 10
data_2["Catégorie_consommation"] = data_2["total_energy_consumption"].apply(fonction_decoupage)
data_2.head()

data_3 = data_2.drop(columns=["total_energy_consumption"])


#OneHotEncoding
features_to_encode = ["job_id","host_oar","processor","job_user_oar","resource_ids_oar"]
                      
myEncoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
data_3_encoded = pd.DataFrame(myEncoder.fit_transform(data_3[features_to_encode]))
data_3_encoded.columns = myEncoder.get_feature_names(features_to_encode)

data_3.drop(features_to_encode ,axis=1, inplace=True)
data_3_final= pd.concat([data_3, data_3_encoded ], axis=1)


#variables sélectionnées : 
all_inputs = data_3_final.drop(columns=['Catégorie_consommation'])
all_classes = data_3_final['Catégorie_consommation']

all_inputs.head()
all_classes.head()
    
#Préparation des données

(training_inputs,
 testing_inputs,
 training_classes,
 testing_classes) = train_test_split(all_inputs, all_classes, test_size = 0.25, 
                                     random_state=1)


#Création du modèle RandomForest
random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(training_inputs, training_classes)
random_forest_preds = random_forest.predict(testing_inputs)

print('The accuracy of the Random Forests model is :\t',metrics.accuracy_score(random_forest_preds,testing_classes))

#Explication avec Lime
Test = pd.concat([testing_classes,testing_inputs],axis=1)
predict_fn_rf = lambda x: random_forest.predict_proba(x).astype(float)
X = training_inputs.values
explainer = lime.lime_tabular.LimeTabularExplainer(X,feature_names = training_inputs.columns,class_names=['Catégorie 0','Catégorie 1','Catégorie 2',
                                                                                                          'Catégorie 3','Catégorie 4','Catégorie 5',
                                                                                                          'Catégorie 6','Catégorie 7','Catégorie 8','Catégorie 9','Catégorie 10','Catégorie 11'],kernel_width=5)

choosen_instance = testing_inputs.loc[307]
exp = explainer.explain_instance(choosen_instance, predict_fn_rf,num_features=10)
exp.show_in_notebook(show_all=False)