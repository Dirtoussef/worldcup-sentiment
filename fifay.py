import streamlit as st
import pandas as pd
import requests
from textblob import TextBlob
from appfifa import load_data, phases
import matplotlib.pyplot as plt
from collections import defaultdict
from wordcloud import WordCloud
import numpy as np
import seaborn as sns

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False
if 'country_coords' not in st.session_state:
    st.session_state['country_coords'] = None

# Classer les tweets par phase du tournoi
@st.cache_data
def classify_phases(Fifa_clean):
    huitieme_debut = pd.to_datetime("2018-06-29")
    huitieme_fin = pd.to_datetime("2018-07-04")
    demi_debut = pd.to_datetime("2018-07-10")
    demi_fin = pd.to_datetime("2018-07-11")
    finale = pd.to_datetime("2018-07-15")

    Fifa_clean['Phase'] = Fifa_clean['Date'].apply(lambda x: 
        "Huitièmes de finale" if huitieme_debut <= pd.to_datetime(x) <= huitieme_fin else
        "Quarts de finale" if huitieme_fin < pd.to_datetime(x) < demi_debut else
        "Demi-finales" if demi_debut <= pd.to_datetime(x) <= demi_fin else
        "Finale" if pd.to_datetime(x) >= finale else "Tous"
    )
    return Fifa_clean

# Calculer le sentiment des tweets
def calculate_sentiment(text):
    analysis = TextBlob(str(text))
    return analysis.sentiment.polarity    

# Ajouter une colonne pour la catégorie de sentiment
def categorize_sentiment(polarity):
    return "Positif" if polarity > 0.05 else ("Négatif" if polarity < -0.05 else "Neutre")

# Pré-calculer et mettre en cache les données filtrées pour chaque phase
@st.cache_data
def precompute_filtered_data(Fifa_clean):
    Fifa_clean['Sentiment'] = Fifa_clean['Tweet'].apply(calculate_sentiment)
    Fifa_clean['Sentiment_Category'] = Fifa_clean['Sentiment'].apply(categorize_sentiment)
    
    filtered_data_dict = {}
    phases = ["Tous", "Huitièmes de finale", "Quarts de finale", "Demi-finales", "Finale"]
    
    for phase in phases:
        if phase == "Tous":
            phase_data = Fifa_clean
        else:
            phase_data = Fifa_clean[Fifa_clean['Phase'] == phase]
        
        tweet_count_filtered = phase_data.groupby('Country').size().reset_index(name='Tweet_Count')
        sentiment_category_filtered = phase_data.groupby('Sentiment_Category').size().reset_index(name='Count')
        sentiment_by_country = phase_data.groupby('Country')['Sentiment'].mean().reset_index(name='Sentiment_Mean')
        
        filtered_data_dict[phase] = {
            'tweet_count_filtered': tweet_count_filtered,
            'sentiment_category_filtered': sentiment_category_filtered,
            'sentiment_by_country': sentiment_by_country,
            'phase_data': phase_data
        }
    
    return filtered_data_dict

# Charger les données et les mettre en cache
@st.cache_data(hash_funcs={pd.DataFrame: lambda _: None})
def load_data_wrapper():
    Fifa_clean, country_coords = load_data()
    Fifa_clean = classify_phases(Fifa_clean)
    return precompute_filtered_data(Fifa_clean), country_coords

# Charger les données
if not st.session_state['data_loaded']:
    filtered_data_dict, country_coords = load_data_wrapper()
    st.session_state['data_loaded'] = True
    st.session_state['filtered_data_dict'] = filtered_data_dict
    st.session_state['country_coords'] = country_coords
else:
    filtered_data_dict = st.session_state['filtered_data_dict']
    country_coords = st.session_state['country_coords']

# Titre de l'application
st.title("Analyse des Tweets de la Coupe du Monde FIFA 2018")

# Ajouter un filtre pour les phases dans la sidebar
with st.sidebar:
    selected_phase = st.selectbox("Sélectionnez une phase", phases, key="phase_selectbox")

