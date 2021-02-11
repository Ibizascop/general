data = read.table("fertility_Diagnosis.txt",sep=",")

library(factoextra)
library(caret)
library(lime)
library(rpart)
library(cluster)
library(rpart.plot)
library(psych)

names(data)[1] <- "Season"
names(data)[2] <- "Age"
names(data)[3] <- "Childish Diseases"
names(data)[4] <- "Accident or Serious Trauma"
names(data)[5] <- "Surgical Intervention"
names(data)[6] <- "High Fevers"
names(data)[7] <- "Alchool Consumption"
names(data)[8] <- "Smoking Habit"
names(data)[9] <- "Nb hours sitting per day"
names(data)[10] <- "Diagnosis"


#Matrice de nuages de points
plot(data)

#Transforme la colonne Diagnosis en numérique pour histogrammes, correlations ....
data_2 = data
code = function(x) {
  if (x == "N") 
    return (1)
  if (x == "O") 
    return (2)
}
data_2$Diagnosis_codé = apply(data_2[,c("Diagnosis"),drop = F],1,code)
data_2 = data_2[-c(10)]

cor(data_2)

#Visualisations préliminaires
par(mfrow=c(2,5))


#Histogrammes
hist(data$Season)
hist(data$Age)
hist(data$`Childish Diseases`)
hist(data$`Accident or Serious Trauma`)
hist(data$`Surgical Intervention`)
hist(data$`High Fevers`)
hist(data$`Alchool Consumption`)
hist(data$`Smoking Habit`)
hist(data$`Nb hours sitting per day`)
hist(data_2$Diagnosis_codé)

#Boxplots
boxplot(split(data$Season,data$Diagnosis), main="Season")
boxplot(split(data$Age,data$Diagnosis), main="Age")
boxplot(split(data$`Childish Diseases`,data$Diagnosis), main="Childish Diseases")
boxplot(split(data$`Accident or Serious Trauma`,data$Diagnosis), main="Accident or Serious Trauma")
boxplot(split(data$`Surgical Intervention`, data$Diagnosis), main="Surgical Intervention")
boxplot(split(data$`High Fevers`,data$Diagnosis), main="High Fevers")
boxplot(split(data$`Alchool Consumption`,data$Diagnosis), main="Alchool Consumption")
boxplot(split(data$`Smoking Habit`,data$Diagnosis), main="Smoking Habit")
boxplot(split(data$`Nb hours sitting per day`,data$Diagnosis), main="Nb hours sitting per day")


par(mfrow=c(1,1))

#Classification non supervisée, on enlève la variable à prédire
data_4 = data[-c(10)]

#Kmeans
#Détermination du nb de classes par méthode du coude
Sommes_carrés=c()
for (i in 2:20) {
  K_means <- kmeans(data_4,i)
  Sommes_carrés[i-1] = K_means$tot.withinss
}
Sommes_carrés

plot(2:20,Sommes_carrés,type='o',xlab ='Nb de classes',ylab='Sommes carrées intraclasses',main="Kmeans Nb de classes optimal")
abline(v = 4,col="blue")

#Kmeans avec 4 classes, visualisation
K_means_final = kmeans(data_4,4)
print(K_means_final)
fviz_cluster(K_means_final, data_4, ellipse.type = "norm")

#PAM
#Détermination du nb de classes aves la valeur silhouette
Silhouette_PAM =c()
for (i in 2:20) {
  PAM = pam(data_4,i)
  Silhouette_PAM[i-1] = PAM$silinfo$avg.width
}
Silhouette_PAM
plot(2:20,Silhouette_PAM,type='o',xlab ='Nb de classes',ylab='Valeur silhouette globale',main="Nb de classes optimal pour le PAM")

#Visualisation d'un PAM avec 5 classes, meilleur résultat avec un nb de classes restreint
PAM_final = pam(data_4,5)
PAM_final$id.med
fviz_silhouette(PAM_final, label=TRUE)

#CAH
#Agglomerative clustering , bien pour des petits clusters
CAH_Agglo = agnes(x = data_4, 
                  stand = TRUE, 
                  metric = "euclidean",
                  method = "ward")
CAH_Agglo$ac #Mesurer la qualité du clustering, similaire à la silhouette

#Détermination de la meilleure partition
inertie <- sort(CAH_Agglo$height, decreasing = TRUE)
plot(inertie[1:20], type = "s", xlab = "Nombre de classes", ylab = "Inertie")
points(c(2, 3), inertie[c(2, 3)], col = c("green3", "red3"), cex = 2, lwd = 3)

