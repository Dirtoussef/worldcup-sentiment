import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import geopandas as gpd
from geopy.geocoders import Nominatim
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re


# Charger les données
Fifa = pd.read_csv("data/FIFA.csv")

# Nettoyer les données
Fifa18 = Fifa.copy()
Fifa18['Country'] = Fifa18['Place'].apply(lambda x: 
    "Nigeria" if re.search("Nigeria|Abuja|Lagos|Kaduna|Ibadan|Kano|Port Harcourt|Enugu|Lekki|Gombe|Ikeja|Benin-City|Tema", str(x)) else
    "United Kingdom" if re.search("England|UK|London|Manchester|Sheffield|Newcastle Upon Tyne|Leeds|West Midlands|Nottingham|South East|Liverpool|Old Trafford|Leicester|Bristol|North East|Birmingham|Stamford Bridge|Brighton|Norwich|Oxford|Southampton|Hull|York|Bolton|Stoke-on-Trent", str(x)) else
    "India" if re.search("India|Hyderabad|New Delhi|Pune|Bangalore|Kerala|Delhi|Ahmadabad City|Jaipur|Chandigarh", str(x)) else
    "United States" if re.search("USA|America|New York|Los Angeles|Austin|Philadelphia|San Diego|California|Georgia|Chicago|San Antonio|Orlando|Virginia|Portland|Maryland|North Carolina|Denver|Charlotte|Phoenix|Columbus|Pittsburgh|Massachusetts|Miami|Tampa|Ohio|Minnesota|Fort Worth|Long Beach|Seattle|Bay Area|Detroit|Raleigh|Buffalo|Oakland|Kansas City|Cincinnati|San Francisco|New Orleans|Houston|Washington DC", str(x)) else
    "France" if re.search("France|Paris|Ile-de-France|Lyon|Marseille|Lille", str(x)) else
    "Indonesia" if re.search("Indonesia|Jakarta|Yogyakarta|DKI Jakarta|Jakarta Capital Region|Bandung|Kota Surabaya|Bekasi|Batu|Tangerang|Jakarta Selatan", str(x)) else
    "Pakistan" if re.search("Pakistan|Islamabad|Karachi|Lahore|Punjab|Rawalpindi", str(x)) else
    "Canada" if re.search("Canada|Toronto|Ontario|Montréal|Vancouver|British Columbia|Ottawa|Edmonton", str(x)) else
    "Australia" if re.search("Australia|Sydney|Melbourne|New South Wales|Victoria|Brisbane", str(x)) else
    "Ghana" if re.search("Ghana|Accra|Greater Accra|Kumasi|Port Harcourt|Kingston|Enugu|Lekki|Gombe|Ikeja|Nakuru", str(x)) else
    "Brazil" if re.search("Brazil|Rio de Janeiro|São Paulo|Porto Alegre|Curitiba|Salvador|Recife|Manaus|Fortaleza|Brasília|Belém|Belo Horizonte|Campinas|Goiânia|Campo Grande|Sorocaba", str(x)) else
    "Philippines" if re.search("Philippines|Republic of the Philippines|Manila", str(x)) else
    "South Korea" if re.search("South Korea|Seoul|Republic of Korea", str(x)) else
    "Bangladesh" if re.search("Bangladesh|Dhaka|Chattogram", str(x)) else
    "Argentina" if re.search("Argentina|Buenos Aires", str(x)) else
    "Uruguay" if re.search("Uruguay|uruguay|URUGUAY", str(x)) else
    "Mexico" if re.search("Mexico|Mexico City|Ciudad de México|Puebla", str(x)) else
    "Egypt" if re.search("Egypt|Alexandria", str(x)) else
    "South Africa" if re.search("South Africa|Cape Town|Bloemfontein|Port Elizabeth|East London|Pretoria|Johannesburg|Durban|Soweto|Polokwane|Rustenburg|Pietermaritzburg", str(x)) else
    "Ireland" if re.search("Ireland|Dublin|Cork", str(x)) else
    "Germany" if re.search("Germany|Deutschland|Berlin", str(x)) else
    "Croatia" if re.search("Croatia|Zagreb", str(x)) else
    "Sweden" if re.search("Sweden|sweden|suede|sueden", str(x)) else
    "Scotland" if re.search("Scotland|Edinburgh|Glasgow", str(x)) else
    "Colombia" if re.search("Colombia|colombia|Colombia|Colombie", str(x)) else
    "Russia" if re.search("Russia|Moscow", str(x)) else
    "Japan" if re.search("Japan|Tokyo", str(x)) else
    "Peru" if re.search("Peru|Lima", str(x)) else
    "Chile" if re.search("Chile|Santiago", str(x)) else
    "Wales" if re.search("Wales|Cardiff", str(x)) else
    "Spain" if re.search("Spain|Barcelona|Madrid", str(x)) else
    "Belgium" if re.search("Belgium|Brussels", str(x)) else
    "Malaysia" if re.search("Malaysia|Johore|Perak|Kelantan|Kuching|Kedah|Johor Bahru|Bat", str(x)) else
    "Ecuador" if re.search("Ecuador|Guayaquil", str(x)) else
    "Panama" if re.search("Panamá", str(x)) else
    "Poland" if re.search("Poland", str(x)) else
    "Kuwait" if re.search("Kuwait", str(x)) else
    "Italy" if re.search("Italy|Milan", str(x)) else
    "Jamaica" if re.search("Jamaica|Kingston", str(x)) else
    "Costa Rica" if re.search("Costa Rica|costa Rica|costa rica", str(x)) else
    "Kenya" if re.search("Kenya|Mombasa|Nakuru", str(x)) else
    "Serbia" if re.search("Serbia|serbia", str(x)) else
    "Senegal" if re.search("Senegal|senegal", str(x)) else
    "Egypt" if re.search("Egypte|egypte", str(x)) else
    "Morocco" if re.search("Maroc|Moroco", str(x)) else
    "Portugal" if re.search("Portugal|portugal", str(x)) else
    "Iceland" if re.search("Island|island|islands|Islands|ISLANDS", str(x)) else
    "Tunisia" if re.search("Tunisia|tunisia|Tunis|tunis|Tunisie|tunisie", str(x)) else
    "Saudi Arabia" if re.search("Kingdom of Saudi Arabia|Saudi Arabia|saudi arabia|Kingdom of Saudi Arabia|Kingdom of Saudi Arabi|Saudi Arabia", str(x)) else
    "Switzerland" if re.search("Switzerland|suisse|Suisse|switzerland", str(x)) else
    "Iran" if re.search("Iran|iran", str(x)) else
    "Peru" if re.search("Peru|peru|PERU", str(x)) else
    "Others"
)


