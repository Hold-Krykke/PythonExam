# 4. semester python eksamens projekt
#### Lavet af:
* Cph-mh748 - Malte Hviid-Magnussen 
* Cph-rn118 - Rúni Vedel Niclasen 
* Cph-ab363 - Asger Bjarup 
* Cph-cs340 - Camilla Staunstrup 


### Følgende er det vi overordnet har indtil videre (skal nok udvides med teknologier og grundigere beskrivelser):
Vores grundlag for projektet er at vi gerne vil undersøge om hovedparten af følgende tweets med hashtags er overvejende positive eller negative:
* __#Trump, #Trump2020__
* __#Biden, #Biden2020__
* __#Election2020__  


### 
* __Web scraping af Twitter, baseret på hashtag.__
  * Forhindringer:
    * Hvordan håndterer Twitter web scrapers? Skal vi gøre brug af API? Rate limits?
  * Teknologier:
    * Web scraping med BeautifulSoup4, evt. Scrapy
  * Kan evt. udvides til at kunne tilbyde som service med en Flask server. 
    * Hertil kunne man gøre brug af Twitters avancerede søgefunktioner, som at sortere efter popularitet, seneste, med/uden billeder. Eller søgning med/uden diverse ord, engagement, timeframes mm.
* __Preprocessing af Twitter-dataen (clean-up, fjerne stop words)__
  * Teknologier:
    * Regex
    * Natural Language Toolkit (NLTK) 
* __Sentiment analysis / evt topic analysis hvis tid (swear words, hate speech eller lignende)__
  * Teknologier:
    * Natural Language Toolkit (NLTK)
    * evt sklearn
* __Presentation (grafphs/plots)__
  * Teknologier:
    * matplotlib


### Links til tutorials, libraries og lignende:
* [Scrapy](https://scrapy.org/)
* [Removing stop words with NLTK](https://www.geeksforgeeks.org/removing-stop-words-nltk-python/)
* [Sentiment Dictionary](https://provalisresearch.com/products/content-analysis-software/wordstat-dictionary/sentiment-dictionaries/)
* [Twitter api](https://developer.twitter.com/en/docs)
* [Sentiment Analysis with Scikit-Learn](https://stackabuse.com/python-for-nlp-sentiment-analysis-with-scikit-learn//)
* [Sentiment Analysis with NLTK](https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk)
* [Web Scraping & Sentiment Analysis Youtube Tutorial](https://www.youtube.com/watch?v=e6xZAISu-5E) and [Reporitory](https://github.com/jg-fisher/redditSentiment)
