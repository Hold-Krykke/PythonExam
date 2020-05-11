from modules import Preprocessing

# scrape here
print('Scraping...')
tweet_data = [{}]  # do stuff
# open file for preprocessing
print('Preprocessing...')
# FILENAME = './'
# with open(FILENAME) as file_object:
#     tweet_data = file_object.read()

handled_tweets = Preprocessing.get_tweet_data(tweet_data)  # do stuff

# analysis here
print('Performing sentiment analysis...')
analyzed_tweets = *handled_tweets  # do stuff

# presentation here
print('Generating presentations...')
result = *analyzed_tweets  # do stuff

if __name__ == "__main__":
    pass
