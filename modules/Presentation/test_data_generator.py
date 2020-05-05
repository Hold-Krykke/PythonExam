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
        datetime.datetime(2020, 5, 17),
        datetime.datetime(2020, 6, 17),
        datetime.datetime(2020, 5, 8),
    ]
    results = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    accuracy = range(100)

    example = {
        "tweet": random.choice(tweets),
        "hashtags": [random.choice(hashtags), random.choice(hashtags)],
        "people": [random.choice(people), random.choice(people)],
        "urls": [random.choice(urls), random.choice(urls)],
        "author": random.choice(authors),
        "date": "01/05/2020",
        "sentiment": {
            "result": random.choice(results),
            "accuracy": random.choice(accuracy),
        },
    }

    return example
