from typing import List
from datetime import datetime, timedelta
from modules.web_scraper import get_tweets
from modules.Preprocessing import handle_tweet_data
# from modules.Preprocessing import handle_tweet_data
# from modules.Sentiment_Analysis import train_model_if_necessary, analyze_many_tweets
# import modules.presentation as presentation
import argparse
import re

_REGEX_CHAR_MATCHER_HASHTAGS = re.compile('[^A-Za-z0-9]')

#########CUSTOM TYPES#########


def _restricted_float(val: float):
    """
    Only allow float values within our range [0.00-1.00]
    """
    try:
        val = float(val)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{val} not a floating-point literal")

    if 0.0 < val > 1.0:
        raise argparse.ArgumentTypeError(f"{val} not in range [0.0, 1.0]")
    return val


def _restricted_dates(date):
    """
    This method is called by argparse on a per-argument basis, meaning it calls it twice
    Argparse itself validates nargs=2
    """
    _dates = list(date)
    print('_DATES', _dates)
    print('DATES_HERE', date)
    try:
        return_date = datetime.strptime(date, '%Y-%m-%d').date()
        # end_date = datetime.strptime(dates[1], '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Could not parse dates. Did you format them yyyy-mm-dd? Dates received:\n{date}")

    # if start_date > end_date:
    #     raise argparse.ArgumentTypeError(
    #         f"Start date {start_date} may not be later than end date {end_date}")
    # return [start_date, end_date, 55]
    return return_date


def _restricted_sentiment(val: str):
    """
    Only allow given sentiments
    """
    sentiments = ["Positive", "Negative", "Uncertain"]
    try:
        val = str(val).title()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{val} could not be parsed to a string")

    if val not in sentiments:
        raise argparse.ArgumentTypeError(
            f"{val} is not a valid sentiment. Possible values: {', '.join(sentiments)}")
    return val


def _restricted_plots(val: str):
    """
    Only allow given plots
    """
    plots = ["bar", "line", "pie"]
    try:
        val = str(val).lower()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{val} could not be parsed to a string")

    if val not in plots:
        raise argparse.ArgumentTypeError(
            f"{val} is not a valid plot type. Possible values: {', '.join(plots)}")
    return val


def _restricted_hashtags(val: str):
    """
    Only allow hashtags that follow our standards.
    Typically we remove #-symbols even if a user passed them.
    """
    try:
        val = str(val).lower()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{val} could not be parsed to a string")

    val = re.sub(_REGEX_CHAR_MATCHER_HASHTAGS, "", val)
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


def _default_dates():
    """
    Generates today and five days from now for use with default values of the date-argument
    """
    today = datetime.now().date()
    five_days_from_now = today + timedelta(days=5)
    # create readable format, as should be input
    # return [today.strftime('%Y-%m-%d'), five_days_from_now.strftime('%Y-%m-%d')]
    return [today, five_days_from_now]
#########HELPER METHODS#########


# TODO Check hashtag format before calling
# TODO CHECK DATE RANGE <> OUTSIDE FUNCTION
# TODO warn user that plt.show() is blocking
# TODO region ARGPARSE ARGUMENTS


def prepare_data(hashtags: List,
                 tweet_amount: int,
                 fresh_search: bool,
                 file_name: str,
                 dates: List[datetime.date],
                 plot_type: str,
                 search_mentions: List,
                 search_hashtags: List,
                 search_urls: List,
                 remove_sentiment: str,
                 certainty_low: float,
                 certainty_high: float):
    # Verify data
    start_date, end_date = dates
    if (start_date > end_date):
        raise ValueError(
            f'Start date {start_date} may not be later than end date {end_date}')

    #tweet_list = get_tweets(tweet_amount, fresh_search, hashtags)
    #print("Done scraping...")
    # print(tweet_list[:5])


if __name__ == "__main__":
    # train_model_if_necessary()
    # region ARGPARSE
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
        'hashtags',
        help="The hashtags to scrape.\nEXAMPLE: 'trump biden'\n-REQUIRED-",
        nargs='+',
        type=_restricted_hashtags)
    parser.add_argument(
        '-p', '--plot',
        help="Plot chart type, choose one. VALUES=[bar, line, pie]\n",
        type=_restricted_plots,
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
        type=_restricted_dates,
        default=_default_dates(),
        dest='date')
    parser.add_argument(
        '-f', '--filename',
        help="The filename to store plots in.\n(if omitted will show plots instead)\n",
        type=str,
        dest='filename')
    parser.add_argument(
        '-s', '--sentiment',
        help="Ignore specific sentiment.\nVALUES=[Positive, Negative, Uncertain]\n",
        type=_restricted_sentiment,
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
        '-su',
        help="Filter result data by specific URLs.\nEXAMPLE: 'https://pic.twitter.com/'\n",
        type=str,
        nargs='+',
        dest='search_urls')
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
    # endregion
    # turn Namespace object into usable dict
    args_dict = vars(parser.parse_args())
    print(args_dict)
    print(args_dict['hashtags'])
    from operator import itemgetter
    # extract items from dict
    hashtags, plot_type, fresh_search, tweet_count, date, filename, remove_sentiment, search_hashtags, search_mentions, search_urls, certainty_low, certainty_high = itemgetter(
        'hashtags', 'plot_type', 'fresh_search', 'tweet_count', 'date', 'filename', 'remove_sentiment', 'search_hashtags', 'search_mentions', 'search_urls', 'certainty_low', 'certainty_high')(args_dict)
    # prepare_data(hashtags, tweet_count, fresh_search, filename, date, plot_type, search_mentions,
    #             search_hashtags, search_urls, remove_sentiment, certainty_low, certainty_high)
    # prepare_data_and_create_plot()
