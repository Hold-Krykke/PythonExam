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


# Getting the test_data.
test_data = get_data_from_csv(test_data_path)
# Manually testing if we got it how we want it.
print(test_data.head())


def number_of_tweets_test(dataframe):
    # https://matplotlib.org/tutorials/introductory/customizing.html#matplotlib-rcparams
    plot_size = plt.rcParams["figure.figsize"]
    print(plot_size[0])
    print(plot_size[1])

    plot_size[0] = 8
    plot_size[1] = 6
    plt.rcParams["figure.figsize"] = plot_size
    # .value_counts() https://www.geeksforgeeks.org/python-pandas-index-value_counts/
    dataframe.airline.value_counts().plot(kind='pie', autopct='%1.0f%%')


# number_of_tweets_test(test_data)
# plt.show()


def sentiment_tweets_test(dataframe):
    plot_size = plt.rcParams["figure.figsize"]
    print(plot_size[0])
    print(plot_size[1])
    plot_size[0] = 8
    plot_size[1] = 6
    plt.rcParams["figure.figsize"] = plot_size
    dataframe.airline_sentiment.value_counts().plot(
        kind='pie', autopct='%1.0f%%', colors=["red", "yellow", "green"])


sentiment_tweets_test(test_data)
plt.show()
