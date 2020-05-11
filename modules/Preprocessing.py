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


def _handle_date(date_string: str):
    """
    We receive dates from tweets in the format 'yyyy-m-d'.
    This function returns a datetime object with proper formatting (yyyy-mm-dd)
    """
    # return date(*[int(date) for date in date_string.split(',')]) # sorry we didnt get to use you ;(
    return datetime.strptime(date_string, '%Y,%m,%d').date()


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

        # remove hyperlinks
        token = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', token)
        # remove special chars, numbers, inc emojies
        token = re.sub("[^A-Za-z]", "", token)

        if tag.startswith("NN"): #noun
            pos = 'n'
        elif tag.startswith('VB'): #verb
            pos = 'v'
        else: #adjective
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        #lemmatize sentence (bring word from full form to base form) (running -> run)
        token = lemmatizer.lemmatize(token, pos)
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
    # prepare stats_format for
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
        if (tweet_text != None and any(symbol in tweet_text for symbol in ['#', '@'])):
            for word in tweet_text.split(' '):
                if word.startswith('#'):
                    # add to local hashtags
                    tweet['hashtags'].append(word)
                    # add to overall hashtags
                    hashtag_stats[word.lower()] = hashtag_stats.get(word.lower(), 0) + 1
                    # remove hashtag
                    tweet_text = tweet_text.replace(word, '')
                if word.startswith('@'):
                    # add to local hashtags
                    tweet['mentions'].append(word)
                    # add to overall hashtags
                    mention_stats[word.lower()] = mention_stats.get(word.lower(), 0) + 1
                    # remove mention
                    tweet_text = tweet_text.replace(word, '')
        # handle dates
        tweet['date'] = _handle_date(tweet['date'])
        # add emoji descriptions to tweet text
        if tweet['emojis']:
            tweet_text += ' '.join(tweet['emojis'])
        # clear unused words, numbers, symbols and the like
        tweet['tweet'] = remove_noise(tweet_text)  # must finish with this
    # sort hashtag and mention stats
    hashtag_stats = {k: v for k, v in sorted(hashtag_stats.items(), key=lambda item: item[1], reverse=True)}
    mention_stats = {k: v for k, v in sorted(mention_stats.items(), key=lambda item: item[1], reverse=True)}
    return tweets, hashtag_stats, mention_stats