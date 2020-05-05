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
import json


# Basic Preprocessing, will be replaced by Rúnis work - Tokenizing the Data
positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')
text = twitter_samples.strings('tweets.20150430-223406.json')

tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
print(tweet_tokens[0])

# Basic Preprocessing, will be replaced by Rúnis work - Normalizing the Data


def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence


# Basic Preprocessing, will be replaced by Rúnis work - Removing Noise from the Data
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


stop_words = stopwords.words('english')

positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

positive_cleaned_tokens_list = []
negative_cleaned_tokens_list = []

for tokens in positive_tweet_tokens:
    positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

for tokens in negative_tweet_tokens:
    negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))


# Basic Preprocessing, will be replaced by Rúnis work - Determining Word Density
def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


all_pos_words = get_all_words(positive_cleaned_tokens_list)
freq_dist_pos = FreqDist(all_pos_words)


# Preparing Data and Building and Testing the Model - should be redone once Rúnis part is done
def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)


positive_dataset = [(tweet_dict, "Positive")
                    for tweet_dict in positive_tokens_for_model]

negative_dataset = [(tweet_dict, "Negative")
                    for tweet_dict in negative_tokens_for_model]

dataset = positive_dataset + negative_dataset

random.shuffle(dataset)

train_data = dataset[:7000]
test_data = dataset[7000:]
print('TEST DATA SET', test_data[0])
# test_tweets

# print(train_data[0])
classifier = NaiveBayesClassifier.train(train_data)

# print("Accuracy is:", classify.accuracy(classifier, test_data))
# print(classifier.show_most_informative_features(10))

# Single Tweet test
#custom_tweet = "({'dont': True, 'come': True, 'italy': True, ':(': True}, 'Negative')"
custom_tweet = "this is not great custom tweet sad good person!! #tweet"
custom_tokens = remove_noise(word_tokenize(custom_tweet))
print(custom_tokens)
print(classifier.classify(dict([token, True] for token in custom_tokens)))
print("Accuracy is:", classify.accuracy(classifier, test_data))

# KEY = TOJSON(dict([token, True] for token in custom_tokens))
# VALUE = classifier.classify(dict([token, True] for token in custom_tokens))
#test_json = json.dumps(dict([token, True] for token in custom_tokens))
print("DICT ", dict([token, True] for token in custom_tokens))
#print("TEST JSON", test_json)
# print("json test af dict ", test_json)
comb = (dict([token, True] for token in custom_tokens), classifier.classify(
    dict([token, True] for token in custom_tokens)))
print(comb)
print(classifier.show_most_informative_features(100))
print("Accuracy is:", classify.accuracy(classifier, [comb]))

# print(classifier.prob_classify(dict([token, True] for token in custom_tokens)).max())


prob_dist = classifier.prob_classify(dict([token, True]
                                          for token in custom_tokens))
print(prob_dist.max())
print(round(prob_dist.prob("Positive"), 2))
print(round(prob_dist.prob("Negative"), 2))


# print(positive_cleaned_tokens_list[0])
# print(positive_cleaned_tokens_list[1])
# print(positive_cleaned_tokens_list[2])
# print(positive_cleaned_tokens_list[3])
# print(positive_cleaned_tokens_list[4])
# print(positive_cleaned_tokens_list[5])
# print(positive_cleaned_tokens_list[6])
# print(positive_cleaned_tokens_list[7])
# print(positive_cleaned_tokens_list[8])
# print(positive_cleaned_tokens_list[9])
