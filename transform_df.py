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
print(f" {df_parc_auto_carb_2021.shape} ")
### Transposeons les types de carburant et aggrégeons les nb de véhicules 2021 
df_parc_auto_carb_pivot_2021 = pandas.pivot_table(df_parc_auto_carb_2021,index=["Code INSEE","commune_de_residence"],columns='carburant',values='2021',aggfunc=numpy.sum)
df_parc_auto_carb_pivot_2021.head(20)