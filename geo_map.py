#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas
import numpy
import numpy as np
import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pyxll


# In[2]:


import scipy
#import gaussian_kde
"%matplotlib inline"


# In[3]:


df = pandas.read_excel('D:\\Adlane\\1.Formation PYTHON\\pandas\\parc auto\\parc_vp_commune_2022.xlsx', skiprows = 3, header = 0)


# In[4]:


print(df.shape)


# In[5]:


print(df.columns)


# In[6]:


df_1 = df.dropna()


# In[7]:


df_1.isnull().sum().sum()


# In[9]:


#droper cummune contenant 'Inconnu' ds colonne Commune de résidence
df_2 = df_1[~df_1["Commune de résidence"].str.contains('Inconnu', na=False)]


# In[10]:


df_2.shape


# In[11]:


# une fonction pour:
# créer une colonne avec les 2 premiers chiffres du code commune en créeant df_3
# droper 96 et 97
def df_propre_fr(df_fr_propre):
        df_fr_propre.drop(df_fr_propre[df_fr_propre['Code commune de résidence'].str.startswith('96')].index, inplace=True)
        df_fr_propre.drop(df_fr_propre[df_fr_propre['Code commune de résidence'].str.startswith('97')].index, inplace=True)
        df_fr_propre['code_departement'] = df_fr_propre['Code commune de résidence'].str[:2]
        return df_fr_propre


# In[12]:


df_3 = df_2


# In[13]:


df_propre_fr(df_3)


# In[14]:


df_3.shape


# In[16]:


# reset index
df_3.reset_index(drop = True, inplace = True)


# In[17]:


# deplacer colonne
colonne_a_deplacer = df_3.pop('code_departement')
df_3.insert(0, 'code_departement', colonne_a_deplacer)


# In[18]:


df_3


# In[19]:


# reset index
df_3.reset_index(drop = True, inplace = True)


# In[20]:


df_4 = df_3


# In[21]:


df_4.info()


# In[22]:


dfc = df_4


# In[23]:


# Arrondir la colonne 2022 à l'entier le plus proche et transformer la colonne en int
dfc['2022'] = dfc['2022'].round(0)
dfc['2022'] = dfc['2022'].astype(int)


# In[24]:


# importer file région
dfr = pandas.read_csv('D:\\Adlane\\1.Formation PYTHON\\pandas\\parc auto\\departements-region.csv', header = 0)


# In[25]:


dfr.shape


# In[26]:


# créer dataframe dfj qui merge dfc et dfr 
dfj = pandas.merge(dfc,dfr,how = 'left',left_on='code_departement',right_on='num_dep')


# In[27]:


dfj


# In[28]:


# renomer entête
dfj_f = dfj.rename(columns={ 'code_departement' : 'code_departement_de_residence', 'Code commune de résidence': 'code_commune_insee_residence', 'Commune de résidence': 'commune_de_residence', 
              'Carburant': 'carburant', "Crit'Air": 'crit_air' , 'dep_name' : 'departement_de_residence','region_name':'region_de_residence'})


# In[29]:


dfj_f.info()


# In[30]:


# droper champ num_dep
dfj_f = dfj_f.drop('num_dep', axis=1)


# In[31]:


# Fonction 1 : filtrer par année et région de résidence
# par carburant

## pour afficher la légende 
# Définir les deux fonctions de filtrage
def filter_par_annee_region_carburant(annee, region):
    filtered_df_1 = dfj_f.loc[dfj_f['region_de_residence'] == region, ['carburant', str(annee)]]
    return filtered_df_1

def filter_annee_region_t1(annee, region):
    filtered_df_1 = dfj_f.loc[(dfj_f['region_de_residence'] == region),['carburant', str(annee)]]
    sum_carburant = filtered_df_1.groupby('carburant')[str(annee)].sum()
    proportions = sum_carburant / sum_carburant.sum() * 100
    result = pandas.concat([sum_carburant, proportions], axis=1)
    result.columns = ['Nombre des véhicules', 'Proportion']
    result['Proportion'] = result['Proportion'].apply("{:.1f}%".format)
    total_vehicles = result['Nombre des véhicules'].sum()
    result.loc['Total'] = [total_vehicles, '']
    return result

# Définir les paramètres pour le camembert
annee = 2020
region = 'Île-de-France'
data_1 = filter_par_annee_region_carburant(annee, region).groupby('carburant')[str(annee)].sum()
explode_1 = (data_1.values == data_1.max()) * 0.1

# Définir les paramètres pour le tableau
tableau_1 = filter_annee_region_t1(annee, region)

