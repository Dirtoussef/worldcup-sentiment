import pandas as pd
from textblob import TextBlob

# Calculer le sentiment des tweets
def calculate_sentiment(text):
    analysis = TextBlob(str(text))
    return analysis.sentiment.polarity

# Classer les tweets par phase du tournoi
def classify_phases(Fifa_clean):
    huitieme_debut = pd.to_datetime("2018-06-29")
    huitieme_fin = pd.to_datetime("2018-07-04")
    demi_debut = pd.to_datetime("2018-07-10")
    demi_fin = pd.to_datetime("2018-07-11")
    finale = pd.to_datetime("2018-07-15")

    Fifa_clean['Phase'] = Fifa_clean['Date'].apply(
        lambda x: "Huitièmes de finale" if huitieme_debut <= pd.to_datetime(x) <= huitieme_fin else
        "Quarts de finale" if huitieme_fin < pd.to_datetime(x) < demi_debut else
        "Demi-finales" if demi_debut <= pd.to_datetime(x) <= demi_fin else
        "Finale" if pd.to_datetime(x) >= finale else "Tous"
    )
    return Fifa_clean

# Préparer les données des hashtags
def prepare_hashtag_data(Fifa_clean):
    data_hashtags = Fifa_clean[Fifa_clean['Hashtags'] != ""].copy()
    data_hashtags['Hashtags'] = data_hashtags['Hashtags'].str.split(',')
    data_hashtags = data_hashtags.explode('Hashtags')
    data_hashtags['Hashtags'] = data_hashtags['Hashtags'].str.strip()
    
    hashtag_stats = data_hashtags.groupby('Hashtags').agg(
        TotalLikes=('Likes', 'sum'),
        TotalRTs=('RTs', 'sum')
    ).reset_index()
    return hashtag_stats