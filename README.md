# 4. semester python eksamens projekt
#### Lavet af:
* Cph-mh748 - Malte Hviid-Magnussen 
* Cph-rn118 - Rúni Vedel Niclasen 
* Cph-ab363 - Asger Bjarup 
* Cph-cs340 - Camilla Staunstrup 


### Følgende er det vi overordnet har indtil videre (skal nok udvides med teknologier og grundigere beskrivelser):
##### Vores grundlag for projektet er at vi gerne vil undersøge om hovedparten af følgende tweets med hashtags er overvejende positive eller negative:
* #Trump, #Trump2020
* #Biden, #Biden2020
* #Election2020  


### 
* Web scraping af Twitter, baseret på hashtag.
  * Forhindringer:
    * Hvordan håndterer Twitter web scrapers? Skal vi gøre brug af API? Rate limits?
  * Teknologier:
    * Web scraping med BeautifulSoup4, evt. Scrapy
  * Kan evt. udvides til at kunne tilbyde som service med en Flask server. 
    * Hertil kunne man gøre brug af Twitters avancerede søgefunktioner, som at sortere efter popularitet, seneste, med/uden billeder. Eller søgning med/uden diverse ord, engagement, timeframes mm.
* Preprocessing af Twitter-dataen (clean-up, fjerne stop words)
  * Teknologier:
    * Regex
    * Natural Language Toolkit (NLTK) 
* Sentiment analysis / evt topic analysis hvis tid (swear words, hate speech eller lignende)
  * Teknologier:
    * Natural Language Toolkit (NLTK)
    * evt sklearn
* Præsentation af analysen (grafer/plots ??)
  * Teknologier:
    * matplotlib


