from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
import re
import string
from nltk.corpus import stopwords
from nltk import FreqDist
# All above i think is just for the dummy preprocessing
import random
from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from ala_Runi_tweets import test_tweets


################### Preprocessing util methods ##################
def remove_noise(tweet_tokens, stop_words=()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)
################### Preprocessing util methods ##################


################### Test Tweets for building ####################
positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')
text = twitter_samples.strings('tweets.20150430-223406.json')
################### Test Tweets for building ####################


####################### Prepare the Data ########################
def prepare_tweet_data_for_model():
    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    # print("Freq")
    # print(freq_dist_pos.most_common(20))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset
    random.shuffle(dataset)
    # train_data = dataset[:7000]
    # test_data = dataset[7000:]

    return dataset
####################### Prepare the Data ########################


####################### Analyze the Data ########################
def analyze_many_tweets(classifier, tweets_list):

    for item in tweets_list:
        tweet = item.get("tweet")
        result = analyze_tweet(tweet, classifier)
        item["sentiment_analysis"] = [result]

    return tweets_list


def analyze_tweet(tweet, classifier):
    tweet_tokens = remove_noise(word_tokenize(tweet))

    # Check format
    comb = (dict([token, True] for token in tweet_tokens), classifier.classify(dict([token, True] for token in tweet_tokens)))
    # print("COMB", comb)

    probability_distrubution = classifier.prob_classify(dict([token, True] for token in tweet_tokens))

    result = {}
    result["verdict"] = probability_distrubution.max()
    result["positive_procent"] = round(probability_distrubution.prob("Positive"), 2)
    result["negative_procent"] = round(probability_distrubution.prob("Negative"), 2)
    return result


train_data = prepare_tweet_data_for_model()
classifier = NaiveBayesClassifier.train(train_data)
print(analyze_many_tweets(classifier, test_tweets))
####################### Analyze the Data ########################
