import datetime
from modules.web_scraper import get_tweets
from modules.Preprocessing import handle_tweet_data
# from modules.Preprocessing import handle_tweet_data
# from modules.Sentiment_Analysis import train_model_if_necessary, analyze_many_tweets
# import modules.presentation as presentation
import argparse


#########CUSTOM TYPES#########
def _restricted_float(val: float):
    try:
        val = float(val)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{val} not a floating-point literal")

    if 0.0 < x > 1.0:
        raise argparse.ArgumentTypeError(f"{val} not in range [0.0, 1.0]")
    return val


#########CUSTOM TYPES#########

#########HELPER METHODS#########

class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter):
    """
    Allows us to use two formatters for argparse instead of only the default 1 (hackish)
    https://stackoverflow.com/a/18462760
    """

    def _split_lines(self, text, width):
        # https://stackoverflow.com/a/29498894
        # modify super to add newline between arguments
        lines = super()._split_lines(text, width)
        if text.endswith('\n'):  # custom newline
            lines += ['']
        else:
            lines += ['']  # also add newline between different arguments
        return lines


def _default_date():
    """
    Generates today and five days from now for use with default values of the date-argument
    """
    today = datetime.date.today()
    five_days_from_now = today + datetime.timedelta(days=5)
    # create readable format, as should be input
    return ' '.join([today.strftime('%Y-%m-%d'), five_days_from_now.strftime('%Y-%m-%d')])
#########HELPER METHODS#########


# def prepare_data_and_create_plot(hashtags: list, tweet_amount: int, fresh_search: bool, file_name, start_date, end_date, plot_type, search_for: dict, remove_sentiment: str):
#     """
#     This is the main method which calls several helper methods
#     """

#     # tweet_list a list of tweet objects (not a list of strings)
#     tweet_list = web_scraper.get_tweets(tweet_amount, fresh_search, hashtags)
#     print("Done scraping...")

#     # tweet_data is a tuple with a list and 2 dicts: tweets: list[dict[str, str]], hashtag_stats: dict, mention_stats: dict
#     tweets, hashtag_stats, mention_stats = Preprocessing.handle_tweet_data(
#         tweet_list)
#     print("Done preprocessing...")

#     # analyzed_tweet_data is a list of tweet dicts with the new data from the SA
#     analyzed_tweet_data = Sentiment_Analysis.analyze_many_tweets(tweets)
#     print("Done analyzing...")

#     # filtering data to get only data between the two specified dates
#     filtered_data = presentation.get_tweets_in_daterange(
#         analyzed_tweet_data, start_date, end_date)
#     print("Done filtering on date...")

#     # filter for specific hashtag, mention or url
#     if (list(search_for.keys())):
#         filtered_data = presentation.get_by_key_value(
#             filtered_data, list(search_for.keys())[0], list(search_for.values())[0])
#         print("Done filtering for hashtag, mention or url...")

#     # filter sentiment if possible
#     if (remove_sentiment):
#         filtered_data = presentation.remove_sentiment(
#             filtered_data, remove_sentiment)
#         print("Done removing sentiment...")

#     # Getting plot data from the get_sentiment function
#     PLOT_ME = presentation.get_sentiment(filtered_data)
#     print("Done getting sentiment df for plotting...")

#     # Create plot and save so the endpoint can send the .png file
#     if plot_type == "bar":
#         presentation.bar_plot(PLOT_ME, file_name, file_name)
#     if plot_type == "line":
#         presentation.line_plot(PLOT_ME, file_name, file_name)
#     if plot_type == "pie":
#         presentation.pie_chart(PLOT_ME, file_name, file_name)


if __name__ == "__main__":
    # train_model_if_necessary()
    parser = argparse.ArgumentParser(
        prog='TweetScraper9000',
        formatter_class=CustomFormatter,
        description="""
        A program that scrapes Twitter for hashtags and performs a sentiment analysis on the results. 
        Presents results in a chosen chart format.
        """,
        usage='%(prog)s',
        epilog='Source: https://github.com/Hold-Krykke/PythonExam\nCreated by: Camilla, Malte, Asger, Rúni')
    parser.add_argument(
        '-t', '--hashtags',
        help="The hashtags to scrape.\nEXAMPLE: 'trump biden'\n-REQUIRED-",
        nargs='+',
        required=True,
        type=str,
        dest='hashtags')

    # TODO add newline support for examples https://stackoverflow.com/a/22157136
    # add theese advanced arguments at the end TODO
    # TODO make da
    # TODO check and convert (date) arguments then call main method
    # TODO Check hashtag format before calling
    # TODO Custom date types
    # Check sentiment types
    # TODO warn user that plt.show() is blocking
    # check plot type, .lower()
    parser.add_argument(
        '-p', '--plot',
        help="Plot chart type, choose one. VALUES=[bar, line, pie]\n",
        type=str,
        default='bar',
        dest='plot_type')
    parser.add_argument(
        '-l', '--local',
        help="Pass to attempt scraping from local files.\n",
        action='store_true',
        dest='fresh_search',
        default=False)
    parser.add_argument(
        '-c', '--count',
        help="The amount of tweets to search for.\n",
        type=int,
        default=300,
        dest='tweet_count')
    parser.add_argument(
        '-d', '--date',
        help="The date range (yyyy-mm-dd) to search for. \nEXAMPLE: '2020-05-01 2020-05-05'.\n",
        nargs=2,
        type=str,
        default=_default_date(),
        dest='date')
    parser.add_argument(
        '-f', '--filename',
        help="The filename to store plots in (if omitted will show plots instead)\n",
        type=str,
        dest='filename')
    parser.add_argument(
        '-s', '--sentiment',
        help="Ignore specific sentiment.\nVALUES=[Positive, Negative, Uncertain]\n",
        type=str,
        dest='remove_sentiment')
    parser.add_argument(
        '-sh',
        help="Filter result data by specific hashtags.\nEXAMPLE: '#Trump #Biden'\n",
        type=str,
        nargs='+',
        dest='search_hashtags')
    parser.add_argument(
        '-sm',
        help="Filter result data by specific mentions.\nEXAMPLE: '@JoeBiden @folketinget'\n",
        type=str,
        nargs='+',
        dest='search_mentions')
    parser.add_argument(
        '-cl',
        help="The lower float value for determining if a sentiment is deemed uncertain.\nEXAMPLE: 0.15.\nVALUES: [0.00-1.00]",
        type=_restricted_float,
        default=0.25,
        metavar='ADVANCED: certainty low',
        dest='certainty_low')
    parser.add_argument(
        '-ch',
        help="The higher float value for determining if a sentiment is deemed uncertain.\nEXAMPLE: 0.65.\nVALUES: [0.00-1.00]",
        type=_restricted_float,
        default=0.75,
        metavar='ADVANCED: certainty high',
        dest='certainty_high')
    print(parser.parse_args())
    args_dict = vars(parser.parse_args())
    print(args_dict)
    print(args_dict['hashtags'])
    hashtags = args_dict
    print(hashtags)
