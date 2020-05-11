#!flask/bin/python
from flask import Flask, jsonify, abort, request, send_file
import presentation
import web_scraper
import Preprocessing
import Sentiment_Analysis
import datetime

app = Flask(__name__)

@app.route('/api/hashtag/<string:hashtag>', methods=['GET'])
def get_obama(hashtag):

    if hashtag == "trump":
        do_everything(str(hashtag))
        return send_file("./plots/trump.png"), 200
    return jsonify({"message": "No content"}), 404

def do_everything(hashtag: str):
    # tweet_list a list of tweet objects (not a list of strings)
    tweet_list = web_scraper.get_tweets(20, False, hashtag)

    # tweet_data is a tuple with a list and 2 dicts: tweets: list[dict[str, str]], hashtag_stats: dict, mention_stats: dict
    tweet_data = Preprocessing.get_tweet_data(tweet_list) 

    # Train the model if necessary
    Sentiment_Analysis.train_model_if_necessary()

    # analyzed_tweet_data is a list of tweet dicts with the new data from the SA 
    analyzed_tweet_data = Sentiment_Analysis.analyze_many_tweets(tweet_data[0], 25, 75)

    # creating new tuple with the updated analyzed data and the stats from the previous tuple (tweet_data)
    # we have to update the data by creating a new tuple because tuples are immutable :)))
    analyzed_data = analyzed_tweet_data, tweet_data[1], tweet_data[2]
    
    # filtering data to get only data between the two specified dates
    filtered_data = presentation.get_tweets_in_daterange(analyzed_data[0], datetime.date(2020, 5, 10), datetime.date(2020, 5, 11))

    # Getting plot data from the get_sentiment function 
    PLOT_ME = presentation.get_sentiment(filtered_data)

    # Create plot and save so the endpoint can send the .png file
    presentation.bar_plot(PLOT_ME, hashtag, True)



if __name__ == '__main__':
    app.run(debug=True)

    