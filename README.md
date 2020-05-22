# 4. Semester Python Eksamens Projekt
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
* __Sentiment analysis__
  * Teknologier:
    * Natural Language Toolkit (NLTK)
    * evt sklearn
* __Presentation (grafphs/plots)__
  * Teknologier:
    * matplotlib
## Using the program 
1. Clone the repo and follow the instructions in `setup.ipynb`

## Using the program through Flask
1. Insert here

## Using the program through CLI
1. In the root folder, run `python app.py -h` to print the **help** output:  

<img src="https://i.imgur.com/wCrfTY0.png" height=850 width=750/>  

A lot of the arguments have default values.  
The program can run using all default values by simply passing the hashtags you want to gather info from.  

For example, to search for the hashtags `#trump` and `#biden`:  
`python app.py trump biden`  
This would run the program using the following values:
```py
{'certainty_high': 0.75,
 'certainty_low': 0.25,
 'date': [datetime.date(2020, 5, 22),
          datetime.date(2020, 5, 27)],
 'fresh_search': False,
 'hashtags': ['trump',
              'biden'],
 'plot_type': 'pie',
 'remove_sentiment': None,
 'save_plot': False,
 'search_hashtags': None,
 'search_mentions': None,
 'search_urls': None,
 'tweet_count': 300}
 ```
 *Date by default is set to current day + 5 days*


### Links til tutorials, libraries og lignende:
* [Scrapy](https://scrapy.org/)
* [Removing stop words with NLTK](https://www.geeksforgeeks.org/removing-stop-words-nltk-python/)
* [Sentiment Dictionary](https://provalisresearch.com/products/content-analysis-software/wordstat-dictionary/sentiment-dictionaries/)
* [Twitter api](https://developer.twitter.com/en/docs)
* [Sentiment Analysis with Scikit-Learn](https://stackabuse.com/python-for-nlp-sentiment-analysis-with-scikit-learn//)
* [Sentiment Analysis with NLTK](https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk)
* [Web Scraping & Sentiment Analysis Youtube Tutorial](https://www.youtube.com/watch?v=e6xZAISu-5E) and [Reporitory](https://github.com/jg-fisher/redditSentiment)
* [Video om Natural Language Processing fra Slack](https://www.youtube.com/watch?v=xvqsFTUsOmc)
* [Plotting](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.show.html)