# Créer la figure avec deux sous-graphiques
fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(10,5))

# Afficher le camembert dans le premier sous-graphique
wedges, texts, autotexts = ax1.pie(data_1.values, autopct='%1.1f%%', explode=explode_1)
ax1.set_title('Répartition des véhicules par carburant')
ax1.legend(wedges, data_1.index,
          title="Carburant",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
for i, autotext in enumerate(autotexts):
    autotext.set_text(tableau_1['Proportion'][i])

# Afficher le tableau dans le deuxième sous-graphique
ax2.axis('off')
ax2.table(cellText=tableau_1.values, colLabels=tableau_1.columns, rowLabels=tableau_1.index, loc='center')
ax2.set_title('Nombre et proportion des véhicules par carburant')

# Afficher la figure
plt.show()


# In[32]:


# par crit_air

# Définir les deux fonctions de filtrage
def filter_par_annee_region_crit_air(annee, region):
    filtered_df_1 = dfj_f.loc[dfj_f['region_de_residence'] == region, ['crit_air', str(annee)]]
    return filtered_df_1

def filter_annee_region_t1(annee, region):
    filtered_df_1 = dfj_f.loc[(dfj_f['region_de_residence'] == region),['crit_air', str(annee)]]
    sum_crit_air = filtered_df_1.groupby('crit_air')[str(annee)].sum()
    proportions = sum_crit_air / sum_crit_air.sum() * 100
    result = pandas.concat([sum_crit_air, proportions], axis=1)
    result.columns = ['Nombre des véhicules', 'Proportion']
    result['Proportion'] = result['Proportion'].apply("{:.1f}%".format)
    total_vehicles = result['Nombre des véhicules'].sum()
    result.loc['Total'] = [total_vehicles, '']
    return result

# Définir les paramètres pour le camembert
annee = 2020
region = 'Île-de-France'
data_1 = filter_par_annee_region_crit_air(annee, region).groupby('crit_air')[str(annee)].sum()
explode_1 = (data_1.values == data_1.max()) * 0.1

# Définir les paramètres pour le tableau
tableau_1 = filter_annee_region_t1(annee, region)

# Créer la figure avec deux sous-graphiques
fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(10,5))

# Afficher le camembert dans le premier sous-graphique
wedges, texts, autotexts = ax1.pie(data_1.values, autopct='%1.1f%%', explode=explode_1)
ax1.set_title('Répartition des véhicules par critère air')
ax1.legend(wedges, data_1.index,
          title="Critère air",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
for i, autotext in enumerate(autotexts):
    autotext.set_text(tableau_1['Proportion'][i])

# Afficher le tableau dans le deuxième sous-graphique
ax2.axis('off')
ax2.table(cellText=tableau_1.values, colLabels=tableau_1.columns, rowLabels=tableau_1.index, loc='center')
ax2.set_title('Nombre et proportion des véhicules par critère air')

# Afficher la figure
plt.show()


# In[33]:


# Fonction 2 : filtrer par année, région et departement de résidence

# Définir les deux fonctions de filtrage
def filter_par_annee_region_departement_carburant(annee, region, departement):
    filtered_df_2 = dfj_f.loc[(dfj_f['region_de_residence'] == region) & (dfj_f['code_departement_de_residence'] == departement), ['carburant', str(annee)]]
    return filtered_df_2

def filter_annee_region_departement_t2(annee, region, departement):
    filtered_df_2 = dfj_f.loc[(dfj_f['region_de_residence'] == region) & (dfj_f['code_departement_de_residence'] == departement), ['carburant', str(annee)]]
    sum_carburant = filtered_df_2.groupby('carburant')[str(annee)].sum()
    proportions = sum_carburant / sum_carburant.sum() * 100
    result = pandas.concat([sum_carburant, proportions], axis=1)
    result.columns = ['Nombre des véhicules', 'Proportion']
    result['Proportion'] = result['Proportion'].apply("{:.1f}%".format)
    total_vehicles = result['Nombre des véhicules'].sum()
    result.loc['Total'] = [total_vehicles, '']
    return result

# Définir les paramètres pour le camembert
annee = 2020
region = 'Île-de-France'
departement = '75'
data_2 = filter_par_annee_region_departement_carburant(annee, region,departement).groupby('carburant')[str(annee)].sum()
explode_2 = (data_2.values == data_2.max()) * 0.1

# Définir les paramètres pour le tableau
tableau_2 = filter_annee_region_departement_t2(annee, region, departement)

# Créer la figure avec deux sous-graphiques
fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(10,5))

