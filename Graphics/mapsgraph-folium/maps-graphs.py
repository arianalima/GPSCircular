## Criacao mapa de bolha no mapa colorido de acordo com a media pessoas em cada parada em todas as coletas validas

import folium
from folium.plugins import HeatMap
import pandas as pd
import branca.colormap as cm

coletas = pd.read_csv('coletas_reais.csv', header=[0])
coletas['lat'] = coletas['lat'].astype(float)
coletas['long'] = coletas['long'].astype(float)
coletas['media'] = coletas['media'].astype(int)
coletas['coletas'] = coletas['coletas'].astype(int)

mapa_media = folium.Map(location=[-8.0169, -34.94844], zoom_start=15)
mapa_coletas = folium.Map(location=[-8.0169, -34.94844], zoom_start=15)
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
mapa_coletas.add_child(cor)
mapa_media.add_child(cor)


##  Cria as bolhas no mapa
def marcar(parada, dado, lat, long, mapa):
        if mapa == mapa_media:
                popup_dado = "<b>" + parada + "</b><br/>" + "media: " + str(dado)
        elif mapa == mapa_coletas:
                popup_dado = "<b>" + parada + "</b><br/>" + "quantidade: " + str(dado)
        folium.CircleMarker(
            location = [lat, long],
            popup = popup_dado,
            fill = True,
            fill_opacity = 0.4,
            fill_color = cor(dado),
            color = cor(dado),
            radius = dado
        ).add_to(mapa)

## Pega apenas os dados relevante ao grafico
def get_dados_media(x):
    marcar(x['parada'], x['media'], x['lat'], x['long'], mapa_media)

def get_dados_coletas(x):
    marcar(x['parada'], x['coletas'], x['lat'], x['long'], mapa_coletas)
    
## Passa os dados de todas as paradas e de todas as coletas
list(map(lambda linha: get_dados_media(linha[1]), coletas.iterrows()))
list(map(lambda linha: get_dados_coletas(linha[1]), coletas.iterrows()))

mapa_media.save('media-coletas-bolha.html')
mapa_coletas.save('contagem-bolha.html')
mapa_calor.save('media-coletas-heatmap.html')