#Visualisation des 2 potentielles meilleures parititions
fviz_dend(CAH_Agglo, cex = 0.8,k=2,main = paste("Agglomerative Cluster Dendrogram","Quality=",round(CAH_Agglo$ac,4)), 
          xlab = "",
          ylab = "Height",
          color_labels_by_k = TRUE,
          rect = TRUE,
          rect_border = "black"
           )

fviz_dend(CAH_Agglo, cex = 0.8,k=3,main = paste("Agglomerative Cluster Dendrogram","Quality=",round(CAH_Agglo$ac,4)), 
          xlab = "",
          ylab = "Height",
          color_labels_by_k = TRUE,
          rect = TRUE,
          rect_border = "black"
)


#Division entrainement / test

division = sample(nrow(data), 0.6*nrow(data), replace = FALSE)
TrainSet = data[division,]
ValidSet = data[-division,]


#Arbre de classification
arbre <- rpart(data$Diagnosis~ ., data=data,subset = division, control = rpart.control("minsplit" = 1), xval = 30)
               
arbre
plot(arbre)
text(arbre)
tab = table(predict(arbre, data[-division,], type="class"), data[-division,"Diagnosis"]) 
(tab[1]+tab[4])/sum(tab)


#Bootsratp
précision_boot = matrix(0,nrow=100,ncol=1)
précision_max = 0
for (i in 1:100) {
  division_boot = sample(nrow(data), 0.6*nrow(data), replace = FALSE)
  TrainSet_boot = data[division_boot,]
  ValidSet_boot = data[-division_boot,]
  arbre_boot <- rpart(data$Diagnosis~ ., data=data,subset = division_boot, control = rpart.control("minsplit" = 1), xval = 30)
  tab_boot = table(predict(arbre_boot, data[-division_boot,], type="class"), data[-division_boot,"Diagnosis"]) 
  précision_boot[i] = (tab_boot[1]+tab_boot[4])/sum(tab_boot)
  
  if (précision_boot[i] > précision_max) {
    précision_max = précision_boot[i]
    arbre_final = arbre_boot
    check = i 
  }
}
#Récupérer meilleur arbre
arbre_final
tab_final = table(predict(arbre_final, data[-division_boot,], type="class"), data[-division_boot,"Diagnosis"]) 
tab_final
(tab_final[1]+tab_final[4])/sum(tab_final)
#Visualisation simple
plot(arbre_final)
text(arbre_final)

#Visualisation avancée
rpart.plot(arbre_final,tweak=1.6,extra=101)

#Moyenne, Variance de l'ensemble des arbres
mean(précision_boot)
var(précision_boot)
hist(précision_boot,xlab="Précision des arbres",main=paste("Précision moyenne =",
                                                           round(mean(précision_boot),4),",",
                                                           "Variance",round(var(précision_boot),4)))

#RandomForest
set.seed(22)
division_rf = sample(nrow(data), 0.6*nrow(data), replace = FALSE)
TrainSet_rf = data[division_rf,]
ValidSet_rf = data[-division_rf,]

#Création de la gridsearch
tgrid <- expand.grid(
  .mtry = 2:9,
  .splitrule = "gini",
  .min.node.size = 2:10)

#Création modèle (avec Caret)
rf = train(Diagnosis  ~ ., data = TrainSet_rf,
           method = "ranger",
           trControl = trainControl(method="cv", number = 10, verboseIter = T, classProbs = T),
           tuneGrid = tgrid,
           num.trees = 100,
           importance = "impurity")


#Vérification sur entrainement
predTrain <- predict(rf, TrainSet_rf)
mean(predTrain == TrainSet_rf$Diagnosis)    
table(predTrain, TrainSet_rf$Diagnosis)  

#Essai sur test
predValid <- predict(rf, ValidSet_rf)
mean(predValid == ValidSet_rf$Diagnosis)                    
table(predValid,ValidSet_rf$Diagnosis)

#Suppression variable à prédir pour lime
train_x <- dplyr::select(TrainSet_rf, -Diagnosis)
test_x <- dplyr::select(ValidSet_rf, -Diagnosis)

train_y <- dplyr::select(TrainSet_rf, Diagnosis)
test_y <- dplyr::select(ValidSet_rf, Diagnosis)

#création explainer  
explainer <- lime(train_x, rf, n_bins = 5, quantile_bins = TRUE)
explanation_rf <- lime::explain(test_x, explainer, n_labels = 1, n_features = 9, n_permutations = 1000, feature_select = "forward_selection")

#visualisation
plot_features(explanation_rf[101:1312, ], ncol = 1)