# Afficher le camembert dans le premier sous-graphique
wedges, texts, autotexts = ax1.pie(data_2.values, autopct='%1.1f%%', explode=explode_2)
ax1.set_title('Répartition des véhicules par carburant')
ax1.legend(wedges, data_2.index,
          title="Carburant",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
for i, autotext in enumerate(autotexts):
    autotext.set_text(tableau_2['Proportion'][i])

# Afficher le tableau dans le deuxième sous-graphique
ax2.axis('off')
ax2.table(cellText=tableau_2.values, colLabels=tableau_2.columns, rowLabels=tableau_2.index, loc='center')
ax2.set_title('Nombre et proportion des véhicules par carburant')

# Afficher la figure
plt.show()


# In[34]:


# par crit_air

# Définir les deux fonctions de filtrage
def filter_par_annee_region_departement_crit_air(annee, region, departement):
    filtered_df_2 = dfj_f.loc[(dfj_f['region_de_residence'] == region) & (dfj_f['code_departement_de_residence'] == departement), ['crit_air', str(annee)]]
    return filtered_df_2

def filter_annee_region_departement_t2(annee, region, departement):
    filtered_df_2 = dfj_f.loc[(dfj_f['region_de_residence'] == region) & (dfj_f['code_departement_de_residence'] == departement), ['crit_air', str(annee)]]
    sum_crit_air = filtered_df_2.groupby('crit_air')[str(annee)].sum()
    proportions = sum_crit_air / sum_crit_air.sum() * 100
    result = pandas.concat([sum_crit_air, proportions], axis=1)
    result.columns = ['Nombre des véhicules', 'Proportion']
    result['Proportion'] = result['Proportion'].apply("{:.1f}%".format)
    total_vehicles = result['Nombre des véhicules'].sum()
    result.loc['Total'] = [total_vehicles, '']
    return result

# Définir les paramètres pour le camembert
annee = 2020
region = 'Île-de-France'
departement = '75'
data_2 = filter_par_annee_region_departement_crit_air(annee, region,departement).groupby('crit_air')[str(annee)].sum()
explode_2 = (data_2.values == data_2.max()) * 0.1

# Définir les paramètres pour le tableau
tableau_2 = filter_annee_region_departement_t2(annee, region, departement)

# Créer la figure avec deux sous-graphiques
fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(10,5))

# Afficher le camembert dans le premier sous-graphique
wedges, texts, autotexts = ax1.pie(data_2.values, autopct='%1.1f%%', explode=explode_2)
ax1.set_title('Répartition des véhicules par critère air')
ax1.legend(wedges, data_2.index,
          title="Critère air",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
for i, autotext in enumerate(autotexts):
    autotext.set_text(tableau_2['Proportion'][i])

# Afficher le tableau dans le deuxième sous-graphique
ax2.axis('off')
ax2.table(cellText=tableau_2.values, colLabels=tableau_2.columns, rowLabels=tableau_2.index, loc='center')
ax2.set_title('Nombre et proportion des véhicules par critère air')

# Afficher la figure
plt.show()


# In[35]:


# Fonction 3 : filtrer par année, région, departement et commune de résidence

# Définir les deux fonctions de filtrage
def filter_par_annee_region_departement_commune_carburant(annee, region, departement, commune):
    filtered_df_3 = dfj_f.loc[(dfj_f['region_de_residence'] == region) & (dfj_f['code_departement_de_residence'] == departement) & (dfj_f['commune_de_residence'] == commune), ['carburant', str(annee)]]
    return filtered_df_3

def filter_annee_region_departement_commune_t3(annee, region, departement, commune):
    filtered_df_3 = dfj_f.loc[(dfj_f['region_de_residence'] == region) & (dfj_f['code_departement_de_residence'] == departement) & (dfj_f['commune_de_residence'] == commune), ['carburant', str(annee)]]
    sum_carburant = filtered_df_3.groupby('carburant')[str(annee)].sum()
    proportions = sum_carburant / sum_carburant.sum() * 100
    result = pandas.concat([sum_carburant, proportions], axis=1)
    result.columns = ['Nombre des véhicules', 'Proportion']
    result['Proportion'] = result['Proportion'].apply("{:.1f}%".format)
    total_vehicles = result['Nombre des véhicules'].sum()
    result.loc['Total'] = [total_vehicles, '']
    return result

# Définir les paramètres pour le camembert
annee = 2020
region = 'Île-de-France'
departement = '75'
commune = 'Paris 2e Arrondissement'
data_3 = filter_par_annee_region_departement_commune_carburant(annee, region,departement,commune).groupby('carburant')[str(annee)].sum()
explode_3 = (data_3.values == data_3.max()) * 0.1

# Définir les paramètres pour le tableau
tableau_3 = filter_annee_region_departement_commune_t3(annee, region, departement,commune)

# Créer la figure avec deux sous-graphiques
fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(10,5))

