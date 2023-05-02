import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
# en relation avec le changement d'echelle sur l'axe des y pour les barplot
from matplotlib.ticker import FuncFormatter
import gmplot
from plotnine import *
import folium
from folium.plugins import MarkerCluster
from gmaps import *
import base64
from io import BytesIO
import json

p = os.getcwd()

# , dtype={3: str, 4: str})
df_propre = pd.read_csv(
    # p + r'/France_data/df_merged_geoloc_lat_long.csv', index_col=[0], dtype={4: str, 5: str, 21: str})
    p + r'/France_data/parc_vp_propre_geoloc_final.csv', index_col=[0], dtype={1: str, 2: str, 20: str})
df_propre[['lattitude', 'longitude']
          ] = df_propre['geo_point_2d'].str.split(',', expand=True)
df_propre[['lattitude', 'longitude']] = df_propre[[
    'lattitude', 'longitude']].astype(float)

# # Define colors for each Crit'Air category
# colors = {"Crit'Air E": 'green', "Crit'Air 1": 'purple', "Crit'Air 2": 'yellow', "Crit'Air 3": 'orange',
#         "Crit'Air 4": 'maroon', "Crit'Air 5": 'gray', "Inconnu": 'black', "Non classé": 'brown'}
# # Add color column based on Crit'Air category
# df_propre['couleur'] = [colors[x] for x in df_propre['crit_air']]

# print (df_propre)


def carto(df,model):
    # init google map
    # apikey = 'AIzaSyD1p5gcCvLbVqhuqtdMsg_1laPEDAOoXXQ'
    lat0 = df.iloc[0]['lattitude']
    lon0 = df.iloc[0]['longitude']
    
    # instanciation objets
    gmap = gmplot.GoogleMapPlotter(lat0, lon0, 13)#, apikey=apikey)

    m = folium.Map(location=[lat0, lon0], zoom_start=15)

    for commune in df['commune_de_residence'].unique():
        data = df[df['commune_de_residence'] == commune]
        # data = df[df['commune_de_residence'].isin(commune)]
        print ('for commune',df)
        lat0 = data.iloc[0]['lattitude']
        lon0 = data.iloc[0]['longitude']
        shape = data.iloc[0]['geo_shape']
        shape_json = json.loads(shape)
           
        # Récupération des coordonnées du polygone
        polygon_coords = shape_json['coordinates'][0]

        # Séparation des coordonnées en deux listes: lattitudes et longitudes
        lats = [coord[1] for coord in polygon_coords]
        # print(lats)
        lngs = [coord[0] for coord in polygon_coords]
        # print(lngs)

        # Tracé du polygone sur la carte
        gmap.polygon(lats, lngs)
        folium.GeoJson(data=shape_json).add_to(m)
           
        plt.figure(figsize=(2.5, 2.5))
        # Change the font size of the pie chart labels
        plt.rcParams['font.size'] = 8

        data = data.reset_index(drop=True)
        # print('data', data)

        explode_index = data['proportion'].idxmax()

        # Create an "explode" array with a non-zero value for the largest percentage
        explode = [0.1 if i == explode_index else 0 for i in range(len(data))]

        print (data['couleur'])

        plt.pie(data['proportion'], labels=data[model],autopct='%1.1f%%',
                colors=data['couleur'], explode=explode)
        plt.title(commune)

        # Save the plot to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        # Encode the image as a base64 string
        encoded = base64.b64encode(img.read()).decode()

        # Create an HTML img tag using the base64 string
        html = f'<img src="data:image/png;base64,{encoded}">'
 
        # Add a marker for each location in the dfFrame
        gmap.marker(lat0, lon0, info_window=html)
        marker_cluster = MarkerCluster().add_to(m)
        # Create a folium Popup object containing the HTML img tag
        popup = folium.Popup(html, max_width=2650)
        location = lat0,lon0
        # Add a marker to the map with the popup
        folium.Marker(location=location, popup=popup).add_to(marker_cluster)

    # plt.show()
    # Save map
    m.save('folium_map.html')
    # Draw the map to an HTML file
    gmap.draw("google_map.html")
    with open('google_map.html', 'r') as f:
        lines = f.readlines()

    with open('google_map.html', 'w') as f:
        for line in lines:
            if '<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization"></script>' in line:
                # f.write('<div id="carte"></div> <script src="https://cdn.jsdelivr.net/gh/somanchiu/Keyless-Google-Maps-API@v5.9/mapsJavaScriptAPI.js"></script>')
                f.write('<div id="carte"></div> <script src="gm_keyless.js" async defer></script>')
            else:
                f.write(line)

