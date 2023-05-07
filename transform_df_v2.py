### author : Félix
### Target : automatize the transformation of the table 
### parameters : year for the number of cars, crit_air or carburant for the distribution variable
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
df_pa = pandas.DataFrame()
df_pa_pv = pandas.DataFrame()
"""
print("structure de la table parc auto")
print(f" {df_parc_auto.shape} ")
print(df_parc_auto.columns)
"""
liste_Carburant = ["Diesel","Diesel HNR","Electrique et hydrogène","Essence","Essence HNR", "Gaz et inconnu","Hybride rechargeable"]
liste_CritAir = ["Crit'Air 1","Crit'Air 2","Crit'Air 3","Crit'Air 4","Crit'Air 5","Crit'Air E","Non classé","Inconnu"]

def distribution_by_city(year_V,distribution_V): 

    global df_parc_auto
    global df_pa
    global df_pa_pv
    global liste_Carburant
    global liste_CritAir
    # select of relevant columns
    df_pa = df_parc_auto[['Code INSEE','commune_de_residence', distribution_V,year_V]]
    # transform the table pivoting values of distribution_V in columns 
    df_pa_pv = pandas.pivot_table(df_pa,index=["Code INSEE","commune_de_residence"],columns=distribution_V,values=year_V,aggfunc=numpy.sum)
    # allocate the good list for loop
    if distribution_V == 'crit_air':
        liste_choisie = liste_CritAir
    elif distribution_V == 'carburant':
        liste_choisie = liste_Carburant
    # change NaN values in 0 
    for elt in liste_choisie:
        df_pa_pv[elt] = df_pa_pv[elt].fillna(0) 
    
    df_pa_pv["total nb vehicules"] = 0
    # create column global sum
    for elt in liste_choisie:
        df_pa_pv["total nb vehicules"] += df_pa_pv[elt]
    
    # create proportion for each elt
    liste_choisie_prop = []
    for elt in liste_choisie:
        liste_choisie_prop.append('Prop '+elt)
    for elt_prop,elt in zip(liste_choisie_prop,liste_choisie):
        df_pa_pv[elt_prop] = round((df_pa_pv[elt]/df_pa_pv["total nb vehicules"])*100,2)


distribution_by_city('2021','crit_air')
df_pa_pv.head(10) 
df_pa_pv.to_csv("C:/Users/felod/Desktop/Python/Projet Parc Automobile/Sources/pa_critair_2021.csv",index = True, encoding="utf-8-sig")


# verif of global sum of the table 
print (df_parc_auto["2021"].sum())
print (df_parc_auto['crit_air'].unique())