# Afficher le camembert dans le premier sous-graphique
wedges, texts, autotexts = ax1.pie(data_3.values, autopct='%1.1f%%', explode=explode_3)
ax1.set_title('Répartition des véhicules par carburant')
ax1.legend(wedges, data_3.index,
          title="Carburant",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
for i, autotext in enumerate(autotexts):
    autotext.set_text(tableau_3['Proportion'][i])

# Afficher le tableau dans le deuxième sous-graphique
ax2.axis('off')
ax2.table(cellText=tableau_3.values, colLabels=tableau_3.columns, rowLabels=tableau_3.index, loc='center')
ax2.set_title('Nombre et proportion des véhicules par carburant')

# Afficher la figure
plt.show()


# In[36]:


# par crit_air

# Définir les deux fonctions de filtrage
def filter_par_annee_region_departement_commune_crit_air(annee, region, departement, commune):
    filtered_df_3 = dfj_f.loc[(dfj_f['region_de_residence'] == region) & (dfj_f['code_departement_de_residence'] == departement) & (dfj_f['commune_de_residence'] == commune), ['crit_air', str(annee)]]
    return filtered_df_3

def filter_annee_region_departement_commune_t3(annee, region, departement, commune):
    filtered_df_3 = dfj_f.loc[(dfj_f['region_de_residence'] == region) & (dfj_f['code_departement_de_residence'] == departement) & (dfj_f['commune_de_residence'] == commune), ['crit_air', str(annee)]]
    sum_crit_air = filtered_df_3.groupby('crit_air')[str(annee)].sum()
    proportions = sum_crit_air / sum_crit_air.sum() * 100
    result = pandas.concat([sum_crit_air, proportions], axis=1)
    result.columns = ['Nombre des véhicules', 'Proportion']
    result['Proportion'] = result['Proportion'].apply("{:.1f}%".format)
    total_vehicles = result['Nombre des véhicules'].sum()
    result.loc['Total'] = [total_vehicles, '']
    return result

# Définir les paramètres pour le camembert
annee = 2020
region = 'Île-de-France'
departement = '92'
commune = 'Sceaux'
data_3 = filter_par_annee_region_departement_commune_crit_air(annee, region,departement,commune).groupby('crit_air')[str(annee)].sum()
explode_3 = (data_3.values == data_3.max()) * 0.1

# Définir les paramètres pour le tableau
tableau_3 = filter_annee_region_departement_commune_t3(annee, region, departement,commune)

# Créer la figure avec deux sous-graphiques
fig, (ax2, ax1) = plt.subplots(1, 2, figsize=(10,5))

# Afficher le camembert dans le premier sous-graphique
wedges, texts, autotexts = ax1.pie(data_3.values, autopct='%1.1f%%', explode=explode_3)
ax1.set_title('Répartition des véhicules par critère de qualité de l\'air')
ax1.legend(wedges, data_3.index,
          title="Critère de qualité de l\'air",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
for i, autotext in enumerate(autotexts):
    autotext.set_text(tableau_3['Proportion'][i])

# Afficher le tableau dans le deuxième sous-graphique
ax2.axis('off')
ax2.table(cellText=tableau_3.values, colLabels=tableau_3.columns, rowLabels=tableau_3.index, loc='center')
ax2.set_title('Nombre et proportion des véhicules par critère de qualité de l\'air')

# Afficher la figure
plt.show()


# In[37]:


dfe = dfj_f


# In[38]:


dfe


# In[39]:


# importer df_geloc

df_geo = pandas.read_csv('D:\\Adlane\\1.Formation PYTHON\\pandas\\parc auto\\df_geoloc.csv', header = 0)


# In[40]:


df_geo.isnull().sum().sum()


# In[41]:


# faire un merge dfe et df_geo
parc_vp_propre_geoloc = pandas.merge(dfe, df_geo[['Code INSEE','geo_point_2d','geo_shape','ID Geofla']], left_on='code_commune_insee_residence', right_on='Code INSEE', how='left')


# In[42]:


parc_vp_propre_geoloc.info()


# In[43]:


parc_vp_propre_geoloc.isnull().sum().sum()


# In[44]:


parc_vp_propre_geoloc.isnull().sum()


# In[45]:


# droper lignes nulles
parc_vp_propre_geoloc_final = parc_vp_propre_geoloc.dropna()


# In[46]:


parc_vp_propre_geoloc_final.isnull().sum()


# In[47]:


parc_vp_propre_geoloc_final.info()


# In[48]:


parc_vp_propre_geoloc_final.isnull().sum().sum()


# In[ ]:


# créer un csv 
parc_vp_propre_geoloc_final.to_csv("D:\\Adlane\\1.Formation PYTHON\\pandas\\parc auto\\parc_vp_propre_geoloc_final.csv",index = True, encoding="utf-8-sig")


# In[49]:


parc_vp_propre_geoloc_final.columns


# In[50]:


parc_vp_propre_geoloc_final['geo_point_2d'].tail(20)


# In[51]:


parc_map = parc_vp_propre_geoloc_final


# In[55]:


parc_map.describe(include = 'all')


# In[56]:


parc_map[['lattitude', 'longitude']] = parc_map['geo_point_2d'].str.split(',', expand=True)


# In[70]:


parc_map


# In[96]:


def filter_annee_region_departement_commune_t3(annee, region, departement, commune):
    filtered_df_3 = parc_map.loc[(parc_map['region_de_residence'] == region) & (parc_map['code_departement_de_residence'] == departement) & (parc_map['commune_de_residence'] == commune), ['crit_air', str(annee)]]
    sum_crit_air = filtered_df_3.groupby('crit_air')[str(annee)].sum()
    proportions = sum_crit_air / sum_crit_air.sum() * 100
    result = pandas.concat([sum_crit_air, proportions], axis=1)
    result.columns = ['Nombre des véhicules', 'Proportion']
    result['Proportion'] = result['Proportion'].apply("{:.1f}%".format)
    total_vehicles = result['Nombre des véhicules'].sum()
    result.loc['Total'] = [total_vehicles, '']
    return result



# In[97]:


# Créer une liste vide pour stocker les DataFrames pour chaque commune
commune_dfs = []


# In[99]:


# Itérer sur toutes les communes du DataFrame parc_map
for i, commune in enumerate(parc_map['commune_de_residence'].unique()):
    # Filtrer les données pour cette commune et cette année
    commune_df = filter_annee_region_departement_commune_t3(2021, '', '', commune)
    # Ajouter une colonne pour le nom de la commune
    commune_df['Commune'] = commune
    # Ajouter le DataFrame pour cette commune à la liste
    commune_dfs.append(commune_df)
    # Afficher le progrès tous les 1000 éléments
    if i % 1000 == 0:
        print(f"Progression : {i}/{len(parc_map['commune_de_residence'].unique())}")


# In[119]:


def filter_annee_region_departement_commune_t3(annee, region, departement, commune, crit_air_type):
    filtered_df_3 = parc_map.loc[(parc_map['region_de_residence'] == region) & (parc_map['code_departement_de_residence'] == departement) & (parc_map['commune_de_residence'] == commune) & (parc_map['crit_air'] == crit_air_type), ['crit_air', str(annee)]]
    sum_crit_air = filtered_df_3.groupby('crit_air')[str(annee)].sum()
    proportions = sum_crit_air / sum_crit_air.sum() * 100
    result = pandas.concat([sum_crit_air, proportions], axis=1)
    result.columns = ['Nombre des véhicules', 'Proportion']
    result['Proportion'] = result['Proportion'].apply("{:.1f}%".format)
    total_vehicles = result['Nombre des véhicules'].sum()
    result.loc['Total'] = [total_vehicles, '']
    result['Type de critère air'] = crit_air_type
    return result

# Créer une liste vide pour stocker les DataFrames pour chaque commune
commune_dfs = []
# Itérer sur toutes les communes du DataFrame parc_map
for i, commune in enumerate(parc_map['commune_de_residence'].unique()):
    # Filtrer les données pour cette commune, cette année, et ce type de critère d'air
    commune_df = filter_annee_region_departement_commune_t3(2021, '', '', commune, 'Type de critère d\'air')
    # Ajouter une colonne pour le nom de la commune
    commune_df['Commune'] = commune
    # Ajouter le DataFrame pour cette commune à la liste
    commune_dfs.append(commune_df)
    # Afficher le progrès tous les 1000 éléments
    if i % 1000 == 0:
        print(f"Progression : {i}/{len(parc_map['commune_de_residence'].unique())}")


# In[120]:


# Concaténer tous les DataFrames pour chaque commune en un seul DataFrame
result_df = pandas.concat(commune_dfs, ignore_index=True)


# In[121]:


result_df

