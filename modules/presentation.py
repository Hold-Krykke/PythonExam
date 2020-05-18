# Presentation file
# Contains charts
# IMPORTS:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import nltk
import datetime
# https://www.accelebrate.com/blog/using-defaultdict-python
from collections import defaultdict


"""
How to use:

You have to have an array of tweets.
1. Sort
2. Get sentiment
3. Plot
4. Save plot or show

First, you sort the tweets, using for example get_by_key_value or get_tweets_in_daterange
Then you use get_sentiment 
Then you feed the result of get_sentiment to a plotter function

You can chain several filters.

"""

# Change here, if sentiments change
sentiments = ["Positive", "Negative", "Uncertain"]

# 1 SORTING
# FILTERING / SORTING FUNCTIONS START


def get_tweets_in_daterange(tweets, start_date, end_date):
    """
    Category: Filter function

    Returns all tweets with "date" between start_date and end_date

    Parameters:\n
        tweets: array of tweets
        start_date and end_date are datetime objects

    Returns:\n
        Filtered list of tweets within start_date and end_date
    """
    if not isinstance(start_date, datetime.date) or not isinstance(end_date, datetime.date):
        raise Exception("Wrong date format. Has to be datetime.date")

    if start_date > end_date:
        raise Exception("Start_date was before end_date.")
    return list(
        filter(
            lambda tweet: tweet["date"] <= end_date and tweet["date"] >= start_date,
            tweets,
        )
    )


def get_by_key_value(tweets, key, value):
    """
    Category: Filter function

    Get tweets from tweet array, by key and value. 

    For example:\n
        key = hashtags
        value = #Biden

    Parameters: \n
        tweets = Array of tweets you want to filter
        key = String: one of: [hashtags, people, urls]
        value = String

    Returns: \n
        Filtered List
    """
    if key not in ["hashtags", "mentions", "tweet_urls"]:
        raise Exception('key has to be "hashtags", "mentions", "tweet_urls"')

    print(tweets[0])
    return list(filter(lambda tweet: value in tweet[key], tweets))



def get_by_sentiment(tweets, sentiment):
    f"""
    Category: Filter function

    Parameters: \n
        Sentiment: {sentiments}

    Returns all tweets with a certain sentiment. 
    """
    if sentiment not in sentiments:
        raise Exception(f"Sentiment has to be in '{sentiments}'")
    # The is keyword is used to test if two variables refer to the same object.
    # Use the == operator to test if two variables are equal.
    return list(
        filter(
            lambda tweet: sentiment == tweet["sentiment_analysis"]["verdict"], tweets
        )
    )


def remove_sentiment(tweets, sentiment):
    f"""
    Category: Filter function

    Parameters: \n
        Sentiment: {sentiments}

    Returns all tweets without a certain sentiment. 
    """
    if sentiment not in sentiments:
        raise Exception(f"Sentiment has to be in '{sentiments}'")

    return list(
        filter(
            lambda tweet: sentiment != tweet["sentiment_analysis"]["verdict"], tweets
        )
    )


# FILTERING / SORTING FUNCTIONS DONE

# 2. GET SENTIMENT
def get_sentiment(tweets):
    """
    Filter tweets using other methods, before you use this one. 
    Makes a list of tweets into a Pandas DataFrame. 
    It has date on index and Sentiment on Columns and the value is the amount of tweets. 
    """
    # Make a dict, where key is date and value is a list of all sentiments for that date
    tweets_dict = defaultdict(list)
    for tweet in tweets:
        # The sentiment_analysis apparently has a list with the dict inside instead of just the dict..
        tweets_dict[tweet["date"]].append(
            tweet["sentiment_analysis"]["verdict"])

    # Takes .value_counts() https://www.geeksforgeeks.org/python-pandas-index-value_counts/
    for date in tweets_dict.keys():
        tweets_dict[date] = pd.Series(tweets_dict[date]).value_counts()

    # Makes a transposed dataframe sorted by index(date in this case)
    return pd.DataFrame(tweets_dict).T.fillna(value=0).sort_index()


# 3. PLOT
# PLOTTING START
def pie_chart(df, title, save=None):
    """
    Make a Pie Chart about Sentiments for given dataframe

    Parameters: \n
        df = DataFrame made by get_sentiment
        title = String
        save = If set, save with this file_name
    """
    sentiment = {}
    for column in sentiments:
        if column in df.columns:
            sentiment[column] = df[column].sum()

    plt.axes(pd.Series(sentiment).plot(
        kind="pie", autopct="%1.0f%%", title=title))
    plt.ylabel("")

    if save:
        save_plot(plt, save)
    else:
        plt.show()


def bar_plot(df, title, save=None):
    """
    Make a Bar Plot about Sentiments for given dataframe

    Parameters: \n
        df = DataFrame made by get_sentiment
        title = String
        save = If set, save with this file_name
    """
    ax = df.plot(kind="bar", rot=17, title=title)
    # There is a bit of repeat settings here, and in line_plot.
    # Maybe a "plt_settings" function could be an idea?
    ax.locator_params(integer=True)
    ax.set_ylabel("Tweets")
    plt.gca().set_ylim(bottom=0)

    if save:
        save_plot(plt, save)
    else:
        plt.show()


def line_plot(df, title, save=None):
    """
    Make a Line Chart about Sentiments for given dataframe

    Parameters: \n
        df = DataFrame made by get_sentiment
        title = String
        save = If set, save with this file_name
    """
    ax = df.plot(kind="line", rot=17, title=title)
    ax.locator_params(integer=True)
    ax.set_xticks(df.index)
    ax.set_ylabel("Tweets")
    plt.gca().set_ylim(bottom=0)

    if save:
        save_plot(plt, save)
    else:
        plt.show()


# PLOTTING END

# Save helper function
def save_plot(fig, name):
    """
    Save Plot to file

    Parameters:\n
        fig: Figure. pyplot fig. 
        name: string. Name of file. No extension. 

    Returns:\n
        Nothing. 
    """
    if isinstance(name, str):
        from pathlib import Path

        # https://stackoverflow.com/a/273227/11255140
        # if plots folder doesn't exist, create it.
        Path("./plots").mkdir(parents=True, exist_ok=True)
        # bbox_inches="tight" ensures less white space in the image.
        fig.savefig("./plots/" + name + ".png", bbox_inches="tight")
        print("Successfully saved Plot to ./plots/" + name + ".png")
    else:
        print("Name has to be a string.")
        raise Exception("name has to be a string.")
