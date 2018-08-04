## Criacao mapa de bolha no mapa colorido de acordo com a media pessoas em cada parada em todas as coletas validas

import folium
from folium.plugins import HeatMap
import pandas as pd

coletas = pd.read_csv('coletas_reais.csv', header=[0])

mapa = folium.Map(location=[-8.0169, -34.94844], zoom_start=15)
mapa_calor = folium.Map(location=[-8.0169, -34.94844], zoom_start=15)

coletas['lat'] = coletas['lat'].astype(float)
coletas['long'] = coletas['long'].astype(float)
coletas['media'] = coletas['media'].astype(float)

## Mapa de calor
calor = coletas[['lat', 'long', 'media']].values.tolist()
HeatMap(calor, radius=15).add_to(mapa_calor)    

## Verifica a media e retorna uma cor correspondente
def colorir(media):
    if media in list(range(0,15)):
        return 'blue'
    elif media in list(range(15,20)):
        return 'yellow'
    else:
        return 'red'
    
##  Cria as bolhas no mapa
def marcar(parada, media, lat, long):
        folium.CircleMarker(
            location = [lat, long],
            popup = "<b>" + parada + "</b><br/>" + "media: " + str(media),
            fill = True,
            fill_opacity=0.4,
            color = colorir(media),
            fill_color = colorir(media),
            radius = media
        ).add_to(mapa)

## Pega apenas os dados relevante ao grafico
def get_dados(x):
    marcar(x['parada'],x['media'],x['lat'],x['long'])
    
## Passa os dados de todas as paradas e de todas as coletas
list(map(lambda linha: get_dados(linha[1]), coletas.iterrows()))

mapa.save('media-coletas-bolha.html')
mapa_calor.save('media-coletas-heatmap.html')
