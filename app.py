from modules import Preprocessing

# scrape here

# open file for preprocessing
FILENAME = './'
with open(FILENAME) as file_object:
    tweet_data = file_object.read()

tweets = Preprocessing.get_tweet_data(tweet_data)

# analysis here

# presentation here


if __name__ == "__main__":
    pass
