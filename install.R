# install.R
install.packages(c("shiny", "tm", "ggplot2", "dplyr", "leaflet", "syuzhet", "wordcloud", "RColorBrewer", "plotly", "ggmap", "httr", "jsonlite", "purrr", "maps", "countrycode", "igraph", "ggraph", "topicmodels", "LDAvis", "widyr", "rnaturalearth", "shinythemes", "rworldmap", "rnaturalearthdata", "DT", "tidyr", "scales"))
# Mettre à jour les packages spécifiques
install.packages(c("cachem", "htmltools", "promises"))

  
packageVersion("cachem")
packageVersion("htmltools")
packageVersion("promises")

shiny::runApp('C:/Users/Youssef/Desktop/M2/TextMining/FifaApp')
