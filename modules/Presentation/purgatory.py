# CONTAINS OUTDATED TESTING

# Manually testing if we got it how we want it.
# print(test_data.head())
import numpy as np


# FUNCTIONS BELOW MIGHT BE OUTDATED
# EARLIER VERSIONS OF CODE
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

    print(trump_biden_tweets)

    # Making dataframes. Transposing so the structure is correct.
    trump = pd.DataFrame(trump_biden_tweets["Trump"]).T  # .T = Transpose
    biden = pd.DataFrame(trump_biden_tweets["Biden"]).T
    return trump.sort_index(), biden.sort_index()


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


# Test Data Path
test_data_path = "../../data/test_tweets/presentation_test_tweets.csv"

# Getting the test_data.
test_data = get_data_from_csv(test_data_path)
print(np.linspace(0, 1, 101))

# Start-point is this tutorial: https://stackabuse.com/python-for-nlp-sentiment-analysis-with-scikit-learn//
def number_of_tweets_test(dataframe):
    # https://matplotlib.org/tutorials/introductory/customizing.html#matplotlib-rcparams
    plot_settings()
    array_of_airline_names = dataframe.airline
    # .value_counts() https://www.geeksforgeeks.org/python-pandas-index-value_counts/
    unique_counts_of_airline = array_of_airline_names.value_counts()
    pie_plot = unique_counts_of_airline.plot(kind="pie", autopct="%1.0f%%")
    plt.show()


# number_of_tweets_test(test_data)


def sentiment_tweets_test(dataframe):
    plot_settings()
    dataframe.airline_sentiment.value_counts().plot(
        kind="pie", autopct="%1.0f%%", colors=["red", "yellow", "green"]
    )
    plt.show()


# sentiment_tweets_test(test_data)


def bar_plot_test(dataframe):
    # plot_settings()
    airline_sentiment = (
        dataframe.groupby(["airline", "airline_sentiment"])
        .airline_sentiment.count()
        .unstack()
    )
    airline_sentiment.plot(kind="bar")
    # save_plot(plt.gcf(), "test")
    plt.show()


# bar_plot_test(dataframe=test_data)


# trumpaverage = defaultdict()
# bidenaverage = defaultdict()

# for date in trumptweets.keys():
#     trumpaverage[date].append(Average(trumptweets[date]))
# for date in bidentweets.keys():
#     bidenaverage[date].append(Average(bidentweets[date]))

# trumpaverage = {}
# bidenaverage = {}

# for date in trumptweets.keys():
#     trumpaverage[date] = Average(trumptweets[date])
# for date in bidentweets.keys():
#     bidenaverage[date] = Average(bidentweets[date])

# print("TRUMP AVERAGE PER DATE")
# print(trumpaverage)
# print("BIDEN AVERAGE PER DATE")
# print(bidenaverage)

# df = pd.DataFrame([trumpaverage, bidenaverage])
# print()
# print(df)
# print()
# print()
# print(df.unstack())
# df = df.astype(float)
# print("ASS")
# print(df)


# date { Trump: [sentiment results], Biden}


# print(make_test_data(), "\n\n", make_test_data())
# print(object_test_data)


# print("TRUMP TWEETS:")
# print(trumptweets)
# print()
# print()
# print("BIDEN TWEETS:")
# print(bidentweets)
