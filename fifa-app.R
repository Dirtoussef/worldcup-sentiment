suppressPackageStartupMessages({
library(shiny)
library(tm)
library(ggplot2)
library(tm)
library(readxl)
library(wordcloud)
library(shiny)
library(RColorBrewer)
library(tm)
library(wordcloud)
library(RColorBrewer)
library(ggplot2)
library(syuzhet)#sentiment
library(dplyr)
library(ggplot2)
library(tidytext)
library(plotly)
library(ggmap)
library(httr)
library(jsonlite)
library(purrr)
library(maps)
library(countrycode)
library(igraph)
library(ggraph)
library(topicmodels)
library(LDAvis)
library(widyr)
library(leaflet)
library(rnaturalearth)
library(shinythemes)
library(rworldmap)
library(rnaturalearthdata)
library(DT)
library(tidyr)
library(scales)})






Fifa <- read.csv("data/FIFA.csv")

Fifa18 <- Fifa %>%
  mutate(Country = case_when(
    grepl("Nigeria|Abuja|Lagos|Kaduna|Ibadan|Kano|Port Harcourt|Enugu|Lekki|Gombe|Ikeja|Benin-City|Tema", Place) ~ "Nigeria",
    grepl("England|UK|London|Manchester|Sheffield|Newcastle Upon Tyne|Leeds|West Midlands|Nottingham|South East|Liverpool|Old Trafford|Leicester|Bristol|North East|Birmingham|Stamford Bridge|Brighton|Norwich|Oxford|Southampton|Hull|York|Bolton|Stoke-on-Trent", Place) ~ "United Kingdom",
    grepl("India|Hyderabad|New Delhi|Pune|Bangalore|Kerala|Delhi|Ahmadabad City|Jaipur|Chandigarh", Place) ~ "India",
    grepl("USA|America|New York|Los Angeles|Austin|Philadelphia|San Diego|California|Georgia|Chicago|San Antonio|Orlando|Virginia|Portland|Maryland|North Carolina|Denver|Charlotte|Phoenix|Columbus|Pittsburgh|Massachusetts|Miami|Tampa|Ohio|Minnesota|Fort Worth|Long Beach|Seattle|Bay Area|Detroit|Raleigh|Buffalo|Oakland|Kansas City|Cincinnati|San Francisco|New Orleans|Houston|Washington DC", Place) ~ "United States",
    grepl("France|Paris|Ile-de-France|Lyon|Marseille|Lille", Place) ~ "France",
    grepl("Indonesia|Jakarta|Yogyakarta|DKI Jakarta|Jakarta Capital Region|Bandung|Kota Surabaya|Bekasi|Batu|Tangerang|Jakarta Selatan", Place) ~ "Indonesia",
    grepl("Pakistan|Islamabad|Karachi|Lahore|Punjab|Rawalpindi", Place) ~ "Pakistan",
    grepl("Canada|Toronto|Ontario|Montréal|Vancouver|British Columbia|Ottawa|Edmonton", Place) ~ "Canada",
    grepl("Australia|Sydney|Melbourne|New South Wales|Victoria|Brisbane", Place) ~ "Australia",
    grepl("Ghana|Accra|Greater Accra|Kumasi|Port Harcourt|Kingston|Enugu|Lekki|Gombe|Ikeja|Nakuru", Place) ~ "Ghana",
    grepl("Brazil|Rio de Janeiro|São Paulo|Porto Alegre|Curitiba|Salvador|Recife|Manaus|Fortaleza|Brasília|Belém|Belo Horizonte|Campinas|Goiânia|Campo Grande|Sorocaba", Place) ~ "Brazil",
    grepl("Philippines|Republic of the Philippines|Manila", Place) ~ "Philippines",
    grepl("South Korea|Seoul|Republic of Korea", Place) ~ "South Korea",
    grepl("Bangladesh|Dhaka|Chattogram", Place) ~ "Bangladesh",
    grepl("Argentina|Buenos Aires", Place) ~ "Argentina",
    grepl("Uruguay|uruguay|URUGUAY", Place) ~ "Uruguay",
    grepl("Mexico|Mexico City|Ciudad de México|Puebla", Place) ~ "Mexico",
    grepl("Egypt|Alexandria", Place) ~ "Egypt",
    grepl("South Africa|Cape Town|Bloemfontein|Port Elizabeth|East London|Pretoria|Johannesburg|Durban|Soweto|Polokwane|Rustenburg|Pietermaritzburg", Place) ~ "South Africa",
    grepl("Ireland|Dublin|Cork", Place) ~ "Ireland",
    grepl("Germany|Deutschland|Berlin", Place) ~ "Germany",
    grepl("Croatia|Zagreb", Place) ~ "Croatia",
    grepl("Sweden|sweden|suede|sueden", Place) ~ "Sweden",
    grepl("Scotland|Edinburgh|Glasgow", Place) ~ "Scotland",
    grepl("Colombia|colombia|Colombia|Colombie", Place) ~ "Colombia",
    grepl("Russia|Moscow", Place) ~ "Russia",
    grepl("Japan|Tokyo", Place) ~ "Japan",
    grepl("Peru|Lima", Place) ~ "Peru",
    grepl("Chile|Santiago", Place) ~ "Chile",
    grepl("Wales|Cardiff", Place) ~ "Wales",
    grepl("Spain|Barcelona|Madrid", Place) ~ "Spain",
    grepl("Belgium|Brussels", Place) ~ "Belgium",
    grepl("Malaysia|Johore|Perak|Kelantan|Kuching|Kedah|Johor Bahru|Bat", Place) ~ "Malaysia",
    grepl("Ecuador|Guayaquil", Place) ~ "Ecuador",
    grepl("Panamá", Place) ~ "Panama",
    grepl("Sweden", Place) ~ "Sweden",
    grepl("Poland", Place) ~ "Poland",
    grepl("Kuwait", Place) ~ "Kuwait",
    grepl("Italy|Milan", Place) ~ "Italy",
    grepl("Jamaica|Kingston", Place) ~ "Jamaica",
    grepl("Brazil|brazil|Bresil|bresil", Place) ~ "Brazil", 
    grepl("Costa Rica|costa Rica|costa rica", Place) ~ "Costa Rica",
    grepl("Kenya|Mombasa|Nakuru", Place) ~ "Kenya",
    grepl("Serbia|serbia", Place) ~ "Serbia",
    grepl("Senegal|senegal", Place) ~ "Senegal",
    grepl("Egypte|egypte", Place) ~ "Egypt", 
    grepl("Maroc|Moroco", Place) ~ "Morocco", 
    grepl("Portugal|portugal", Place) ~ "Portugal",
    grepl("Island|island|islands|Islands|ISLANDS", Place) ~ "Iceland", 
    grepl("Tunisia|tunisia|Tunis|tunis|Tunisie|tunisie", Place) ~ "Tunisia",
    grepl("Kingdom of Saudi Arabia|Saudi Arabia|saudi arabia|Kingdom of Saudi Arabia|Kingdom of Saudi Arabi|Saudi Arabia", Place) ~ "Saudi Arabia",
    grepl("Switzerland|suisse|Suisse|switzerland", Place) ~ "Switzerland",
    grepl("Iran|iran", Place) ~ "Iran",
    grepl("Peru|peru|PERU", Place) ~ "Peru",
    TRUE ~ "Others"
  ))

