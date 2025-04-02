import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import math
import base64

# Função para carregar a imagem e convertê-la para base64
def get_base64_of_image(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Definir o background com a imagem convertida em base64
def set_background(image_file):
    base64_str = get_base64_of_image(image_file)
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    .title-box {{
        background: rgba(0, 0, 0, 0.6);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: bold;
        width: 60%;
        margin: auto;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Aplicando o background
set_background("bg.jpg")

# Função para obter coordenadas a partir do CEP
def obter_coordenadas_cep(cep):
    url = f"https://cep.awesomeapi.com.br/json/{cep}"
    response = requests.get(url)
    if response.status_code == 200:
        dados_cep = response.json()
        return float(dados_cep['lat']), float(dados_cep['lng'])
    else:
        st.error(f"Erro ao obter dados do CEP. Código de status: {response.status_code}")
        return None

# Função para calcular distância usando a fórmula de Haversine
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  # Raio da Terra em quilômetros
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Função principal
def main():
    st.markdown('<div class="title-box">App de Distância entre CEPs</div>', unsafe_allow_html=True)
    
    cep1 = st.text_input("Digite o primeiro CEP:")
    cep2 = st.text_input("Digite o segundo CEP:")
    
    if st.button("Calcular Distância"):
        if cep1 and cep2:
            coords1 = obter_coordenadas_cep(cep1)
            coords2 = obter_coordenadas_cep(cep2)
            if coords1 and coords2:
                distancia = calcular_distancia(*coords1, *coords2)
                st.write(f"**Distância entre os CEPs:** {distancia:.2f} km")
                
                # Exibir mapa com os dois pontos
                m = folium.Map(location=[(coords1[0] + coords2[0]) / 2, (coords1[1] + coords2[1]) / 2], zoom_start=6)
                folium.Marker(location=coords1, popup=f"CEP 1: {coords1[0]}, {coords1[1]}", icon=folium.Icon(color='blue')).add_to(m)
                folium.Marker(location=coords2, popup=f"CEP 2: {coords2[0]}, {coords2[1]}", icon=folium.Icon(color='red')).add_to(m)
                folium_static(m)
        else:
            st.warning("Insira os dois CEPs para calcular a distância.")

if __name__ == "__main__":
    main()