def y_formatter(y, pos):
    return "{:,}".format(int(y)).replace(',', ' ')
    # return f'{(int(y))}'

# Afficher la variation du nb de VL par crit'air ou par carburant en fonction de la region, du departement, des communes, du type d'energie et de la plage d'annees


def sort_par_model_couleur(df,model):
    if model == 'crit_air':
        model_order = {'Crit\'Air E': 0, 'Crit\'Air 1': 1, 'Crit\'Air 2': 2,
                        'Crit\'Air 3': 3, 'Crit\'Air 4': 4, 'Crit\'Air 5': 5, 'Non classé': 6, 'Inconnu': 7}
        df = df.sort_values(by=[model,'Annee'], key=lambda x: x.map(model_order))
        
        # Define colors for each Crit'Air category
        colors = {"Crit'Air E": 'green', "Crit'Air 1": 'purple', "Crit'Air 2": 'yellow', "Crit'Air 3": 'orange',
        "Crit'Air 4": 'maroon', "Crit'Air 5": 'gray', "Inconnu": 'black', "Non classé": 'brown'}
        
        # Add color column based on Crit'Air category
        df['couleur'] = [colors[x] for x in df[model]]
        return df.reset_index(drop=True)
    
    elif model == 'carburant':
        model_order = {'Electrique et hydrogène': 0, 'Hybride rechargeable': 1, 'Gaz et inconnu': 2,
                        'Essence HNR': 3, 'Diesel HNR': 4, 'Essence': 5, 'Diesel': 6}
        df = df.sort_values(by=[model,'Annee'], key=lambda x: x.map(model_order))

        # Define colors for each Crit'Air category
        colors = {"Electrique et hydrogène": 'green', "Hybride rechargeable": 'purple', "Gaz et inconnu": 'yellow', "Essence HNR": 'orange',
        "Diesel HNR": 'maroon', "Essence": 'gray', "Diesel": 'black'}
        
        # Add color column based on Crit'Air category
        df['couleur'] = [colors[x] for x in df[model]]

        return df.reset_index(drop=True)
    else: print ('model inconnu')




