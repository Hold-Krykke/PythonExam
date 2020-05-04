# Presentation file
# Contains charts
# Start-point is this tutorial: https://stackabuse.com/python-for-nlp-sentiment-analysis-with-scikit-learn//
# IMPORTS:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import nltk

# Test Data Path
test_data_path = "../../data/test_tweets/presentation_test_tweets.csv"

'''
Example of data structure for the real data:
[
  1: {
       words: [

       ],
       sentiment: ...,
       date: ...,
       originalPoster:...,
       sentiment: true or false,
       other...
     },
  2: {
     },
  ...
]
'''


def get_data_from_csv(test_data_path):
    """
    Importing CSV data as pandas DataFrame.

    Parameters:
    test_data_path (string): Path to the CSV data you want to import.

    Returns:
    Pandas DataFrame
    """

    test_tweets = pd.read_csv(test_data_path)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    return test_tweets


def save_plot(fig, name):
    if (isinstance(name, str)):
        from pathlib import Path
        # https://stackoverflow.com/a/273227/11255140
        # if plots folder doesn't exist, create it.
        Path("./plots").mkdir(parents=True, exist_ok=True)
        # bbox_inces="tight" ensures less white space in the image.
        fig.savefig("./plots/"+name+".png", bbox_inces='tight')
        print("Successfully saved Plot to ./plots/"+name+".png")
    else:
        print("Name has to be a string.")


# Getting the test_data.
test_data = get_data_from_csv(test_data_path)
# Manually testing if we got it how we want it.
# print(test_data.head())


def plot_settings():
    """
    Used to set common settings for a pyplot
    """
    # https://stackoverflow.com/a/332311/11255140
    plot_size = plt.rcParams["figure.figsize"]
    plot_size[0] = 8  # width in inches
    plot_size[1] = 6  # height in inches
    plt.rcParams["figure.figsize"] = plot_size


def number_of_tweets_test(dataframe):
    # https://matplotlib.org/tutorials/introductory/customizing.html#matplotlib-rcparams
    plot_settings()
    # .value_counts() https://www.geeksforgeeks.org/python-pandas-index-value_counts/
    dataframe.airline.value_counts().plot(kind='pie', autopct='%1.0f%%')
    plt.show()


# number_of_tweets_test(test_data)


def sentiment_tweets_test(dataframe):
    plot_settings()
    dataframe.airline_sentiment.value_counts().plot(
        kind='pie', autopct='%1.0f%%', colors=["red", "yellow", "green"])
    plt.show()


# sentiment_tweets_test(test_data)

def bar_plot_test(dataframe):
    plot_settings()
    airline_sentiment = dataframe.groupby(
        ['airline', 'airline_sentiment']).airline_sentiment.count().unstack()
    airline_sentiment.plot(kind='bar')
    save_plot(plt.gcf(), "test")
    plt.show()


bar_plot_test(dataframe=test_data)
