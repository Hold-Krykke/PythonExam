# Presentation file
# Contains charts
# IMPORTS:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import nltk
import datetime


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

# FILTERING / SORTING FUNCTIONS START
def get_tweets_in_daterange(tweets, start_date, end_date):
    """
    Category: Sorter function

    Returns all tweets with "date" between start_date and end_date

    Parameters:

        tweets: array of tweets
        start_date and end_date are datetime objects

    Returns:

        Filtered list of tweets within start_date and end_date
    """
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
    Category: Sorter function

    Get tweets from tweet array, by key and value. 

    For example:
        
        key = hashtags
        value = #Biden

    Parameters:
        
        tweets = Array of tweets you want to filter
        key = String: one of: [hashtags, people, urls]
        value = String

    Returns: 

        Filtered List
    """

    # def custom_filter(tweet):
    #     # For use by .filter()
    #     if value in tweet[key]:
    #         return True
    #     else:
    #         return False

    # return list(filter(custom_filter, tweets))
    return list(filter(lambda tweet: value in tweet[key], tweets))


def get_by_sentiment(tweets, sentiment):
    """
    Returns all tweets with a certain sentiment. 
    Positive, Negative or Uncertain 
    """
    # The is keyword is used to test if two variables refer to the same object.
    # Use the == operator to test if two variables are equal.
    return list(
        filter(
            lambda tweet: sentiment == tweet["sentiment_analysis"]["verdict"], tweets
        )
    )


def remove_sentiment(tweets, sentiment):
    """
    Remove all tweets with certain sentiment
    """
    return list(
        filter(
            lambda tweet: sentiment != tweet["sentiment_analysis"]["verdict"], tweets
        )
    )


# FILTERING / SORTING FUNCTIONS DONE


def get_sentiment(tweets):
    """
    Filter tweets using other methods, before you use this one. 
    Makes a list of tweets into a Pandas DataFrame. 
    It has date on index and Sentiment on Columns and the value is the amount of tweets. 
    """
    # Make a dict, where key is date and value is a list of all sentiments for that date
    tweets_dict = defaultdict(list)
    for tweet in tweets:
        tweets_dict[tweet["date"]].append(tweet["sentiment_analysis"]["verdict"])

    # Takes .value_counts() https://www.geeksforgeeks.org/python-pandas-index-value_counts/
    for date in tweets_dict.keys():
        tweets_dict[date] = pd.Series(tweets_dict[date]).value_counts()

    # Makes a transposed dataframe sorted by index(date in this case)
    return pd.DataFrame(tweets_dict).T.sort_index()


# PLOTTING START
def pie_chart(df, title, save=None):
    """
    Make a Pie Chart about Sentiments for given dataframe

    Parameters: 

        df = DataFrame made by get_sentiment
        title = String
        save = If set, save with this file_name
    """
    sentiment = {}
    for column in ["Positive", "Negative", "Uncertain"]:
        if column in df.columns:
            sentiment[column] = df[column].sum()

    plt.axes(pd.Series(sentiment).plot(kind="pie", autopct="%1.0f%%", title=title))
    plt.ylabel("")

    if save:
        save_plot(plt, save)
    else:
        plt.show()


def bar_plot(df, title, save=None):
    df.plot(kind="bar", rot=0, title=title)

    if save:
        save_plot(plt, save)
    else:
        plt.show()


def line_plot(df, title, save=None):
    df.plot(kind="line", title=title)

    if save:
        save_plot(plt, save)
    else:
        plt.show()


# PLOTTING END

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
        # bbox_inces="tight" ensures less white space in the image.
        fig.savefig("./plots/" + name + ".png", bbox_inces="tight")
        print("Successfully saved Plot to ./plots/" + name + ".png")
    else:
        print("Name has to be a string.")