def plot_vehicule_evolution(df, model, region=None, departement=None, commune=None, carburant=None, crit_air=None, depart_Annee=None, fin_Annee=None):

    # Transformation du dfFrame en un format long en utilisant la fonction melt()
    df = df.melt(id_vars=['region_de_residence',
                          'departement_de_residence',
                          'commune_de_residence',
                          'carburant',
                          'crit_air',
                          'geo_point_2d',
                          'geo_shape',
                          'lattitude',
                          'longitude'],
                 value_vars=[str(Annee)
                             for Annee in range(depart_Annee, fin_Annee+1)],
                 var_name=[('Annee')], value_name='nombre de véhicules')
    print ('df_melted',df)
    # df.to_csv(p + r'/France_data/df_melted_utf-8_b.csv',encoding="utf-8")
    


    l_col = df.columns
    l_Annees = []

    for element in l_col:
        if element.isdigit():
            l_Annees.append(int(element))

    # print(l_Annees)

    # Si les arguments région, département, commune ou type de carburant sont vides,
    # on leur attribue la valeur du filtre correspondant

    if region == None:
        region_str = 'toutes régions'
    else:
        list_region = region.split(',')
        df = df[df['region_de_residence'].isin(list_region)]
        region_str = ",".join(list_region)
        df0 = df.iloc[0]
        departement_str = str(df0.loc['departement_de_residence'])
        commune_str = str(df0.loc['commune_de_residence'])
        
    if departement == None:
        departement_str = 'tous départements'
    else:
        list_departement = departement.split(',')
        df = df[df['departement_de_residence'].isin(list_departement)]
        departement_str = ",".join(list_departement)
        df0 = df.iloc[0]
        region_str = str(df0.loc['region_de_residence'])
        commune_str = str(df0.loc['commune_de_residence'])
        
    if commune == None:
        commune_str = 'toutes communes'
    else:
        list_commune = commune.split(',')
        df = df[df['commune_de_residence'].isin(list_commune)]
        commune_str = ",".join(list_commune)
        df0 = df.iloc[0]
        region_str = str(df0.loc['region_de_residence'])
        departement_str = str(df0.loc['departement_de_residence'])

    if carburant == None:
        carburant_str = 'tous carburants'
    else:
        list_carburant = carburant.split(',')
        df = df[df['carburant'].isin(list_carburant)]
        carburant_str = ",".join(list_carburant)

    if crit_air == None:
        crit_air_str = "tous Crit'Air"
    else:
        list_crit_air = crit_air.split(',')
        df = df[df['crit_air'].isin(list_crit_air)]
        crit_air_str = ",".join(list_crit_air)

    if depart_Annee is None and fin_Annee is None:
        depart_Annee = l_Annees[0]
        fin_Annee = l_Annees[-1]
    if depart_Annee is None:
        depart_Annee = l_Annees[0]
    if fin_Annee is None:
        fin_Annee = l_Annees[-1]

    
    
    

    # Conversion de la colonne Annee en entier
    # df['Annee'] = df['Annee'].astype(int)

    # df.groupby([model])['nombre de véhicules'].sum().plot.pie(autopct='%1.1f%%')

    # df = df.groupby(['Annee', model, 'geo_point_2d', 'lattitude', 'longitude'])['nombre de véhicules'].sum().reset_index()
    df = df.groupby([ model,'Annee', 'departement_de_residence','commune_de_residence','geo_point_2d', 'geo_shape', 'lattitude', 'longitude'])[
        'nombre de véhicules'].agg(['sum', 'mean', 'min', 'max']).reset_index()
    df = df.rename(columns={'sum': 'nombre de véhicules'})

    df2 = df.groupby([model,'Annee'])['nombre de véhicules'].agg(['sum','max']).reset_index()
    df2 = df2.rename(columns={'sum': 'nombre de véhicules'})
 
    # print(df)

    # df['max'] = df['max'].astype(int)
    # df0 = df.dropna(subset=['max'])
    df = df.loc[(df['max'] != 0)]
    df2 = df2.loc[(df2['max'] != 0)]
    print (df2)
    # df = df.drop(['commune_de_residence','geo_point_2d','geo_shape','lattitude','longitude','mean', 'min', 'max'], axis=1)
    # print ('drop_com',df)
    

    # Tri des données par les colonnes Annee et model
    # df = df.sort_values(by=['Annee', model])
    df = sort_par_model_couleur(df,model)
    df2 = sort_par_model_couleur(df2,model)
    print(df2)

    # df.to_csv(p + r'/France_df/df_MIN_MAX.csv', encoding="utf-8")
    # print(df)

    # Agrandissement du cadre du graphique

    # fig, ax0 = plt.subplots()
    plt.figure(figsize=(15, 8.5))

    # Création d'un graphique en ligne en utilisant la bibliothèque seaborn
    # sns.lineplot(df=df, x='Annee', y='nombre de véhicules', hue=model)
    # sns.barplot(df=df, x='Annee', y='nombre de véhicules', hue=model)
    # sns.cubehelix_palette(start=2, rot=0, dark=0, light=.95, reverse=True, as_cmap=True)

    # ax = sns.barplot(df=df, x='Annee', y='nombre de véhicules',palette="mako", hue=model)
    # palette = ax.palette('mako').reversed()
    # inverted_palette = sns.color_palette(palette)
    # data0 = df2[df2[model] == model]
    # pc = df2['couleur']
    pc = pd.unique(df2['couleur'])
    print (pc)

    sns.barplot(data=df2, x='Annee', y='nombre de véhicules',
                palette=pc, hue=model)
    
    # sns.barplot(data=df, x='Annee', y='nombre de véhicules',
    #             palette=colors, hue=model)

    # sns.barplot(df=df, x='Annee', y='nombre de véhicules',palette="mako", hue=model)#, ax=ax0)

    # ax0.set_ylabel("Sequential")

    # ax1 = ax0.twinx()
    # sns.boxplot(df=df, x='Annee', y='nombre de véhicules',palette="rocket", hue=model, ax=ax1)

    # sns.barplot(df=df, x='Annee', y='nombre de véhicules', hue=model)

    # plt.gca().yaxis.set_ticks(range(0, 100, 10), minor = True)

    # Récupération de l'objet Axes courant
    ax = plt.gca()
    ax.yaxis.set_tick_params(direction='out', length=10, width=5,
                             color='black', labelsize=10, pad=10,
                             labelcolor='blue', right=True, left=True)
    ax.yaxis.set_label_coords(0, 0)

    # Quelle est la variation du nombre de véhicules selon le carburant par région, département, commune ?

    titre = (f"Variation du nombre de véhicules en fonction du type de " +
             f"{model} de {depart_Annee} à {fin_Annee}\n" +
             f"pour {region_str}, {departement_str} / {commune_str} / {crit_air_str}\n" +
             f"{carburant_str}")

    plt.title(titre)

    plt.xlabel('Annee')
    # plt.ylabel('nombre de véhicules',loc='top', rotation=0, fontsize=10, labelpad=-25)
    plt.ylabel('nombre de véhicules', loc='top', rotation=0, fontsize=10)

    # Extraction de la légende du graphique et placement dans un cadre séparé
    leg = plt.legend(bbox_to_anchor=(.95, 1.15),
                     fontsize=7.5,  loc=2, borderaxespad=0)
    ax.add_artist(leg)
    # plt.gca().set_ylim(0, 1000000)

    # Définition des graduations sur l'axe des ordonnées²
    ax.yaxis.set_major_formatter(FuncFormatter(y_formatter))
    # plt.savefig('./png/'+region)
    plt.show()

    

    # Calculate percentage of vehicles in each category
    # df0 = df.groupby('crit_air')['nombre de véhicules'].sum()
    # df0['proportion'] = df0.groupby(['crit_air'])['nombre de véhicules'].apply(lambda x: x / x.sum() * 100)
    # df0.name = 'ma_serie'
    # df0.to_frame("toto")
    
    df['proportion'] = df.groupby('commune_de_residence')['nombre de véhicules'].apply(lambda x: x / x.sum() * 100)
    
    # df2.to_csv(p + r'/France_data/df_proportion2.csv',encoding="utf-8")


    # df['proportion2'] = df.groupby('crit_air')['nombre de véhicules'].sum()
    # df['proportion'] = df['nombre de véhicules'] / df.groupby(['commune_de_residence', 'crit_air'])['nombre de véhicules'].transform('sum') * 100
    # df.to_csv(p + r'/France_data/df_proportion.csv',encoding="utf-8")
    print (df)

    # Sort df by Crit'Air category
    df = sort_par_model_couleur(df,model)
    # df.to_csv(p + r'/France_data/df_proportion.csv',encoding="utf-8")
    carto(df,model)

    

# exemples
# plot_vehicule_evolution(df_propre,'crit_air',None,None,'Menucourt',None,None,2017,None)
# plot_vehicule_evolution(df_propre,'crit_air',None,None,None,None,None,2011)
# plot_vehicule_evolution(df_propre,'carburant',None,None,None,'Hybride rechargeable,Electrique et hydrogène',None)


# region_de_residence = pd.unique(df_propre['region_de_residence'])
# print(region_de_residence)

# carburant = pd.unique(df_propre['carburant'])
# print (carburant)

# for r in region_de_residence:
#     print (r)
#     plot_vehicule_evolution(df_propre,'carburant',r,None,None,None,None,None,2021)
# plot_vehicule_evolution(df_propre,'crit_air',None,None,'Menucourt','Hybride rechargeable,Electrique et hydrogène',None,None,None)
plot_vehicule_evolution(df_propre, 'crit_air', None,
                        'Hauts-de-Seine', None, None, None, 2021, 2021)
# plot_vehicule_evolution(df_propre, 'crit_air', 'Auvergne-Rhône-Alpes',
#                         None, None, None, None, 2020, 2021)
