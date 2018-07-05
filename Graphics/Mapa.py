import pandas as pd
import folium

mapa = folium.Map(location=[-8.0175094,-34.9492219],zoom_start=16)

#ceagri
folium.Marker(([-8.01785, -34.9447]),
popup='ceagri').add_to(mapa)

#cegoe
folium.Marker(([-8.01754, -34.95028]),
popup='cegoe').add_to(mapa)

#zootecnia
folium.Marker(([-8.02007, -34.95384]),
popup='zootecnia').add_to(mapa)

#central
folium.Marker(([-8.01453, -34.9504]),
popup='central',
icon=folium.Icon(color='red')).add_to(mapa)

#guarita/central
folium.Marker(([-8.01609, -34.95083]),
popup='guarita central').add_to(mapa)

#retorno/pesca
folium.Marker(([-8.0196, -34.94418]),
popup='pesca').add_to(mapa)

#veterinaria
folium.Marker(([-8.01507, -34.94784]),
popup='veterinária').add_to(mapa)

#guarita zootecnia
folium.Marker(([-8.02001, -34.95443]),
popup='guarita zootecnia').add_to(mapa)

#biblioteca setorial
folium.Marker(([-8.0164, -34.94904]),
popup='biblioteca setorial').add_to(mapa)

#prefeitura
folium.Marker(([-8.01956, -34.94891]),
popup='prefeitura').add_to(mapa)

mapa
mapa.save("locais_parada.html")


