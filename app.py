from modules.web_scraper import get_tweets
from modules.Preprocessing import get_tweet_data
from modules.Sentiment_Analysis import train_model_if_necessary, analyze_many_tweets
import modules.presentation as presentation
import argparse


# def do_everything(hashtags: list, file_name, start_date, end_date, plot_type):
#     # tweet_list a list of tweet objects (not a list of strings)
#     print(f'Scraping hashtags: {", ". join(hashtags)}...')
#     tweet_list = get_tweets(100, False, hashtags)

#     print("Preprocessing...")
#     tweet_data, hashtag_stats, mentions_stats = get_tweet_data(tweet_list)

#     # analyzed_tweet_data is a list of tweet dicts with the new data from the SA
#     print('Performing sentiment analysis...')
#     analyzed_tweet_data = analyze_many_tweets(tweet_data)

#     # filtering data to get only data between the two specified dates
#     print("Filtering data by dates")
#     filtered_data = presentation.get_tweets_in_daterange(
#         analyzed_tweet_data, start_date, end_date)

#     # Getting plot data from the get_sentiment function
#     print("Filtering data by their sentiment")
#     PLOT_ME = presentation.get_sentiment(filtered_data)

#     # Create plot and save so the endpoint can send the .png file
#     if plot_type == "bar":
#         presentation.bar_plot(PLOT_ME, file_name, file_name)
#     if plot_type == "line":
#         presentation.line_plot(PLOT_ME, file_name, file_name)
#     if plot_type == "pie":
#         presentation.pie_chart(PLOT_ME, file_name, file_name)


if __name__ == "__main__":
    # train_model_if_necessary()
    parser = argparse.ArgumentParser(prog='TweetScraper9000',
                                     description='A program that scrapes twitter for hashtags and performs a sentiment analysis on the results.',
                                     usage='%(prog)s',
                                     epilog='Source: https://github.com/Hold-Krykke/PythonExam/')
    parser.add_argument(
        '-t', '--hashtags', help="The hashtags to scrape. Write them seperated by space, without the # character. EXAMPLE: 'trump biden'", nargs='+', required=True, type=str)

    # TODO add newline support for examples https://stackoverflow.com/a/22157136
    # add theese advanced arguments at the end TODO
    # TODO make da
    parser.add_argument(
        '-d', '--date', help="The date range (yyyy-mm-dd) to search for. EXAMPLE: '2020-05-01 2020-05-05", nargs=2, type=str)
    parser.add_argument(
        '-f', '--filename', help="The filename to store plots in (if omitted will show plots instead)", type=str)
    parser.add_argument(
        '-cl', help="The lower float value for determining if a sentiment is deemed uncertain. (percentage) EXAMPLE: 0.15", type=float, default=0.75, metavar='ADVANCED: certainty low')
    parser.add_argument(
        '-ch', help="The higher float value for determining if a sentiment is deemed uncertain. (percentage) EXAMPLE: 0.65", type=float, default=0.25, metavar='ADVANCED: certainty high')
    print(parser.parse_args())
