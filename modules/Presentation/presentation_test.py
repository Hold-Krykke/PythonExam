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

    # Making a somewhat empty dict to contain the info we need.
    trump_biden_tweets = {"Trump": defaultdict(list), "Biden": defaultdict(list)}

    for tweet in tweets:
        ## IF THE TWEET IS ABOUT TRUMP OR BIDEN
        if "#Biden" in tweet["hashtags"]:
            # Add to Biden
            # We only want the sentiment_analysis verdict and the date here.
            # Date is the key. Verdict is added to the value array.
            # "date": [Positive, Negative, Uncertain, Negative, etc, etc]
            trump_biden_tweets["Biden"][tweet["date"]].append(
                tweet["sentiment_analysis"]["verdict"]
            )
        if "#Trump" in tweet["hashtags"]:
            # Add to Trump
            trump_biden_tweets["Trump"][tweet["date"]].append(
                tweet["sentiment_analysis"]["verdict"]
            )

    # We now take .value_counts() and put that as the dates value:
    # .value_counts() https://www.geeksforgeeks.org/python-pandas-index-value_counts/
    for candidate in trump_biden_tweets.keys():
        for date in trump_biden_tweets[candidate].keys():
            # print(candidate, " | DATE: ", date, " | ")
            # print(pd.Series(trump_biden_tweets[candidate][date]).value_counts())
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


def pieChart(trump, biden, sentiment):
    """
    Parameters: 
        trump & biden: DataFrame: has to come from positiveOrNegative
        sentiment: String: Positive, Negative or Uncertain

    
    """
    print(trump, "\n", biden)
    df = pd.Series(
        {"Trump": trump[sentiment].sum(), "Biden": biden[sentiment].sum()}
    ).plot(
        kind="pie",
        autopct="%1.0f%%",
        colors=["red", "blue"],
        title=f"{sentiment} tweets.",
    )

    print(df)

    # trump_sentiment = [trump[sentiment].sum()]  # sum up tweets
    # biden_sentiment = [biden[sentiment].sum()]
    # trump_string = f"Trump {sentiment} tweets"
    # biden_string = f"Biden {sentiment} tweets"
    # df = pd.DataFrame(
    #     {trump_string: trump_sentiment, biden_string: biden_sentiment}, index=[0]
    # )

    plt.show()


def barPlot(df):
    # df.value_counts()
    # print("VALUE COUNTS")
    # print(df)
    df.groupby(["Trump", "Biden"])
    df.plot(kind="bar", rot=0, color=["red", "blue"])
    # rot=0 is that x-labels are horizontal


def barPlot(trump, biden):
    print("trump\n", trump)
    print("biden\n", biden)
    trump.plot(kind="bar", rot=0, title="Trump")
    plt.show()
    biden.plot(kind="bar", rot=0, title="Biden")
    plt.show()


# TESTING
object_test_data = []
for i in range(1000):
    object_test_data.append(make_test_data())

trump, biden = positiveOrNegative(object_test_data)


# barPlot(trump, biden)
pieChart(trump, biden, "Positive")
# df = makeDataframeByDate(object_test_data)

# lineGraph(mydict)
# plt.show()
# barPlot(df)
# plt.show()


def makeDataframeByDate(tweets):
    """
    Might be outdated.
    """

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
