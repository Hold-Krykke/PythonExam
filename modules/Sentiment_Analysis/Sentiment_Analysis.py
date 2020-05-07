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


###### Preprocessing util methods will be replaced by Rúni ######
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
        print(dict([token, True] for token in tweet_tokens))
        yield dict([token, True] for token in tweet_tokens)
###### Preprocessing util methods will be replaced by Rúni ######


####################### Prepare the Data ########################
def prepare_training_data_for_model():
    stop_words = stopwords.words('english')

    positive_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tokens = twitter_samples.tokenized('negative_tweets.json')
    print()
    print("raw tokens")
    print(positive_tokens[0])
    print()
    print(positive_tokens[1])
    print()
    print(positive_tokens[2])
    print()
    print()

    positive_preprocessed_tokens = []
    negative_preprocessed_tokens = []

    for tokens in positive_tokens:
        positive_preprocessed_tokens.append(remove_noise(tokens, stop_words))

    for tokens in negative_tokens:
        negative_preprocessed_tokens.append(remove_noise(tokens, stop_words))

    print()
    print("preprocessed tokens")
    print(positive_preprocessed_tokens[0])
    print()
    print(positive_preprocessed_tokens[1])
    print()
    print(positive_preprocessed_tokens[2])
    print()
    print()

    positive_formatted_tokens = get_tweets_for_model(positive_preprocessed_tokens)
    negative_formatted_tokens = get_tweets_for_model(negative_preprocessed_tokens)

    print()
    print("formatted tokens")
    print(positive_formatted_tokens)
    print()
    print()

    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_formatted_tokens]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_formatted_tokens]

    dataset = positive_dataset + negative_dataset
    # random.shuffle(dataset)
    # train_data = dataset[:7000]
    # test_data = dataset[7000:]

    return dataset
####################### Prepare the Data ########################


####################### Analyze the Data ########################

training_dataset = prepare_training_data_for_model()
classifier_has_been_trained = False
classifier = None


def analyze_many_tweets(tweets_list):

    for item in tweets_list:
        tweet = item.get("tweet")
        result = analyze_tweet(tweet)
        item["sentiment_analysis"] = [result]

    return tweets_list


def analyze_tweet(tweet):
    train_model_if_necessary()
    tweet_tokens = remove_noise(word_tokenize(tweet))
    # Check format
    # comb = (dict([token, True] for token in tweet_tokens), classifier.classify(dict([token, True] for token in tweet_tokens)))
    # print("COMB", comb)

    probability_distrubution = classifier.prob_classify(dict([token, True] for token in tweet_tokens))

    result = {}
    result["verdict"] = probability_distrubution.max()
    result["positive_procent"] = round(probability_distrubution.prob("Positive"), 2)
    result["negative_procent"] = round(probability_distrubution.prob("Negative"), 2)
    if (result.get("positive_procent") < 0.75 and result.get("positive_procent") > 0.25):
        result["verdict"] = "Uncertain"

    print(result)
    print()
    return result


def train_model_if_necessary():
    global classifier_has_been_trained
    global classifier

    if (not classifier_has_been_trained):
        classifier = NaiveBayesClassifier.train(training_dataset)
        classifier_has_been_trained = True


print(analyze_many_tweets(test_tweets))
####################### Analyze the Data ########################
