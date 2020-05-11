from modules.Preprocessing import get_tweet_data
from modules.Sentiment_Analysis import train_model_if_necessary, analyze_many_tweets

# Train model
train_model_if_necessary()
# scrape here
print('Scraping...')
tweet_data = [{}]  # do stuff
# open file for preprocessing
print('Preprocessing...')
# FILENAME = './'
# with open(FILENAME) as file_object:
#     tweet_data = file_object.read()

handled_tweets = get_tweet_data(tweet_data)  # do stuff

# analysis here
print('Performing sentiment analysis...')
analyzed_tweets = *handled_tweets  # do stuff

# presentation here
print('Generating presentations...')
result = *analyzed_tweets  # do stuff

if __name__ == "__main__":
    train_model_if_necessary()
