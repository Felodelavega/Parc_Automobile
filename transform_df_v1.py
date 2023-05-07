### importation des bibliothéques

import os
import pandas
import csv
import numpy
import pyxll
import matplotlib
import scipy

### import de la table de données 
df_parc_auto = pandas.read_csv("C:/Users/felod/Desktop/Python/Projet Parc Automobile/Sources/parc_vp_propre_geoloc_final.csv",sep=',') 
print("structure de la table parc auto")
print(f" {df_parc_auto.shape} ")
print(df_parc_auto.columns)
df_parc_auto_carb_2021 = df_parc_auto[['Code INSEE','commune_de_residence', 'carburant','2021']]
### Transposons les types de carburant et aggrégeons les nb de véhicules 2021 
df_parc_auto_carb_pivot_2021 = pandas.pivot_table(df_parc_auto_carb_2021,index=["Code INSEE","commune_de_residence"],columns='carburant',values='2021',aggfunc=numpy.sum)
df_parc_auto_carb_pivot_2021.reset_index()
### transformer les valeurs Nan en 0 pour les colonnes carburant
df_parc_auto_carb_pivot_2021["Diesel"]                  = df_parc_auto_carb_pivot_2021["Diesel"].fillna(0)
df_parc_auto_carb_pivot_2021["Diesel HNR"]              = df_parc_auto_carb_pivot_2021["Diesel HNR"].fillna(0)
df_parc_auto_carb_pivot_2021["Electrique et hydrogène"] = df_parc_auto_carb_pivot_2021["Electrique et hydrogène"].fillna(0)
df_parc_auto_carb_pivot_2021["Essence"]                 = df_parc_auto_carb_pivot_2021["Essence"].fillna(0)
df_parc_auto_carb_pivot_2021["Essence HNR"]             = df_parc_auto_carb_pivot_2021["Essence HNR"].fillna(0)
df_parc_auto_carb_pivot_2021["Gaz et inconnu"]          = df_parc_auto_carb_pivot_2021["Gaz et inconnu"].fillna(0)
df_parc_auto_carb_pivot_2021["Hybride rechargeable"]    = df_parc_auto_carb_pivot_2021["Hybride rechargeable"].fillna(0)
### ajout du total 
df_parc_auto_carb_pivot_2021["total véhicules 2021"] = df_parc_auto_carb_pivot_2021["Diesel"]+df_parc_auto_carb_pivot_2021["Diesel HNR"]+df_parc_auto_carb_pivot_2021["Electrique et hydrogène"]+df_parc_auto_carb_pivot_2021["Essence"]+df_parc_auto_carb_pivot_2021["Essence HNR"]+df_parc_auto_carb_pivot_2021["Gaz et inconnu"]+df_parc_auto_carb_pivot_2021["Hybride rechargeable"]
### ajout des proportions pour chaque carburant
df_parc_auto_carb_pivot_2021["proportion Diesel"] = round((df_parc_auto_carb_pivot_2021["Diesel"]/df_parc_auto_carb_pivot_2021["total véhicules 2021"])*100,2)
df_parc_auto_carb_pivot_2021["proportion Diesel HNR"] = round((df_parc_auto_carb_pivot_2021["Diesel HNR"]/df_parc_auto_carb_pivot_2021["total véhicules 2021"])*100,2)
df_parc_auto_carb_pivot_2021["proportion Electrique et hydrogène"] = round((df_parc_auto_carb_pivot_2021["Electrique et hydrogène"]/df_parc_auto_carb_pivot_2021["total véhicules 2021"])*100,2)
df_parc_auto_carb_pivot_2021["proportion Essence"] = round((df_parc_auto_carb_pivot_2021["Essence"]/df_parc_auto_carb_pivot_2021["total véhicules 2021"])*100,2)
df_parc_auto_carb_pivot_2021["proportion Essence HNR"] = round((df_parc_auto_carb_pivot_2021["Essence HNR"]/df_parc_auto_carb_pivot_2021["total véhicules 2021"])*100,2)
df_parc_auto_carb_pivot_2021["proportion Gaz et inconnu"] = round((df_parc_auto_carb_pivot_2021["Gaz et inconnu"]/df_parc_auto_carb_pivot_2021["total véhicules 2021"])*100,2)
df_parc_auto_carb_pivot_2021["proportion Hybride rechargeable"] = round((df_parc_auto_carb_pivot_2021["Hybride rechargeable"]/df_parc_auto_carb_pivot_2021["total véhicules 2021"])*100,2)
### export
df_parc_auto_carb_pivot_2021.to_csv("C:/Users/felod/Desktop/Python/Projet Parc Automobile/Sources/pa_2011.csv",index = True, encoding="utf-8-sig")