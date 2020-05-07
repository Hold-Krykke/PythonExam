import random
import datetime

# x = datetime.datetime(2020, 5, 17) # Year, month, day


def make_test_data():
    tweets = ["testtweet", "asmongold", "asdakmd", "Trump", "Biden", ":)"]
    hashtags = ["#ass", "#2020", "#Biden", "#Trump"]
    people = ["@Nobbel", "@Asmongold", "@Biden", "@Trump", "@Hillary", "@Who"]
    urls = [
        "runivn.dk",
        "maltemagnussen.com",
        "trade-wind.dk",
        "dr.dk",
        "tv2.dk",
        "fuckstoremounts.com",
    ]
    authors = ["Malte", "Camilla", "some asshole", "Asger", "Runi"]
    dates = [
        datetime.date(2020, 5, 17),
        datetime.date(2020, 6, 17),
        datetime.date(2020, 5, 8),
    ]
    results = range(0, 1, 0.01)
    accuracy = range(100)

    example = {
        "tweet": random.choice(tweets),
        "hashtags": [random.choice(hashtags), random.choice(hashtags)],
        "people": [random.choice(people), random.choice(people)],
        "urls": [random.choice(urls), random.choice(urls)],
        "author": random.choice(authors),
        "date": random.choice(dates),
        "sentiment_analysis": {
            "verdict": "Positive",
            "result": random.choice(results),
            "positive_procent": 0.61,
            "negative_procent": 0.39,
            "accuracy": random.choice(accuracy),
        },
    }

    return example


"""
Example of data structure for the real data:
[
  {
    'tweet': 'This tweet year', 
    'hashtags': [
      '#MyFirstTweet'
      ], 
    'people': [
      '@folketinget'
      ], 
    'urls': [
      'runivn.dk'
      ], 
    'author': 'Runi Vedel', 
    'date': '01/05/2020', 
    'sentiment_analysis': [
      {
        'verdict': 'Positive', 
        'positive_procent': 0.61, 
        'negative_procent': 0.39
      }
    ]
  }, 
  {
    'tweet': ......
  }
]
"""
