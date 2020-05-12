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
from modules.Preprocessing import remove_noise

"""
These are the only methods that should be called from other modules:
    train_model_if_necessary()
    analyze_many_tweets(scraped_tweets, 0.25, 0.75)
"""


####################### Prepare the Data ########################
def _prepare_training_data_for_model():
    """
    This function gathers the training data sets from nltk corpus twitter_samples, calls the preprocessing functions and then
    marks the datasets with "Positive" or "Negative", before finally merging and returning them as one dataset. 
    This is the data used to train our model. 
    _______________
    >>> return train_data, test_data
    """
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')

    positive_preprocessed_tokens = []
    negative_preprocessed_tokens = []

    for tweet in positive_tweets:
        positive_preprocessed_tokens.append(remove_noise(tweet))

    for tweet in negative_tweets:
        negative_preprocessed_tokens.append(remove_noise(tweet))

    positive_formatted_tokens = _get_tweets_for_model(positive_preprocessed_tokens)
    negative_formatted_tokens = _get_tweets_for_model(negative_preprocessed_tokens)

    positive_dataset = [(tweet_dict, "Positive") for tweet_dict in positive_formatted_tokens]
    negative_dataset = [(tweet_dict, "Negative") for tweet_dict in negative_formatted_tokens]

    dataset = positive_dataset + negative_dataset
    random.shuffle(dataset)
    train_data = dataset[:8000]
    test_data = dataset[8000:]

    return train_data, test_data


def _get_tweets_for_model(preprocessed_token_list):
    """
    Util function that yields one token at a time in this form, which is required by the model. 
    _______________
    >>> yield tweet object
    e.g. ({'top': True, 'engage': True, 'member': True, 'community': True, 'week': True}, 'Positive')
    """
    for tweet_tokens in preprocessed_token_list:
        yield dict([token, True] for token in tweet_tokens)
####################### Prepare the Data ########################


####################### Analyze the Data ########################
def analyze_many_tweets(tweets_list, uncertain_low=0.25, uncertain_high=0.75):
    """
    Takes in a list of scraped tweets and calls the analyzer for each, before appending the analyzed 
    result to the tweet and returning the list
    _______________
    >>> return tweets_list
    """
    for item in tweets_list:
        tweet = item.get("tweet")
        result = _analyze_tweet(tweet, uncertain_low, uncertain_high)
        item["sentiment_analysis"] = result
    return tweets_list


def _analyze_tweet(tweet, uncertain_low: float, uncertain_high: float):
    """
    This function is the analyzer. It trains the model if not already trained (should only happen once per run),
    classifies the tweet and appends the results to the result-object, which is then returned.
    _______________
    >>> return result
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
    This function checks if the model has been trained, and trains the model if it hasn't been trained. After this, the model is 
    testet with the testing data, and the accuracy is returned. 
    It should be called from the Main.py on program start, as the training is time-consuming. This should only
    occur once per run. 
    _______________
    >>> return _accuracy
    """
    global _classifier_has_been_trained
    global _classifier
    training_dataset, testing_dataset = _prepare_training_data_for_model()

    if (not _classifier_has_been_trained):
        print("Training Classifier...")
        classifier = NaiveBayesClassifier.train(training_dataset)
        print("Testing Classifier...")
        accuracy = classify.accuracy(classifier, testing_dataset)
        classifier_has_been_trained = True
        print("Accuracy is:", accuracy)
    return accuracy
####################### Analyze the Data ########################


######################## Global variables ########################
_classifier_has_been_trained = False
_classifier = None
######################## Global variables ########################
