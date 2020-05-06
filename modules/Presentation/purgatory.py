# Manually testing if we got it how we want it.
# print(test_data.head())


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

