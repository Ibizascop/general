# Inria

Objectifs compris :
================== 

- Déterminer différents profils de comsommation énergétiques lors des différents jobs   
    Classification / Clustering sur des signaux temporelles   
- Etre capable de prédire l'utilisation energétique   
    Réutilisation des différentes catégories dans le but de prédire si certain coeurs sont sous exploités afin de pouvoir regrouper les jobs qui consomment peu de ressources.
 
 - Rappel HPC : http://oar.imag.fr/docs/2.5/user/quickstart.html

Ce qui est mit en place : 
======================== 
Récupération des données / Prétraitement :
------------------------------------------

Data collection (RAPL)  
Aggrégation (?) for denoising   
Removing outliers   

Séparations des signaux en trois classes grâce à un arbre : 
----------------------------------------------------------------
 -> is stationnare(moving average/moving standart deviation)-> is variable (threshold on standard déviation) -> is periodic (DFT)
 
Questions :
----------
Types d'aggrégations utilisés pour le débruitage ?
Utilisation des données cpu ? Corrélation trop forte avec la consommation d'énergie ?

Idée : 
------ 
Spectrogramme + CNN  
clustering sur tableau individu / variable sur 3 variables issues de l'arbre => analyse des résultats et ajout de variables si nécessaire

Métriques :
----------- 
TWED / DTW  :  
https://arxiv.org/pdf/1401.3973.pdf   
https://github.com/jzumer/pytwed  


# Semaine 1

Methodes mise en place :
=======================

Hierachical clustering :
-----------------------
- Calcul de la distance entre les séries temporelles grâce à la métrique SBD (Shape Based distance : http://www1.cs.columbia.edu/~jopa/Papers/PaparrizosSIGMOD2015.pdf )
- Construction de la matrice de dissimilarité
- Hierachical clustering (à partir de la matrice de dissimilarité obtenue) avec test des différentes méthode d'aggrégation (average,ward ...)
- Analyse visuelle des résultats  
- Extraction des shape des centroides  
<b>Voir le notebook R clustering.Rmd</b>

CNN (abandonné):
---
- Construction d'une interface graphique pour simplifier la labélisation
- Labélisation des 797 séries temporelles en 19 classes 
- Transformation des signaux en spectrogramme
- Data augmentation en utilisant la méthode SpecAugment (https://arxiv.org/abs/1904.08779)
- Entrainement d'un CNN en faisant du transfert learning sur un modèle InceptionV3 entrainé sur imageNet (70% d'accuracy sans hyper parameters tunning)  
<b> Voir le notebook python Deep.ipynb </b>

Idées :
------
Décomposition en wavelet :
- https://www.researchgate.net/publication/24188358_Heartbeat_Time_Series_Classification_With_Support_Vector_Machines

Kernel based methodes :
- https://www.cv-foundation.org//openaccess/content_cvpr_workshops_2013/W16/papers/Lorincz_Emotional_Expression_Classification_2013_CVPR_paper.pdf
- http://ceur-ws.org/Vol-2259/aics_7.pdf
- http://members.cbio.mines-paristech.fr/~jvert/talks/070608telecom/telecom.pdf / https://arxiv.org/pdf/cs/0610033.pdf

Extraire plus de features à la main afin de mieux charactériser les signaux 
- https://tsfresh.readthedocs.io/en/latest/

Matrix profile 
- https://www.cs.ucr.edu/~eamonn/MatrixProfile.html
- https://www.cs.ucr.edu/~eamonn/PID4481997_extend_Matrix%20Profile_I.pdf

# Semaine 2

Hierachical clustering :
-----------------------
- Analyse des résultats et limites (Comparaison avec les signaux labélisés à la main)     
<b> Voir le notebook python Analyse.ipynb </b>

Random forest sur les charactéristiques extraites des signaux via tsfresh:
--------------------------------------------------------------------------
- Choix puis extraction de features via tsfresh  
<b> Voir le notebook python Extraction_de_features.ipynb </b>
- Application de random forrest / cross validation / grid search  
<b> Voir le notebook python Random_forest_on_features.ipynb </b>

Matrices profiles :
------------------
- Application, tracé et extraction de pattern via la méthode de matrice profile (https://www.cs.ucr.edu/~eamonn/PID4481997_extend_Matrix%20Profile_I.pdf)  
<b> Voir le notebook python Matrix_profile.ipynb </b>

# Semaine 3 

Processus gaussiens :
---------------------
- Exploration des méthodes 
  - http://membres-timc.imag.fr/Olivier.Francois/MPA_2013.pdf
  - https://github.com/duvenaud/phd-thesis/blob/master/thesis.pdf
  - http://www.gaussianprocess.org/gpml/chapters/
  - http://cs229.stanford.edu/section/cs229-gaussian_processes.pdf
  - https://www.youtube.com/watch?v=4vGiHC35j9s
  - https://github.com/datalad-datasets/machinelearning-books.git
  - https://betanalpha.github.io/
  - https://bookdown.org/rbg/surrogates/chap5.html)
  - https://durrande.shinyapps.io/gp_playground/ 
  
 - Essayer de coder des premières approches de processus gaussien en utilisant pymc3
  - Détecter les changepoints / https://arxiv.org/pdf/0710.3742.pdf / https://arxiv.org/pdf/1801.00718.pdf <b> Voir le notebook python Changepoints.ipynb </b>
  - Coder un premier processus gaussien avec des kernels simples <b> Voir le notebook python Gaussian_learning.ipynb </b>
  
  - Gradient descent probleme de determinant nul
    https://hal.archives-ouvertes.fr/hal-01264192v4/document
    
# Semaine 4

Processus gaussien :
-------------------- 
   - Abandon implémentation au profit de  l'implémentation https://github.com/T-Flet/GPy-ABCD
   - Analyse des résultats
    
Analyse des clusters obtenus à la main :
----------------------------------------
   - Voir Analyse_cluster.ipynb
   - Res à décire
    
1D CNN + Grad-CAM :
------------------ 
   - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6814172/
   - Implémentation dans notebook 1DCNN.ipynb
  
