# data manipulation and visualisation
library(dplyr,quietly = TRUE)
library(tidyverse,quietly = TRUE)
# hdf5 file manipulation
library(rhdf5)
library(viridis)
library(ggplot2,quietly = TRUE)
library(reshape2,quietly = TRUE)
library(viridis,quietly = TRUE)
library(data.table,quietly = TRUE)
library(xtable,quietly = TRUE)
library(knitr)
library(markdown)
library(stringr)
library(cowplot)
library(patchwork)
library(pacman)
library("rio")
source("./utils/energy_Util.R")
p_load(dtwclust)
p_load(heatmaply)
p_load(rio)
p_load(dbscan)


nb_files <- 797  #put number of element (equivalent to os.list.dir in python)
nb_clusters <- 15

  

matrix <- matrix(0L, nrow = nb_files, ncol = nb_files)

mem <- vector(mode = "list", length = nb_files)

for (i in 1:nb_files) {
  ith_ts <- import(gsub(" ", "", paste(i, ".csv")))
  mem[[i]] <- (ith_ts$engergy)
  j<-1
  print(paste((i/nb_files)*100,"%"))
  flush.console()
  if (i > 1 ){
    for (vec in mem){
      if (is.null(vec) == F){
        matrix[j,i] = SBD(x=ith_ts$engergy,y=vec,znorm=F,error.check = T)$dist
        matrix[i,j] = matrix[j,i]
        j=j+1
      }
    }
  }
}
 

#save(matrix,file="similarity_matrix.RData") 
matrix <- as.dist(matrix) 

#load( file="similarity_matrix.RData" )

fviz_dist(matrix,gradient = list(low = "#00AFBB", mid = "white", high = "#FC4E07"))

hclu=hclust(matrix, method = "ward", members = NULL)

plot(hclu)

h <- sort(hclu$height, decreasing = TRUE)
plot(h[1:as.integer(nb_files/10)], type = "s", xlab = "Nombre de classes", ylab = "Diss")

clusters <- cutree(hclu,nb_clusters)
counter <- 1
clusters_list <- list()
freq <-vector(mode = "list", length = nb_clusters)
summary <- list()
for (i in 1:nb_clusters){
  print(paste((i/nb_clusters)*100,"%"))
  for (j in 1:nb_files){
    if ((clusters == i)[j]){
      ith_ts <- import(gsub(" ", "", paste(j, ".csv")))
      clusters_list[[counter]] <-ith_ts$engergy
    }
  }
  freq[[i]] = sum((clusters == i))
  centroid = shape_extraction(clusters_list,znorm=F)
  plot(centroid,type="lines",main =paste("Class n°",i ," with",sum((clusters == i)),"elements"))
  #export(centroid,gsub(" ", "", paste("centroid_class_",i, ".csv")))
  num <- gsub(" ", "", paste("class_",i, ".png"))
  png(file=gsub(" ","",paste("centroids/",num)), width=600, height=350)
  plot(centroid,type="lines",main =paste("Class n°",i ," with",sum((clusters == i)),"elements"))
  dev.off()
  write.csv(centroid, file =paste("centroid_class_",i, ".csv"), row.names=FALSE)
}

write.csv(freq, file ="freq.csv")

data = matrix(c(1:789*789),row=789)