import streamlit as st
import pandas as pd
from PIL import Image
import requests
import re
from collections import defaultdict


# Activer le mode large
st.set_page_config(layout="wide")




@st.cache_data
def load_data():
    # Charger uniquement les colonnes nécessaires
    Fifa = pd.read_csv("data/FIFA.csv")
    
    # Appliquer la logique de classification des pays
    country_mapping = {
    "Nigeria": "Nigeria|Abuja|Lagos|Kaduna|Ibadan|Kano|Port Harcourt|Enugu|Lekki|Gombe|Ikeja|Benin-City|Tema",
    "United Kingdom": "England|UK|London|Manchester|Sheffield|Newcastle Upon Tyne|Leeds|West Midlands|Nottingham|South East|Liverpool|Old Trafford|Leicester|Bristol|North East|Birmingham|Stamford Bridge|Brighton|Norwich|Oxford|Southampton|Hull|York|Bolton|Stoke-on-Trent",
    "India": "India|Hyderabad|New Delhi|Pune|Bangalore|Kerala|Delhi|Ahmadabad City|Jaipur|Chandigarh",
    "United States": "USA|America|New York|Los Angeles|Austin|Philadelphia|San Diego|California|Georgia|Chicago|San Antonio|Orlando|Virginia|Portland|Maryland|North Carolina|Denver|Charlotte|Phoenix|Columbus|Pittsburgh|Massachusetts|Miami|Tampa|Ohio|Minnesota|Fort Worth|Long Beach|Seattle|Bay Area|Detroit|Raleigh|Buffalo|Oakland|Kansas City|Cincinnati|San Francisco|New Orleans|Houston|Washington DC",
    "France": "France|Paris|Ile-de-France|Lyon|Marseille|Lille",
    "Indonesia": "Indonesia|Jakarta|Yogyakarta|DKI Jakarta|Jakarta Capital Region|Bandung|Kota Surabaya|Bekasi|Batu|Tangerang|Jakarta Selatan",
    "Pakistan": "Pakistan|Islamabad|Karachi|Lahore|Punjab|Rawalpindi",
    "Canada": "Canada|Toronto|Ontario|Montréal|Vancouver|British Columbia|Ottawa|Edmonton",
    "Australia": "Australia|Sydney|Melbourne|New South Wales|Victoria|Brisbane",
    "Ghana": "Ghana|Accra|Greater Accra|Kumasi|Port Harcourt|Kingston|Enugu|Lekki|Gombe|Ikeja|Nakuru",
    "Brazil": "Brazil|Rio de Janeiro|São Paulo|Porto Alegre|Curitiba|Salvador|Recife|Manaus|Fortaleza|Brasília|Belém|Belo Horizonte|Campinas|Goiânia|Campo Grande|Sorocaba",
    "Philippines": "Philippines|Republic of the Philippines|Manila",
    "South Korea": "South Korea|Seoul|Republic of Korea",
    "Bangladesh": "Bangladesh|Dhaka|Chattogram",
    "Argentina": "Argentina|Buenos Aires",
    "Uruguay": "Uruguay|uruguay|URUGUAY",
    "Mexico": "Mexico|Mexico City|Ciudad de México|Puebla",
    "Egypt": "Egypt|Alexandria",
    "South Africa": "South Africa|Cape Town|Bloemfontein|Port Elizabeth|East London|Pretoria|Johannesburg|Durban|Soweto|Polokwane|Rustenburg|Pietermaritzburg",
    "Ireland": "Ireland|Dublin|Cork",
    "Germany": "Germany|Deutschland|Berlin",
    "Croatia": "Croatia|Zagreb",
    "Sweden": "Sweden|sweden|suede|sueden",
    "Scotland": "Scotland|Edinburgh|Glasgow",
    "Colombia": "Colombia|colombia|Colombia|Colombie",
    "Russia": "Russia|Moscow",
    "Japan": "Japan|Tokyo",
    "Peru": "Peru|Lima",
    "Chile": "Chile|Santiago",
    "Wales": "Wales|Cardiff",
    "Spain": "Spain|Barcelona|Madrid",
    "Belgium": "Belgium|Brussels",
    "Malaysia": "Malaysia|Johore|Perak|Kelantan|Kuching|Kedah|Johor Bahru|Bat",
    "Ecuador": "Ecuador|Guayaquil",
    "Panama": "Panamá",
    "Poland": "Poland",
    "Kuwait": "Kuwait",
    "Italy": "Italy|Milan",
    "Jamaica": "Jamaica|Kingston",
    "Costa Rica": "Costa Rica|costa Rica|costa rica",
    "Kenya": "Kenya|Mombasa|Nakuru",
    "Serbia": "Serbia|serbia",
    "Senegal": "Senegal|senegal",
    "Egypt": "Egypte|egypte",
    "Morocco": "Maroc|Moroco",
    "Portugal": "Portugal|portugal",
    "Iceland": "Island|island|islands|Islands|ISLANDS",
    "Tunisia": "Tunisia|tunisia|Tunis|tunis|Tunisie|tunisie",
    "Saudi Arabia": "Kingdom of Saudi Arabia|Saudi Arabia|saudi arabia|Kingdom of Saudi Arabia|Kingdom of Saudi Arabi|Saudi Arabia",
    "Switzerland": "Switzerland|suisse|Suisse|switzerland",
    "Iran": "Iran|iran",
    "Peru": "Peru|peru|PERU",
}
    country_coords = {
    "Nigeria": (9.0820, 8.6753),
    "United Kingdom": (55.3781, -3.4360),
    "India": (20.5937, 78.9629),
    "United States of America": (37.0902, -95.7129),
    "France": (46.6035, 1.8883),
    "Indonesia": (-0.7893, 113.9213),
    "Pakistan": (30.3753, 69.3451),
    "Canada": (56.1304, -106.3468),
    "Australia": (-25.2744, 133.7751),
    "Ghana": (7.9465, -1.0232),
    "Brazil": (-14.2350, -51.9253),
    "Philippines": (12.8797, 121.7740),
    "South Korea": (35.9078, 127.7669),
    "Bangladesh": (23.6850, 90.3563),
    "Argentina": (-38.4161, -63.6167),
    "Uruguay": (-32.5228, -55.7658),
    "Mexico": (23.6345, -102.5528),
    "Egypt": (26.8206, 30.8025),
    "South Africa": (-30.5595, 22.9375),
    "Ireland": (53.4129, -8.2439),
    "Germany": (51.1657, 10.4515),
    "Croatia": (45.1000, 15.2000),
    "Sweden": (60.1282, 18.6435),
    "Scotland": (56.4907, -4.2026),
    "Colombia": (4.5709, -74.2973),
    "Russia": (61.5240, 105.3188),
    "Japan": (36.2048, 138.2529),
    "Peru": (-9.1899, -75.0152),
    "Chile": (-35.6751, -71.5430),
    "Wales": (52.1307, -3.7837),
    "Spain": (40.4637, -3.7492),
    "Belgium": (50.5039, 4.4699),
    "Malaysia": (4.2105, 101.9758),
    "Ecuador": (-1.8312, -78.1834),
    "Panama": (8.5380, -80.7821),
    "Poland": (51.9194, 19.1451),
    "Kuwait": (29.3117, 47.4818),
    "Italy": (41.8719, 12.5674),
    "Jamaica": (18.1096, -77.2975),
    "Costa Rica": (9.7489, -83.7534),
    "Kenya": (-0.0236, 37.9062),
    "Serbia": (44.0165, 21.0059),
    "Senegal": (14.4974, -14.4524),
    "Morocco": (31.7917, -7.0926),
    "Portugal": (39.3999, -8.2245),
    "Iceland": (64.9631, -19.0208),
    "Tunisia": (33.8869, 9.5375),
    "Saudi Arabia": (23.8859, 45.0792),
    "Switzerland": (46.8182, 8.2275),
    "Iran": (32.4279, 53.6880),
}
    
    def classify_country(place):
        for country, pattern in country_mapping.items():
            if re.search(pattern, str(place), re.IGNORECASE):
                return country
        return "Others"

    Fifa['Country'] = Fifa['Place'].apply(classify_country)
    
    # Filtrer les données pour exclure "Others"
    Fifa_clean = Fifa[Fifa['Country'] != "Others"]

    return Fifa_clean, country_coords

logo_image = Image.open("wordcup.png")
logo_resized = logo_image.resize((50, 50))

phases = ["Tous", "Huitièmes de finale", "Quarts de finale", "Demi-finales", "Finale"]

with st.sidebar:
    col1,col2= st.columns([8,12])
    col1.image(logo_resized)
    col2.markdown('<span style="font-weight: bold; font-size: large; display: inline-block; vertical-align: middle;">World Cup</span>', unsafe_allow_html=True)
    # Ajouter un filtre pour les phases

def main():
    st.title("FIFA World Cup Data Analysis")
    data, country_coords = load_data()
    
    # Display the data
    st.dataframe(data)
    
    # Add more Streamlit components as needed
    # ...

if __name__ == "__main__":
    main()