# Accès aux données via session_state
filtered_data = filtered_data_dict[selected_phase]
tweet_count_filtered = filtered_data['tweet_count_filtered']
sentiment_category_filtered = filtered_data['sentiment_category_filtered']
sentiment_by_country = filtered_data['sentiment_by_country']
phase_data = filtered_data['phase_data']

# Convertir tweet_count_filtered en un dictionnaire pour une recherche facile
tweet_data = dict(zip(tweet_count_filtered['Country'], tweet_count_filtered['Tweet_Count']))

# Ajouter le sentiment moyen par pays dans le dictionnaire
sentiment_data = dict(zip(sentiment_by_country['Country'], sentiment_by_country['Sentiment_Mean']))

# Paramètres du Word Cloud
st.sidebar.header("Paramètres du Word Cloud")
min_freq = st.sidebar.slider("Fréquence minimale des mots", min_value=1, max_value=100, value=2)
max_words = st.sidebar.slider("Nombre maximal de mots", min_value=1, max_value=300, value=100)

def generate_wordcloud(data, min_freq, max_words):
    # Nettoyer les données : supprimer les NaN et convertir en str
    data_cleaned = data.dropna(subset=['Tweet'])  # Supprimer les lignes avec des tweets manquants
    data_cleaned['Tweet'] = data_cleaned['Tweet'].astype(str)  # Convertir en chaînes de caractères
    
    # Concaténer tous les tweets en une seule chaîne de texte
    text = " ".join(tweet for tweet in data_cleaned['Tweet'])
    
    if not text.strip():
        return None  # Return None if there are no words to plot
    
    # Générer le Word Cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        min_font_size=10,
        max_words=max_words,
        collocations=False
    ).generate(text)
    
    # Afficher le Word Cloud avec matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    return wordcloud

# Générer le graphique pour les hashtags
def plot_top_hashtags(top_hashtags, metric, color_palette):
    plt.figure(figsize=(10, 6))
    
    # Choisir la palette de couleurs
    if color_palette == "Spectral":
        colors = plt.cm.Spectral(np.linspace(0, 1, len(top_hashtags)))
    else:
        colors = plt.cm.get_cmap(color_palette, len(top_hashtags)).colors
    
    # Créer le graphique en barres
    plt.barh(top_hashtags['Hashtags'], top_hashtags[f'Total{metric}'], color=colors)
    plt.xlabel(f'Total de {metric}')
    plt.ylabel('Hashtags')
    plt.title(f'Top {n_top_hashtags} Hashtags par {metric}')
    plt.gca().invert_yaxis()  # Inverser l'axe Y pour avoir le hashtag le plus populaire en haut
    st.pyplot(plt)

# Ajouter des filtres dans la sidebar pour les hashtags
with st.sidebar:
    st.header("Filtres pour les Hashtags")
    metric = st.selectbox("Choisir la métrique", ["Likes", "Retweets"], key="metric_selectbox")
    n_top_hashtags = st.slider("Nombre de hashtags à afficher", min_value=1, max_value=20, value=10, key="n_top_hashtags_slider")
    color_palette = st.selectbox("Choisir la palette de couleurs", ["Spectral", "Set1", "Set2", "Set3", "Pastel1", "Pastel2"], key="color_palette_selectbox")

# Préparer les données pour les hashtags
@st.cache_data
def prepare_hashtag_data(phase_data):
    data_hashtags = phase_data[phase_data['Hashtags'] != ""].copy()
    data_hashtags['Hashtags'] = data_hashtags['Hashtags'].str.split(',')
    data_hashtags = data_hashtags.explode('Hashtags')
    data_hashtags['Hashtags'] = data_hashtags['Hashtags'].str.strip()
    
    # Grouper par hashtags et calculer les totaux
    hashtag_stats = data_hashtags.groupby('Hashtags').agg(
        TotalLikes=('Likes', 'sum'),
        TotalRTs=('RTs', 'sum'),
        TotalFollowers=('Followers', 'sum')
    ).reset_index()
    
    return hashtag_stats

