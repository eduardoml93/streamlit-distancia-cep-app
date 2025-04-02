import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import math
from PIL import Image
import base64

# Desativar a observação de arquivos para o Streamlit no Docker
# st.set_option('server.headless', True)

# Read and decode the image using PIL
image_path = './static/bg.jpg'
# image = Image.open(image_path)

# Display the decoded image using st.image
# st.image(image, use_column_width=True)

# Function to get base64 of binary file

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Get base64 string of the image
image_base64 = get_base64_of_bin_file('./static/bg.jpg')

# Use the base64 string in the CSS for background
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/jpeg;base64,{image_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
</style>
""", unsafe_allow_html=True)

# Function to fetch coordinates from CEP API

def obter_coordenadas_cep(cep):
    url = f"https://cep.awesomeapi.com.br/json/{cep}"
    response = requests.get(url)
    if response.status_code == 200:
        dados_cep = response.json()
        return float(dados_cep['lat']), float(dados_cep['lng'])
    else:
        st.error(f"Erro ao obter dados do CEP. Código de status: {response.status_code}")
        return None

# Function to calculate distance using Haversine formula

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c
    return distancia

# Update main function to accept two CEP inputs and display distance

def main():
    st.title("App de Distância entre CEPs")

    # Inserir os CEPs
    cep1 = st.text_input("Digite o primeiro CEP:")
    cep2 = st.text_input("Digite o segundo CEP:")

    # Botão para calcular a distância
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