# Filtrer les données
Fifa_clean = Fifa18[Fifa18['Country'] != "Others"]

# Ajouter une colonne pour la source nettoyée
Fifa_clean['Source_Cleaned'] = Fifa_clean['Source'].apply(lambda x: x if x in ["Twitter for Android", "Twitter Web Client", "Twitter for iPhone", "Twitter Lite", "Twitter for iPad"] else "Other")

# Classer les tweets par phase du tournoi
huitieme_debut = pd.to_datetime("2018-06-29")
huitieme_fin = pd.to_datetime("2018-07-04")
demi_debut = pd.to_datetime("2018-07-10")
demi_fin = pd.to_datetime("2018-07-11")
finale = pd.to_datetime("2018-07-15")

Fifa_clean['Phase'] = Fifa_clean['Date'].apply(lambda x: 
    "Huitièmes de finale" if huitieme_debut <= pd.to_datetime(x) <= huitieme_fin else
    "Quarts de finale" if huitieme_fin < pd.to_datetime(x) < demi_debut else
    "Demi-finales" if demi_debut <= pd.to_datetime(x) <= demi_fin else
    "Finale" if pd.to_datetime(x) == finale else None
)

# Analyser les sentiments
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
Fifa_clean['Tweet'] = Fifa_clean['Tweet'].fillna("")

Fifa_clean['Sentiment'] = Fifa_clean['Tweet'].apply(lambda x: sia.polarity_scores(x)['compound'])
Fifa_clean['Sentiment_Category'] = Fifa_clean['Sentiment'].apply(lambda x: 
    "Positif" if x > 0.05 else
    "Négatif" if x < -0.05 else
    "Neutre"
)


# Titre de l'application
st.title("Analyse des Tweets de la Coupe du Monde FIFA 2018")

# Onglets
tabs = ["Introduction", "Carte des Tweets", "Carte de Sentiment", "Répartition des Sentiments", "Nuage de Mots", "Statistiques", "Analyse des Top Hashtags"]
selected_tab = st.sidebar.selectbox("Choisissez un onglet", tabs)

if selected_tab == "Introduction":
    st.header("Introduction")
    st.write("Cette application analyse les tweets liés à la Coupe du Monde FIFA 2018.")
    st.image("parcours.webp", caption="Parcours de la Coupe du Monde 2018", use_column_width=True)
    st.write("Les données proviennent de Kaggle et incluent des tweets collectés pendant le tournoi.")

