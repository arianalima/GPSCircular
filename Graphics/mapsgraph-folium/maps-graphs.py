## Criacao mapa de bolha no mapa colorido de acordo com a media pessoas em cada parada em todas as coletas validas

import folium
from folium.plugins import HeatMap
import pandas as pd
import branca.colormap as cm

coletas = pd.read_csv('coletas_reais.csv', header=[0])
coletas['lat'] = coletas['lat'].astype(float)
coletas['long'] = coletas['long'].astype(float)
coletas['media'] = coletas['media'].astype(int)

mapa = folium.Map(location=[-8.0169, -34.94844], zoom_start=15)
mapa_calor = folium.Map(location=[-8.0169, -34.94844], zoom_start=15)

## Mapa de calor
calor = coletas[['lat', 'long', 'media']].values.tolist()
HeatMap(calor, radius=15).add_to(mapa_calor)    

## Cores dos marcadores
cor = cm.linear.YlOrRd_07.scale(0, 35)
cor = cor.to_step(
    n = 5,
    data = list(coletas['media']),
    method = 'quantiles',
    round_method = 'int'
)
cor.caption = 'Quantidade média de pessoas por parada'
mapa.add_child(cor)

##  Cria as bolhas no mapa
def marcar(parada, media, lat, long):
        folium.CircleMarker(
            location = [lat, long],
            popup = "<b>" + parada + "</b><br/>" + "media: " + str(media),
            fill = True,
            fill_opacity = 0.4,
            fill_color = cor(media),
            color = cor(media),
            radius = media
        ).add_to(mapa)

## Pega apenas os dados relevante ao grafico
def get_dados(x):
    marcar(x['parada'],x['media'],x['lat'],x['long'])
    
## Passa os dados de todas as paradas e de todas as coletas
list(map(lambda linha: get_dados(linha[1]), coletas.iterrows()))

mapa.save('media-coletas-bolha.html')
mapa_calor.save('media-coletas-heatmap.html')
