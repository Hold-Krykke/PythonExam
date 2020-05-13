from datetime import datetime
import re
import string
from typing import List, Dict
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize


# lazy load stopwords
_stopwords = stopwords.words('english')
_stopwords.extend(['twitter', 'nt'])
_REGEX_URL_MATCHER = re.compile(
    '(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)')
_REGEX_CHAR_MATCHER = re.compile('[^A-Za-z]')
# allows hashtags, mentions with letters & numbers
_REGEX_CHAR_MATCHER_TWEETS = re.compile('[^A-Za-z0-9#@]')


def _handle_date(date_string: str):
    """
    We receive dates from tweets in the format 'yyyy-m-d'.
    This function returns a datetime object with proper formatting (yyyy-mm-dd)
    """
    # return date(*[int(date) for date in date_string.split(',')]) # sorry we didnt get to use you ;(
    return datetime.strptime(date_string, '%Y,%m,%d').date()


def sort_dict(unsorted_dict: dict, descending: bool = True):
    """
    Sorts a dict by value-fields using lambda.  

    unsorted_dict: dict to sort  

    descending: sort descending (True) or ascending (False)

    # Returns  
    Same dict but sorted

    """
    return {k: v for k, v in sorted(unsorted_dict.items(), key=lambda item: item[1], reverse=descending)}


def remove_noise(tweet: str):
    """
    Removes noise from the tweets by:
    Tokenizing (Splits sentences into array of words)
    Removes hyperlinks with regex
    Removes special characters (primarily used for emojis) as well as numbers.
    _____________
    Is used for cleaning both scraped data as well as cleaning the data for training the model
    """
    cleaned_tokens = []
    tweet_tokens = word_tokenize(tweet)
    for token, tag in pos_tag(tweet_tokens):
        if tag.startswith("NN"):  # noun
            pos = 'n'
        elif tag.startswith('VB'):  # verb
            pos = 'v'
        else:  # adjective
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        # lemmatize sentence (bring word from full form to base form) (running -> run)
        token = lemmatizer.lemmatize(token, pos)

        # remove hyperlinks
        token = re.sub(_REGEX_URL_MATCHER, '', token)
        # remove special chars, numbers, inc emojies
        token = re.sub(_REGEX_CHAR_MATCHER, "", token)

        # remove empty tokens, punctuations and stopwords
        token = token.lower().strip()
        if len(token) > 1 and token not in string.punctuation and token not in _stopwords:
            cleaned_tokens.append(token)
    return cleaned_tokens


def get_tweet_data(tweets: List[Dict[str, str]]):
    """
    This function takes a list of tweets, containing web scraped dicts (in particular raw_text) and grabs useful information from it.

    As of now it looks for hashtags (#), mentions (@) and emojis.

    Following this, it cleans up the data using remove_noise().

    ## Returns
    Returns the same object with fields:  

    hashtags, mentions, tweet.

    As well as stats for hashtags and mentions
    >>> tweets, hashtag_stats, mention_stats
    """
    # prepare stats_format
    hashtag_stats = {}
    mention_stats = {}

    for tweet in tweets:
        # prepare format
        tweet['hashtags'] = tweet.get('hashtags', [])
        tweet['mentions'] = tweet.get('mentions', [])
        tweet_text = tweet.get('raw_text')
        # remove newline characters (necessary to add spaces between words)
        tweet_text = tweet_text.replace('\n', ' ')

        # check text for hashtags or mentions
        if (any(symbol in tweet_text for symbol in ['#', '@'])):
            for word in tweet_text.split(' '):
                if word.startswith('#'):
                    # clean hashtag
                    clean_word = re.sub(_REGEX_CHAR_MATCHER_TWEETS, "", word)
                    # add to local hashtags
                    tweet['hashtags'].append(clean_word)
                    # add to overall hashtags
                    hashtag_stats[clean_word.lower()] = hashtag_stats.get(
                        clean_word.lower(), 0) + 1
                    # remove hashtag
                    tweet_text = tweet_text.replace(word, '')
                if word.startswith('@'):
                    # clean mention
                    clean_word = re.sub(_REGEX_CHAR_MATCHER_TWEETS, "", word)
                    # add to local hashtags
                    tweet['mentions'].append(clean_word)
                    # add to overall hashtags
                    mention_stats[clean_word.lower()] = mention_stats.get(
                        clean_word.lower(), 0) + 1
                    # remove mention
                    tweet_text = tweet_text.replace(word, '')
        # handle dates
        tweet['date'] = _handle_date(tweet['date'])
        # add emoji descriptions to tweet text
        if tweet['emojis']:
            tweet_text += ' '.join(tweet['emojis'])
        # clear unused words, numbers, symbols and the like
        tweet['tweet'] = remove_noise(tweet_text)  # must finish with this
    # sort hashtag and mention stats by their values
    hashtag_stats = sort_dict(hashtag_stats)
    mention_stats = sort_dict(mention_stats)
    return tweets, hashtag_stats, mention_stats
