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

    if hashtag == "obama":
        return send_file("../data/Barack_Obama.png"), 200
    return jsonify({"message": "No content"}), 404

def do_everything(hashtag):
    tweet_list = web_scraper.get_tweets(20, False, hashtag)
    tweet_data = Preprocessing.get_tweet_data(tweet_list) 
    Sentiment_Analysis.train_model_if_necessary()
    analyzed_tweet_data = Sentiment_Analysis.analyze_many_tweets(tweet_data[0], 25, 75)
    analyzed_data = analyzed_tweet_data, tweet_data[1], tweet_data[2]
    filtered_data = presentation.get_tweets_in_daterange(analyzed_data, datetime.date(2020, 5, 10), datetime.date(2020, 5, 10))
    PLOT_ME = presentation.get_sentiment(filtered_data)
    presentation.bar_plot(PLOT_ME, "Trump Sentiment")


if __name__ == '__main__':
    do_everything("trump")
    app.run(debug=True)

    