elif selected_tab == "Carte des Tweets":
    st.header("Carte des Tweets")
    source = st.selectbox("Choisissez la source:", ["Tous"] + list(Fifa_clean['Source_Cleaned'].unique()))
    phase = st.selectbox("Choisissez la phase:", ["Toutes"] + list(Fifa_clean['Phase'].unique()))

    # Filtrer les données
    filtered_data = Fifa_clean
    if source != "Tous":
        filtered_data = filtered_data[filtered_data['Source_Cleaned'] == source]
    if phase != "Toutes":
        filtered_data = filtered_data[filtered_data['Phase'] == phase]

    # Afficher la carte
    m = folium.Map(location=[0, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in filtered_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row['Tweet']
        ).add_to(marker_cluster)
    folium_static(m)

elif selected_tab == "Carte de Sentiment":
    st.header("Carte de Sentiment")
    source = st.selectbox("Choisissez la source:", ["Tous"] + list(Fifa_clean['Source_Cleaned'].unique()))
    phase = st.selectbox("Choisissez la phase:", ["Toutes"] + list(Fifa_clean['Phase'].unique()))

    # Filtrer les données
    filtered_data = Fifa_clean
    if source != "Tous":
        filtered_data = filtered_data[filtered_data['Source_Cleaned'] == source]
    if phase != "Toutes":
        filtered_data = filtered_data[filtered_data['Phase'] == phase]

    # Afficher la carte des sentiments
    m = folium.Map(location=[0, 0], zoom_start=2)
    for idx, row in filtered_data.iterrows():
        color = "green" if row['Sentiment_Category'] == "Positif" else "red" if row['Sentiment_Category'] == "Négatif" else "blue"
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            popup=row['Tweet']
        ).add_to(m)
    folium_static(m)

elif selected_tab == "Répartition des Sentiments":
    st.header("Répartition des Sentiments")
    countries = st.multiselect("Choisissez les pays:", ["Tous"] + list(Fifa_clean['Country'].unique()))

    # Filtrer les données
    if "Tous" in countries:
        filtered_data = Fifa_clean
    else:
        filtered_data = Fifa_clean[Fifa_clean['Country'].isin(countries)]

    # Afficher la répartition des sentiments
    sentiment_distribution = filtered_data.groupby(['Country', 'Phase', 'Sentiment_Category']).size().unstack().fillna(0)
    st.bar_chart(sentiment_distribution)

elif selected_tab == "Nuage de Mots":
    st.header("Nuage de Mots")
    min_freq = st.slider("Fréquence minimale des mots:", 1, 100, 2)
    max_words = st.slider("Nombre maximal de mots:", 1, 300, 100)
    phase = st.selectbox("Choisissez la phase:", ["Tous"] + list(Fifa_clean['Phase'].unique()))

    # Filtrer les données
    if phase != "Tous":
        filtered_data = Fifa_clean[Fifa_clean['Phase'] == phase]
    else:
        filtered_data = Fifa_clean

    # Générer le nuage de mots
    text = " ".join(filtered_data['Tweet'])
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=max_words, min_font_size=min_freq).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)

elif selected_tab == "Statistiques":
    st.header("Statistiques")
    graph_type = st.selectbox("Choisissez le graphique à afficher:", [
        "Top 10 Influenceurs FIFA par Retweets",
        "Top Source par Nombre de Tweets",
        "Top utilisateurs par Followers"
    ])

    if graph_type == "Top 10 Influenceurs FIFA par Retweets":
        top_retweets = Fifa_clean.groupby('UserMentionNames')['RTs'].sum().nlargest(10)
        st.bar_chart(top_retweets)

    elif graph_type == "Top Source par Nombre de Tweets":
        top_sources = Fifa_clean['Source_Cleaned'].value_counts().nlargest(10)
        st.bar_chart(top_sources)

    elif graph_type == "Top utilisateurs par Followers":
        top_followers = Fifa_clean.groupby('UserMentionNames')['Followers'].max().nlargest(10)
        st.bar_chart(top_followers)

elif selected_tab == "Analyse des Top Hashtags":
    st.header("Analyse des Top Hashtags")
    n_top_hashtags = st.number_input("Nombre de top hashtags à afficher:", min_value=5, max_value=50, value=10, step=5)
    metric = st.radio("Filtrer par:", ["Likes", "Retweets"])
    color_palette = st.selectbox("Choisissez une palette de couleurs:", ["Blues", "Reds", "Greens", "Spectral"])

    # Analyser les hashtags
    hashtags = Fifa_clean['Hashtags'].str.split(',').explode().str.strip()
    hashtags = hashtags[hashtags != ""]
    if metric == "Likes":
        top_hashtags = Fifa_clean.groupby(hashtags)['Likes'].sum().nlargest(n_top_hashtags)
    else:
        top_hashtags = Fifa_clean.groupby(hashtags)['RTs'].sum().nlargest(n_top_hashtags)

    # Afficher le graphique
    fig, ax = plt.subplots()
    sns.barplot(x=top_hashtags.values, y=top_hashtags.index, palette=color_palette.lower(), ax=ax)
    st.pyplot(fig)