Fifa_clean<-Fifa18%>%filter(Country!="Others")

Fifa_clean <- Fifa_clean %>%
  mutate(Source_Cleaned = ifelse(grepl("Twitter for Android|Twitter Web Client|Twitter for iPhone|Twitter Lite|Twitter for iPad", Source), 
                                 Source, "Other"))
huitieme_debut <- as.Date("2018-06-29")  
huitieme_fin <- as.Date("2018-07-04")
demi_debut <- as.Date("2018-07-10")
demi_fin <- as.Date("2018-07-11")
finale <- as.Date("2018-07-15")


# Classification des tweets selon la phase du tournoi
Fifa_clean <- Fifa_clean %>%
  mutate(
    Phase = case_when(
      Date >= huitieme_debut & Date <= huitieme_fin ~ "Huitièmes de finale",
      Date > huitieme_fin & Date < demi_debut ~ "Quarts de finale",
      Date >= demi_debut & Date <= demi_fin ~ "Demi-finales",
      Date == finale ~ "Finale"))



Fifa_clean$Sentiment <- get_sentiment(Fifa_clean$Tweet, method = "syuzhet")
Fifa_clean <- Fifa_clean %>%
  mutate(Sentiment_Category = case_when(
    Sentiment > 0.05 ~ "Positif",
    Sentiment < -0.05 ~ "Négatif",
    TRUE ~ "Neutre"
  ))

