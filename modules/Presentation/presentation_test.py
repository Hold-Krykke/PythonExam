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
    return trump_biden_tweets


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


# TESTING
object_test_data = []
for i in range(1000):
    object_test_data.append(make_test_data())

mydict = positiveOrNegative(object_test_data)


def dictBarPlot(mydict):
    trump = pd.DataFrame(mydict["Trump"]).T
    biden = pd.DataFrame(mydict["Biden"]).T
    print("trump\n", trump)
    print("biden\n", biden)
    plot_settings()
    trump.plot(kind="bar", rot=0, title="Trump")
    plt.show()
    plot_settings()
    biden.plot(kind="bar", rot=0, title="Biden")
    plt.show()


dictBarPlot(mydict)
# df = makeDataframeByDate(object_test_data)

# lineGraph(mydict)
# plt.show()
# barPlot(df)
# plt.show()
