############################################################################################################################################################################################################
#GWAS using GAPIT (Genomic Association & Prediction Integrated Tool)
#Modified from: https://github.com/jiabowang/GAPIT
#Wang J., Zhang Z., GAPIT Version 3: Boosting Power and Accuracy for Genomic Association and Prediction, Genomics, Proteomics & Bioinformatics (2021), doi: https://doi.org/10.1016/j.gpb.2021.08.005
############################################################################################################################################################################################################

#Install GAPIT packages
source("http://zzlab.net/GAPIT/gapit_functions.txt")
source("http://zzlab.net/GAPIT/emma.txt") # update GAPIT package for a new EMMA library

#Import packages to R environment
library(ape)
library(bigmemory)
library(compiler)
library(EMMREML)
library(gplots)
library(lme4)
library(multtest)
library(scatterplot3d)

#Import phenotypic/phenomic data
Phenodata<-read.table("Phenotypes_CottonNeps_BLUP.txt", head=TRUE)
#Import genomic data
Genodata<-read.table("new.HapMap.txt", sep="\t", head=F)

##Genotypic format adjustment
X <- Genodata[-1, ]
n <- nrow(X)
newG_temp <- vector("list", n)

for (i in seq_len(n)) {
  newG_temp[[i]] <- GAPIT.HMP.Amplification(X[i, ])
  if (i %% 100 == 0) cat("Processed:", i, "\n")
}

newG <- do.call(rbind, newG_temp)
newG <- rbind(Genodata[1, ], newG)
write.table(newG, "new.HapMap.txt", sep = "\t", row.names = FALSE, quote = FALSE, col.names = FALSE)

############################################################################################################################################################################################################
#Redefine Genotypic data file
Genodata=data.table::fread("new.HapMap.txt",
                           header = F,
                           na.strings = c("NA", "NaN"),
                           data.table = F)

############################################################################################################################################################################################################
#Run GWAS models:
myGAPIT_MLM <-GAPIT(
  Y=Phenodata[,c(1,3)],
  G=Genodata, 
  PCA.total=3,
  model=c("MLM", "GLM", "FarmCPU", "Blink"))