Fifa_clean$sentimentCategory <- Fifa_clean %>%
  mutate(Sentiment = get_sentiment(Tweet, method = "syuzhet"),
         Sentiment_Category = case_when(
           Sentiment > 0.05 ~ "Positif",
           Sentiment < -0.05 ~ "Négatif",
           TRUE ~ "Neutre"
         ))





# Shiny UI
register_google(key = "VOTRE_CLÉ_API")



# UI
ui <- navbarPage(
  title = "Analyse des Tweets par Pays",
  theme = shinytheme("darkly"),
  
  tags$head(
    tags$style(HTML("
      h1, h2, h3, h4, h5, h6, p, body {
        font-family: 'Roboto', sans-serif;
      }
      /* Custom CSS pour changer la couleur de texte en blanc pour toutes les cellules de DataTable */
      .dataTables_wrapper .dataTable td {
        color: white !important;
      }
      .database-heading {
        color: gray;
        text-align: center;
      }
      .dates-list {
        margin: 0;
        padding: 0;
        list-style-type: none;
        text-align: center;
      }
      .dates-list li {
        display: inline;
        margin-right: 10px;
      }
      /* Ici, vous pouvez ajouter d'autres styles personnalisés si nécessaire */
    "))
  ),
  tabPanel("Introduction",
           fluidPage(
             # Application Title
             h1("Analyse Textuelle des Tweets de la Coupe du Monde FIFA 2018", 
                style = "text-align: center; margin-bottom: 20px;"),
             
             # Contextual Image
             img(src = "parcours.webp", height = "450px", style = "display: block; margin: auto;"),
             
             # Introduction Section
             h3("Contexte", class = "database-heading"),
             p("La Coupe du Monde FIFA est l'un des événements sportifs les plus suivis au monde, suscitant des réactions passionnées sur les réseaux sociaux. Cette application vise à explorer ces réactions en analysant les tweets liés à la Coupe du Monde 2018."),
             
             # Data Source Section
             h3("Base de Données", class = "database-heading"),
             p("Les données utilisées dans cette application proviennent d'une collection de tweets qui ont été  récupérés pendant la Coupe du Monde FIFA 2018 par le site Kaggle."),
             p(HTML("Le Scraping des Tweets a été fait aux dates suivantes : 
           <ul class='dates-list'>
             <li>2018-06-29</li>
             <li>2018-07-04</li>
             <li>2018-07-10</li>
             <li>2018-07-11</li>
             <li>2018-07-15</li>
           </ul>")),
             
             # Data Example Section
             
             
             # Application Features Section
             h3("Applications", class = "database-heading"),
             HTML("<ul>
                     <li>Carte géographique : Visualisation des tweets par pays.</li>
                     <li>Analyse de sentiment : Utilisation de 'syuzhet' pour évaluer les sentiments des tweets.</li>
                     <li>Table DT : Une table interactive pour explorer les tweets.</li>
                     <li>Nuage de mots (WordCloud) : Identification des termes les plus fréquents.</li>
                     <li>Statistiques : Analyses diverses et représentations graphiques des données.</li>
                   </ul>")
           )
  ),
  tabPanel("Carte des Tweets",
           sidebarLayout(
             sidebarPanel(
               selectInput("sourceInputOverview", "Choisissez la source:", 
                           choices = c("Tous", unique(Fifa_clean$Source_Cleaned)), selected = "Tous"),
               selectInput("PhaseInputOverview", "Choisissez la phase:",
                           choices = c("Toutes", unique(Fifa_clean$Phase)), selected = "Toutes")
             ),
             mainPanel(
               leafletOutput("tweetMapOverview")
             )
           )
  ),
  tabPanel("Carte  de  Sentiment",
           sidebarLayout(
             sidebarPanel(
               selectInput("sourceInputSentiment", "Choisissez la source:", 
                           choices = c("Tous", unique(Fifa_clean$Source_Cleaned)), selected = "Tous"),
               selectInput("PhaseInputSentiment", "Choisissez la phase:",
                           choices = c("Toutes", unique(Fifa_clean$Phase)), selected = "Toutes")
             ),
             mainPanel(
               leafletOutput("sentimentMap")
             )
           )
  ),tabPanel("Répartition des Sentiments",
             sidebarLayout(
               sidebarPanel(
                 selectInput("countryInput", "Choisissez les pays:",
                             choices = c("Tous" = "Tous", unique(Fifa_clean$Country)),
                             selected = "Tous", multiple = TRUE)
               ),
               mainPanel(
                 tabsetPanel(
                   id = "sentimentTabs",
                   tabPanel("Trending Topics",
                            fluidRow(
                              column(4,
                                     sliderInput("maxNumberTweets", "Maximum number of Tweets", min = 0, max = 20000, value = 1000),
                                     sliderInput("minLikes", "Minimum Likes", min = 0, max = 100, value = 0),
                                     sliderInput("minRetweets", "Minimum Retweets", min = 0, max = 100, value = 0)
                              ),
                              column(8,
                                     DTOutput("trendingTopicsTable")
                              )
                            )
                   ),
                   # Add additional sub-tabs here as needed
                   tabPanel("Sentiment Overview", plotOutput("sentimentDistribution"))
                   # Add additional content to each tab as required
                 )
               )
             )), tabPanel("Nuage de Mots",
                          sidebarLayout(
                            sidebarPanel(
                              sliderInput("freq", 
                                          "Fréquence minimale des mots:",
                                          min = 1, 
                                          max = 100, 
                                          value = 2),
                              sliderInput("wordmax", 
                                          "Nombre maximal de mots:",
                                          min = 1, 
                                          max = 300, 
                                          value = 100),
                              selectInput("PhaseInputWordCloud", "Choisissez la Phase:", 
                                          choices = c("Tous", unique(Fifa_clean$Phase)), selected = "Tous"),
                            ),
                            mainPanel(
                              plotOutput("wordCloud")
                            )
                          )
             ),  tabPanel("Statistique",
                          sidebarLayout(
                            sidebarPanel(
                              selectInput("graphType", "Choisissez le graphique à afficher:",
                                          choices = c("Top 10 Influenceurs FIFA par Retweets" = "topRetweetsUsers",
                                                      "Top Source par Nombre de Tweets" = "topSourceCleaned",
                                                      "Top utilisateurs par Followers" = "topUsersByFollowers"))
                            ),
                            mainPanel(
                              plotOutput("selectedGraph")
                            )
                          )
             ),
  tabPanel("Analyse des Top Hashtags",
           sidebarLayout(
             sidebarPanel(
               numericInput("nTopHashtags", "Nombre de top hashtags à afficher:", min = 5, max = 50, value = 10, step = 5),
               radioButtons("metric", "Filtrer par:", choices = c("Likes" = "Likes", "Retweets" = "RTs")),
               selectInput("colorPalette", "Choisissez une palette de couleurs:",
                           choices = c("Bleu" = "Blues", "Rouge" = "Reds", "Vert" = "Greens", "Dynamique" = "Spectral"))
             ),
             mainPanel(
               plotOutput("plotTopHashtags")
             )
           )
  )
)


# Server


server <- function(input, output, session) {
  
  # données géographiques
  countries <- ne_countries(scale = "medium", returnclass = "sf")
  
  # Vue d'ensemble
  output$tweetMapOverview <- renderLeaflet({
    # Filtre des données basées sur l'entrée de l'utilisateur
    data_filtered <- Fifa_clean %>%
      filter((Source_Cleaned == input$sourceInputOverview | input$sourceInputOverview == "Tous") &
               (Phase == input$PhaseInputOverview | input$PhaseInputOverview == "Toutes")) %>%
      count(Country, name = "NumTweets")
    
    
    map_data <- left_join(countries, data_filtered, by = c("name" = "Country"))
    
    # la carte
    leaflet(map_data) %>%
      addProviderTiles(providers$CartoDB.Positron) %>%
      addPolygons(fillColor = ~colorNumeric(palette = "YlOrRd", domain = NumTweets)(NumTweets),
                  weight = 0.5,
                  opacity = 1,
                  color = "white",
                  dashArray = "3",
                  fillOpacity = 0.7,
                  highlight = highlightOptions(weight = 5, color = "#666", fillOpacity = 0.7, bringToFront = TRUE),
                  smoothFactor = 0.2,
                  popup = ~paste(name, ": ", NumTweets, "tweets")) %>%
      setView(lat = 0, lng = 0, zoom = 2)
  })
  
  #  Analyse de Sentiment
  output$sentimentMap <- renderLeaflet({
    
    data_filtered <- Fifa_clean %>%
      filter((Source_Cleaned == input$sourceInputSentiment | input$sourceInputSentiment == "Tous") &
               (Phase == input$PhaseInputSentiment | input$PhaseInputSentiment == "Toutes")) %>%
      group_by(Country) %>%
      summarise(Sentiment = mean(Sentiment, na.rm = TRUE))
    
    
    map_data <- left_join(countries, data_filtered, by = c("name" = "Country"))
    
    #  la carte
    sentiment_palette <- colorNumeric(palette = "RdYlBu", domain = map_data$Sentiment)
    
    leaflet(map_data) %>%
      addProviderTiles(providers$CartoDB.Positron) %>%
      addPolygons(
        fillColor = ~sentiment_palette(Sentiment),
        weight = 0.5,
        color = "white",
        dashArray = "3",
        fillOpacity = 0.7,
        highlightOptions = highlightOptions(weight = 5, color = "#666", fillOpacity = 0.7, bringToFront = TRUE),
        smoothFactor = 0.2,
        popup = ~paste(name, ": ", Sentiment, " sentiment")
      ) %>%
      addLegend(
        position = "bottomright",
        pal = sentiment_palette,
        values = ~Sentiment,
        title = "Sentiment",
        opacity = 1
      ) %>%
      setView(lat = 0, lng = 0, zoom = 2)
  })
  
  output$wordCloud <- renderPlot({
    if (!requireNamespace("tm", quietly = TRUE) || !requireNamespace("wordcloud", quietly = TRUE)) {
      stop("Nécessite les packages 'tm' et 'wordcloud'. Veuillez les installer.")
    }
    
    # Filtrer les données basées sur la phase sélectionnée
    filtered_data <- switch(input$PhaseInputWordCloud,
                            "Tous" = Fifa_clean,
                            "Huitièmes de finale" = filter(Fifa_clean, Phase == "Huitièmes de finale"),
                            "Quarts de finale" = filter(Fifa_clean, Phase == "Quarts de finale"),
                            "Demi-finales" = filter(Fifa_clean, Phase == "Demi-finales"),
                            "Finale" = filter(Fifa_clean, Phase == "Finale"))
    # Préparer les données pour le wordcloud
    tweets_text <- tolower(filtered_data$Tweet)
    corpus <- Corpus(VectorSource(tweets_text))
    corpus <- tm_map(corpus, content_transformer(tolower))
    corpus <- tm_map(corpus, removePunctuation)
    corpus <- tm_map(corpus, removeNumbers)
    corpus <- tm_map(corpus, removeWords, stopwords("en"))
    corpus <- tm_map(corpus, stripWhitespace)
    
    dtm <- TermDocumentMatrix(corpus)
    m <- as.matrix(dtm)
    word_freqs <- sort(rowSums(m), decreasing = TRUE)
    dm <- data.frame(word = names(word_freqs), freq = word_freqs)
    
    # Filtreselon input$freq
    dm_filtered <- subset(dm, freq >= input$freq)
    
    #  input$wordmax  limiter le nombre de mots
    wordcloud(words = dm_filtered$word, freq = dm_filtered$freq, min.freq = input$freq,
              max.words = input$wordmax, random.order = FALSE, colors = brewer.pal(8, "Dark2"))
  })
  
  output$selectedGraph <- renderPlot({
    switch(input$graphType,
           "topRetweetsUsers" = {
             top_retweets_users <- Fifa_clean %>%
               group_by(UserMentionNames) %>%
               summarise(Total_retweets = sum(RTs, na.rm = TRUE)) %>%
               arrange(desc(Total_retweets)) %>%
               slice(1:10)
             
             ggplot(top_retweets_users, aes(x = reorder(UserMentionNames, -Total_retweets), y = Total_retweets, fill = UserMentionNames)) +
               geom_bar(stat = "identity") +
               scale_fill_brewer(palette = "Set3") +
               theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
               theme(legend.position = "none")+
               labs(x = "Utilisateur", y = "Total des Retweets", title = "Top 10 Influenceurs FIFA par Retweets")
           },
           "topSourceCleaned" = {
             top_sources <- Fifa_clean %>%
               group_by(Source_Cleaned) %>%
               summarise(Total_tweets = n()) %>%
               arrange(desc(Total_tweets)) %>%
               slice(1:10)
             
             ggplot(top_sources, aes(x = reorder(Source_Cleaned, -Total_tweets), y = Total_tweets, fill = Source_Cleaned)) +
               geom_bar(stat = "identity") +
               coord_flip() +
               scale_fill_brewer(palette = "Pastel1") +
               theme_minimal() +
               theme(legend.position = "none")+
               labs(x = "Source", y = "Nombre de Tweets", title = "Top Source_Cleaned par Nombre de Tweets")
           },
           "topUsersByFollowers" = {
             top_users_by_followers <- Fifa_clean %>%
               group_by(UserMentionNames) %>%
               summarise(Total_followers = max(Followers, na.rm = TRUE)) %>%
               arrange(desc(Total_followers)) %>%
               slice(1:10)
             
             ggplot(top_users_by_followers, aes(x = reorder(UserMentionNames, -Total_followers), y = Total_followers, fill = UserMentionNames)) +
               geom_bar(stat = "identity") +
               coord_flip() +
               scale_fill_brewer(palette = "Set3") +
               theme_minimal() +
               
               theme(legend.position = "none")+
               labs(x = "Utilisateur", y = "Total des Followers", title = "Top Utilisateurs par Followers")
           }
    )
  })
  
  output$sentimentDistribution <- renderPlot({
    
    data_filtered <- if("Tous" %in% input$countryInput) {
      Fifa_clean
    } else {
      Fifa_clean %>% filter(Country %in% input$countryInput)
    }
    
    # la distribution des sentiments
    sentiment_distribution <- data_filtered %>%
      group_by(Country, Phase, Sentiment_Category) %>%
      summarise(Count = n(), .groups = 'drop') %>%
      mutate(Total = sum(Count), Percent = Count / Total) %>%
      filter(Phase %in% c("Huitièmes de finale", "Quarts de finale", "Demi-finales", "Finale")) %>%
      arrange(Phase)
    
    
    ggplot(sentiment_distribution, aes(x = Phase, y = Percent, color = Sentiment_Category)) +
      geom_line(aes(group = Sentiment_Category), size = 1) +
      geom_point(aes(shape = Sentiment_Category), size = 3) +
      facet_wrap(~Country) +
      scale_color_manual(values = c("Positif" = "green", "Négatif" = "red", "Neutre" = "blue")) +
      labs(title = "Répartition des Sentiments par Phase et Pays",
           x = "Phase du Tournoi", y = "Pourcentage de Tweets") +
      theme_minimal() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
  })
  trending_topics_data <- reactive({
    
    req(input$maxNumberTweets, input$minLikes, input$minRetweets)
    
    
    data <- Fifa_clean %>%
      filter(Likes >= input$minLikes, RTs >= input$minRetweets)
    
    # les résultats au nombre spécifié par input$maxNumberTweets
    head(data, as.numeric(input$maxNumberTweets))
  })
  
  #  DataTable
  output$trendingTopicsTable <- renderDT({
    datatable(trending_topics_data(), options = list(pageLength = 5, searchHighlight = TRUE))
  })
  
  output$hashtagPlot <- renderPlot({
    require(tidyr)
    require(dplyr)
    require(ggplot2)
    
    #  'Hashtags' 
    hashtags_data <- Fifa_clean %>%
      select(Hashtags) %>%
      filter(Hashtags != "") %>% 
      separate_rows(Hashtags, sep = ",") %>% 
      group_by(Hashtags) %>%
      summarise(Count = n()) %>%
      arrange(desc(Count)) %>%
      head(10) 
    
    
    ggplot(hashtags_data, aes(x = reorder(Hashtags, Count), y = Count)) +
      geom_bar(stat = "identity", fill = "steelblue") +
      theme_minimal() +
      labs(title = "Top 10 des Hashtags", x = "Hashtag", y = "Nombre d'occurrences") +
      coord_flip() 
  })
  
  output$plotTopHashtags <- renderPlot({
    
    data_hashtags <- Fifa_clean %>%
      select(Hashtags, Likes, RTs, Followers) %>%
      filter(Hashtags != "") %>%
      separate_rows(Hashtags, sep = ",") %>%
      group_by(Hashtags) %>%
      summarise(TotalLikes = sum(Likes), TotalRTs = sum(RTs), TotalFollowers = sum(Followers)) %>%
      ungroup()
    
    
    data_filtered <- if (input$metric == "Likes") {
      data_hashtags %>%
        arrange(desc(TotalLikes)) %>%
        head(input$nTopHashtags)
    } else {
      data_hashtags %>%
        arrange(desc(TotalRTs)) %>%
        head(input$nTopHashtags)
    }
    
    
    p <- ggplot(data_filtered, aes(x = reorder(Hashtags, if (input$metric == "Likes") TotalLikes else TotalRTs), y = if (input$metric == "Likes") TotalLikes else TotalRTs, fill = Hashtags)) +
      geom_bar(stat = "identity") +
      coord_flip() +
      labs(x = "Hashtags", y = if (input$metric == "Likes") "Total de Likes" else "Total de Retweets", title = paste("Top", input$nTopHashtags, "Hashtags par", if (input$metric == "Likes") "Likes" else "Retweets")) +
      theme_minimal()+
      theme(legend.position = "none")
    
    # Appliquer une palette de couleurs spécifique
    num_colors <- length(unique(data_filtered$Hashtags))
    if (input$colorPalette == "Spectral") {
      colors <- colorRampPalette(brewer.pal(11, "Spectral"))(num_colors)
      p <- p + scale_fill_manual(values = colors)
    } else {
      p <- p + scale_fill_brewer(palette = input$colorPalette)
    }
    
    print(p)
    
  })
}
  


