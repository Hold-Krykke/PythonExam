from modules.web_scraper import get_tweets
from modules.Preprocessing import handle_tweet_data
from modules.Sentiment_Analysis import train_model_if_necessary, analyze_many_tweets
import modules.presentation as presentation
import argparse





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