# Charger les données des hashtags
hashtag_stats = prepare_hashtag_data(phase_data)

# Filtrer les données en fonction des choix de l'utilisateur
if metric == "Likes":
    top_hashtags = hashtag_stats.nlargest(n_top_hashtags, 'TotalLikes')
else:
    top_hashtags = hashtag_stats.nlargest(n_top_hashtags, 'TotalRTs')

# Ajouter un sélecteur de graphiques dans la sidebar
with st.sidebar:
    st.header("Sélection du Graphique")
    graph_type = st.selectbox(
        "Choisir le type de graphique",
        ["Top Influenceurs par Retweets", "Top Sources par Nombre de Tweets", "Top Utilisateurs par Followers"],
        key="graph_type_selectbox"
    )

# Fonction pour préparer les données des influenceurs par retweets
@st.cache_data
def prepare_top_retweets_users(phase_data):
    top_retweets_users = phase_data.groupby('UserMentionNames').agg(
        Total_retweets=('RTs', 'sum')
    ).reset_index().nlargest(10, 'Total_retweets')
    return top_retweets_users

# Fonction pour préparer les données des sources par nombre de tweets
@st.cache_data
def prepare_top_sources(phase_data):
    top_sources = phase_data.groupby('Source_Cleaned').agg(
        Total_tweets=('Source_Cleaned', 'size')
    ).reset_index().nlargest(10, 'Total_tweets')
    return top_sources

# Fonction pour préparer les données des utilisateurs par followers
@st.cache_data
def prepare_top_users_by_followers(phase_data):
    top_users_by_followers = phase_data.groupby('UserMentionNames').agg(
        Total_followers=('Followers', 'max')
    ).reset_index().nlargest(10, 'Total_followers')
    return top_users_by_followers

# Charger le fichier GeoJSON des pays
url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
try:
    response = requests.get(url)  # Télécharger le fichier GeoJSON
    response.raise_for_status()  # Vérifier les erreurs HTTP
    countries_geojson = response.json()  # Convertir la réponse en JSON
except requests.exceptions.RequestException as e:
    st.error(f"Erreur lors du chargement du fichier GeoJSON: {e}")
    st.stop()

# Générer le code HTML/JavaScript pour Leaflet
html_code = """
<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<div id="map" style="width: 100%; height: 500px;"></div>
<script>
    // Initialiser la carte avec une vue globale du monde
    var map = L.map('map').setView([0, 0], 2); // Centrer sur le monde avec un zoom adapté

    // Ajouter une couche de tuiles (OpenStreetMap)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Charger les données GeoJSON des pays
    var countriesData = """ + str(countries_geojson) + """;

    // Données de tweets par pays
    var tweetData = """ + str(tweet_data) + """; 

    // Données de sentiment moyen par pays
    var sentimentData = """ + str(sentiment_data) + """;

    // Fonction pour obtenir une couleur en fonction du sentiment moyen
    function getSentimentColor(sentimentMean) {
        if (sentimentMean < -0.5) {
            return '#ff0000'; // Rouge pour les sentiments très négatifs
        } else if (sentimentMean < 0) {
            return '#ff6666'; // Rouge clair pour les sentiments légèrement négatifs
        } else if (sentimentMean == 0) {
            return '#cccccc'; // Gris pour les sentiments neutres
        } else if (sentimentMean <= 0.5) {
            return '#66ff66'; // Vert clair pour les sentiments légèrement positifs
        } else {
            return '#00ff00'; // Vert pour les sentiments très positifs
        }
    }

    // Fonction pour définir le style des pays
    function style(feature) {
        var countryName = feature.properties.name;
        var sentimentMean = sentimentData[countryName] || 0; // Sentiment moyen (0 par défaut)

        return {
            fillColor: getSentimentColor(sentimentMean), // Couleur de remplissage basée sur le sentiment moyen
            weight: 1, // Épaisseur de la bordure
            opacity: 1, // Opacité de la bordure
            color: '#ffffff', // Couleur de la bordure
            fillOpacity: 0.7 // Opacité de remplissage
        };
    }

    // Fonction pour animer le survol
    function highlightFeature(e) {
        var layer = e.target;
        layer.setStyle({
            fillColor: '#00ff00', // Couleur de remplissage au survol
            weight: 2, // Épaisseur de la bordure au survol
            color: '#ffffff', // Couleur de la bordure au survol
            fillOpacity: 0.9 // Opacité de remplissage au survol
        });

        // Afficher la popup au survol
        var countryName = e.target.feature.properties.name;
        var tweetCount = tweetData[countryName] || 0;
        var sentimentMean = sentimentData[countryName] || 0;
        layer.bindPopup(`Pays: ${countryName}<br>Tweets: ${tweetCount}<br>Sentiment Moyen: ${sentimentMean.toFixed(2)}`).openPopup();
    }

    // Fonction pour réinitialiser le style après le survol
    function resetHighlight(e) {
        geojson.resetStyle(e.target);
        e.target.closePopup();
    }

    // Ajouter les événements de survol et de clic
    function onEachFeature(feature, layer) {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight
        });
    }

    // Ajouter la couche GeoJSON à la carte
    var geojson = L.geoJson(countriesData, {
        style: style,
        onEachFeature: onEachFeature
    }).addTo(map);
</script>
"""

