from modules import Preprocessing

# scrape here
print('Scraping...')

# open file for preprocessing
print('Preprocessing...')
FILENAME = './'
with open(FILENAME) as file_object:
    tweet_data = file_object.read()

tweets = Preprocessing.get_tweet_data(tweet_data)

# analysis here
print('Performing sentiment analysis...')

# presentation here
print('Generating presentations...')


if __name__ == "__main__":
    pass
