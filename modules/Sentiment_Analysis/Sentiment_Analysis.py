from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
import re
import string
from nltk.corpus import stopwords
from nltk import FreqDist
import random
from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from ala_Runi_tweets import test_tweets  # should be removed when merged
from ala_scraped import scraped_tweets  # should be removed when merged

# These are the only methods that should be called from other modules:
# train_model_if_necessary()
# analyze_many_tweets(scraped_tweets, 0.25, 0.75)


########################################################################################################################################################################
from datetime import datetime
from typing import List, Dict


_stop_words = stopwords.words('english')
_stop_words.extend(['twitter', 'nt'])


def _handle_date(date_string: str):
    """
    We receive dates from tweets in the format 'yyyy-m-d'.
    This function returns a datetime.date object with proper formatting (yyyy-mm-dd)
    """
    # return date(*[int(date) for date in date_string.split(',')]) # sorry we didnt get to use you ;(
    return datetime.strptime(date_string, '%Y,%m,%d').date()


def _remove_noise(tweet: str):
    """
    Removes noise from the tweets by:
    Tokenizing (Splits sentences into array of words)
    Removes hyperlinks with regex
    Removes special characters (primarily used for emojis) as well as numbers.
    """
    cleaned_tokens = []
    tweet_tokens = word_tokenize(tweet)
    for token, tag in pos_tag(tweet_tokens):

        # remove hyperlinks
        token = re.sub(
            '(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', token)
        # remove special chars, numbers, inc emojies
        token = re.sub("[^A-Za-z]", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        # print('tokenb4', token)
        token = lemmatizer.lemmatize(token, pos)
        # print('tokenAfter', token)
        # remove empty tokens, punctuations and stopwords
        # use substring search (find) instead?
        token = token.lower().strip()
        if len(token) > 1 and token not in string.punctuation and token not in _stop_words:
            cleaned_tokens.append(token)
    return cleaned_tokens


def get_tweet_data(tweets: List[Dict[str, str]]):
    """
    This function takes a list of tweets, containing web scraped dicts (in particular raw_text) and grabs useful information from it.

    As of now it looks for hashtags (#), mentions (@) and emojis.

    Following this, it cleans up the data and returns the same object with fields:
    hashtags, mentions, tweet
    """
    # create for-loop on argument "tweets"
    for tweet in tweets:
        # prepare format
        tweet['hashtags'] = tweet.get('hashtags', [])
        tweet['mentions'] = tweet.get('mentions', [])
        tweet_text = tweet.get('raw_text')
        # remove newline characters (necessary to add spaces between words)
        tweet_text = tweet_text.replace('\n', ' ')

        # check text for hashtags or mentions
        if (tweet_text != None and '#' or '@' in tweet_text):
            for word in tweet_text.split(' '):
                if word.startswith('#'):
                    tweet['hashtags'].append(word)
                    tweet_text = tweet_text.replace(word, '')  # remove hashtag
                if word.startswith('@'):
                    tweet['mentions'].append(word)
                    tweet_text = tweet_text.replace(word, '')  # remove mention
        # handle dates
        tweet['date'] = _handle_date(tweet['date'])
        # add emoji descriptions to tweet text
        if tweet['emojis']:
            tweet_text += ' '.join(tweet['emojis'])
        # clear unused words, numbers, symbols and the like
        tweet['tweet'] = _remove_noise(tweet_text)  # must finish with this
        print("tweet['tweet']")
        print(tweet['tweet'])
    # handle hashtag stats here or in presentation
    # handle mention stats here or in presentation
    return tweets

########################################################################################################################################################################


####################### Prepare the Data ########################
def _prepare_training_data_for_model():
    """
    This function gathers the training data sets from nltk corpus twitter_samples, calls the preprocessing functions and then
    marks the datasets with "Positive" or "Negative", before finally merging and returning them as one dataset. 
    This is the data used to train our model. 
    """
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')

    positive_preprocessed_tokens = []
    negative_preprocessed_tokens = []

    for tweet in positive_tweets:
        positive_preprocessed_tokens.append(_remove_noise(tweet))  # _remove_noise should be called correctly from Rúnis module

    for tweet in negative_tweets:
        negative_preprocessed_tokens.append(_remove_noise(tweet))  # _remove_noise should be called correctly from Rúnis module

    positive_formatted_tokens = _get_tweets_for_model(positive_preprocessed_tokens)
    negative_formatted_tokens = _get_tweets_for_model(negative_preprocessed_tokens)

    positive_dataset = [(tweet_dict, "Positive") for tweet_dict in positive_formatted_tokens]
    negative_dataset = [(tweet_dict, "Negative") for tweet_dict in negative_formatted_tokens]
    dataset = positive_dataset + negative_dataset

    return dataset


def _get_tweets_for_model(preprocessed_token_list):
    """
    Util function that yields one token at a time in this form, which is required by the model: 
    ({'top': True, 'engage': True, 'member': True, 'community': True, 'week': True}, 'Positive')
    """
    for tweet_tokens in preprocessed_token_list:
        yield dict([token, True] for token in tweet_tokens)
####################### Prepare the Data ########################


####################### Analyze the Data ########################
_training_dataset = _prepare_training_data_for_model()
_classifier_has_been_trained = False
_classifier = None


def analyze_many_tweets(tweets_list, uncertain_low: float, uncertain_high: float):
    """
    Takes in a list of scraped tweets and calls the analyzer for each, before appending the analyzed 
    result to the tweet and returning the list
    """
    analyzed_tweets = get_tweet_data(tweets_list)
    for item in analyzed_tweets:
        tweet = item.get("tweet")
        result = _analyze_tweet(tweet, uncertain_low, uncertain_high)
        item["sentiment_analysis"] = [result]
    return analyzed_tweets


def _analyze_tweet(tweet, uncertain_low: float, uncertain_high: float):
    """
    This function is the analyzer. It trains the model if not already trained (should only happen once per run),
    classifies the tweet and appends the results to the result-object, which is then returned.
    """
    train_model_if_necessary()
    probability_distrubution = _classifier.prob_classify(dict([token, True] for token in tweet))

    result = {}
    result["verdict"] = probability_distrubution.max()
    result["positive_procent"] = round(probability_distrubution.prob("Positive"), 2)
    result["negative_procent"] = round(probability_distrubution.prob("Negative"), 2)
    if (result.get("positive_procent") < uncertain_high and result.get("positive_procent") > uncertain_low):
        result["verdict"] = "Uncertain"

    return result


def train_model_if_necessary():
    """
    This function checks if the model has been trained, and trains the model if it hasn't been trained.
    It should be called from the Main.py on program start, as the training is time-consuming. This should only
    occur once per run. 
    """
    global _classifier_has_been_trained
    global _classifier

    if (not _classifier_has_been_trained):
        classifier = NaiveBayesClassifier.train(_training_dataset)
        classifier_has_been_trained = True

####################### Analyze the Data ########################
