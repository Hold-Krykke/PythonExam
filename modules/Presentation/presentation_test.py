# Presentation file
# Contains charts
# IMPORTS:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import nltk
from presentation_helpers import *
from test_data_generator import make_test_data
from collections import defaultdict

# Test Data Path
test_data_path = "../../data/test_tweets/presentation_test_tweets.csv"

# Getting the test_data.
test_data = get_data_from_csv(test_data_path)


def makeDataframeByDate(tweets):

    trumptweets = defaultdict(list)
    bidentweets = defaultdict(list)

    for tweet in tweets:
        ## IF THE TWEET IS ABOUT TRUMP OR BIDEN
        if "#Biden" in tweet["hashtags"]:
            # Add to Biden
            bidentweets[tweet["date"]].append(
                tweet["sentiment_analysis"]["positive_procent"]
            )
        if "#Trump" in tweet["hashtags"]:
            # Add to Trump
            trumptweets[tweet["date"]].append(
                tweet["sentiment_analysis"]["positive_procent"]
            )

    def Average(lst):
        # GET AVERAGE OF A LIST
        myFloat = sum(lst) / len(lst)
        # print(myFloat)
        return myFloat

    average = {"Trump": {}, "Biden": {}}

    for date in trumptweets.keys():
        average["Trump"][date] = Average(trumptweets[date])
    for date in bidentweets.keys():
        average["Biden"][date] = Average(bidentweets[date])

    print(average)

    df = pd.DataFrame(average)
    print(df)

    return df


def positiveOrNegative(tweets):
    """
    Returns 2 pandas dataframes.
    Columns are Negative, Positive and Uncertain Tweets
    Rows are the date of the tweet.
    The value in the cell is the number of tweets that day.

    Parameters:
        tweets: Array of tweets. 


    Returns:
        Trump: Pandas Dataframe of Trump tweets.
        Biden: Pandas Dataframe of Biden tweets.

    """

    trump_biden_tweets = {"Trump": defaultdict(list), "Biden": defaultdict(list)}

    for tweet in tweets:
        ## IF THE TWEET IS ABOUT TRUMP OR BIDEN
        if "#Biden" in tweet["hashtags"]:
            # Add to Biden
            trump_biden_tweets["Biden"][tweet["date"]].append(
                tweet["sentiment_analysis"]["verdict"]
            )
        if "#Trump" in tweet["hashtags"]:
            # Add to Trump
            trump_biden_tweets["Trump"][tweet["date"]].append(
                tweet["sentiment_analysis"]["verdict"]
            )

    for candidate in trump_biden_tweets.keys():
        for date in trump_biden_tweets[candidate].keys():
            print(candidate, " | DATE: ", date, " | ")
            print(pd.Series(trump_biden_tweets[candidate][date]).value_counts())
            trump_biden_tweets[candidate][date] = pd.Series(
                trump_biden_tweets[candidate][date]
            ).value_counts()

    # print(trump_biden_tweets)

    # Making dataframes. Transposing so the structure is correct.
    trump = pd.DataFrame(trump_biden_tweets["Trump"]).T  # .T = Transpose
    biden = pd.DataFrame(trump_biden_tweets["Biden"]).T
    return trump, biden


def lineGraph(mydict):
    # print("VALUE COUNTS")
    # print(df.Trump.apply(value_counts()))
    # print(df.Biden.value_counts())
    trump = pd.DataFrame(mydict["Trump"]).T
    biden = pd.DataFrame(mydict["Biden"]).T
    ax = trump.plot(kind="line", color=["red"])
    biden.plot(kind="line", color=["blue"], ax=ax, rot=30)


def barPlot(df):
    # df.value_counts()
    # print("VALUE COUNTS")
    # print(df)
    df.groupby(["Trump", "Biden"])
    df.plot(kind="bar", rot=0, color=["red", "blue"])
    # rot=0 is that x-labels are horizontal


# TESTING
object_test_data = []
for i in range(1000):
    object_test_data.append(make_test_data())

trump, biden = positiveOrNegative(object_test_data)


def barPlot(trump, biden):
    print("trump\n", trump)
    print("biden\n", biden)
    trump.plot(kind="bar", rot=0, title="Trump")
    plt.show()
    biden.plot(kind="bar", rot=0, title="Biden")
    plt.show()


barPlot(trump, biden)
# df = makeDataframeByDate(object_test_data)

# lineGraph(mydict)
# plt.show()
# barPlot(df)
# plt.show()