# Afficher la carte dans Streamlit
st.components.v1.html(html_code, height=500)

# Afficher le Word Cloud
st.header("Nuage de Mots")
fig, ax = plt.subplots(figsize=(10, 5))
wordcloud = generate_wordcloud(phase_data, min_freq, max_words)
if wordcloud:
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
else:
    st.write("Aucun mot à afficher dans le nuage de mots.")

# Fonction pour afficher le graphique sélectionné
def plot_selected_graph(graph_type, phase_data):
    if graph_type == "Top Influenceurs par Retweets":
        data = prepare_top_retweets_users(phase_data)
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Total_retweets', y='UserMentionNames', data=data, palette='Set3')
        plt.title("Top 10 Influenceurs par Retweets")
        plt.xlabel("Total des Retweets")
        plt.ylabel("Utilisateur")
        plt.xticks(rotation=45)
        # Remove exponential notation
        plt.gca().get_xaxis().get_major_formatter().set_scientific(False)
    
    elif graph_type == "Top Sources par Nombre de Tweets":
        data = prepare_top_sources(phase_data)
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Total_tweets', y='Source_Cleaned', data=data, palette='Pastel1')
        plt.title("Top Sources par Nombre de Tweets")
        plt.xlabel("Nombre de Tweets")
        plt.ylabel("Source")
    
    elif graph_type == "Top Utilisateurs par Followers":
        data = prepare_top_users_by_followers(phase_data)
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Total_followers', y='UserMentionNames', data=data, palette='Set3')
        plt.title("Top Utilisateurs par Followers")
        plt.xlabel("Total des Followers")
        plt.ylabel("Utilisateur")
    
    st.pyplot(plt)

# Afficher le Word Cloud et le graphique des influenceurs côte à côte
st.header("Top Influenceurs et Hashtags")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Influenceurs")
    plot_selected_graph(graph_type, phase_data)  # Call the correct function

with col2:
    st.subheader("Top Hashtags")
    plot_top_hashtags(top_hashtags, metric, color_palette)

def load_data():
    # Define the chunk size
    chunk_size = 100000  # Adjust the chunk size as needed
    chunks = []
    total_rows = 0
    max_rows = 100000  # Limit the total number of rows to 100,000
    
    # Load the CSV file in chunks
    for chunk in pd.read_csv("data/FIFA.csv", chunksize=chunk_size):
        if total_rows + len(chunk) > max_rows:
            remaining_rows = max_rows - total_rows
            chunks.append(chunk.iloc[:remaining_rows])
            break
        chunks.append(chunk)
        total_rows += len(chunk)
    
    # Concatenate all chunks into a single DataFrame
    Fifa = pd.concat(chunks, ignore_index=True)
    return Fifa