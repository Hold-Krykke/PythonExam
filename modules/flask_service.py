#!flask/bin/python
from flask import Flask, jsonify, abort, request, send_file
import presentation
import web_scraper
import Preprocessing
import Sentiment_Analysis
from datetime import datetime, date 

app = Flask(__name__)

@app.route('/api/hashtag/<string:hashtag>', methods=['POST'])
def get_test(hashtag):
    print(hashtag)
    # if hashtag == "trump":
    #     do_everything(str(hashtag))
    #     return send_file("./plots/trump.png"), 200
    return jsonify({"message": "No content"}), 404

@app.route('/api/sentiment', methods=['POST'])
def get_burglaries():
    # Check there is a body in request
    if not request.json:
        abort(400, 'Please provide search data. Example: {"hashtags": ["trump","biden"],"start_date": "2020-5-10","end_date": "2020-5-11"}')
    

    # Check if there is a hashtag list in the JSON
    if not 'hashtags' in request.json:
        abort(400, 'Please provide search hashtags: {"hashtags": ["trump", "biden"]}')
    hashtags = request.json['hashtags']


    file_name = ""
    for index, hashtag in enumerate(hashtags):
        # If we've reached the last search parameter we end the file name with the last search parameter (the last hashtag)
        if ((len(hashtags) - index) == 1):
            file_name += hashtag
        # If there is more than one search parameter left we add both the current search parameter and an underscore to the file name
        else:
            file_name += (hashtag + "_")

    # Check type of plot
    if not 'plot_type' in request.json:
        abort(400, "Please provide plot type")
    plot_type = request.json['plot_type']

    if not any(p_type in plot_type for p_type in ['bar', 'line', 'pie']):
        abort(400, "Please provide plot type, must be either bar, line or pie")

    
    # Check if start date has been provided
    if not 'start_date' in request.json:
        abort(400, "Please provide start date")
    start_date_string = request.json['start_date']
    start_date = datetime.strptime(start_date_string, '%Y-%m-%d').date()

    # Check if end date has been provided
    if not 'end_date' in request.json:
        abort(400, "Please provide end date")
    end_date_string = request.json['end_date']
    end_date = datetime.strptime(end_date_string, '%Y-%m-%d').date()

    # Creating plot
    do_everything(hashtags, file_name, start_date, end_date, plot_type)

    return send_file("./plots/" + file_name + ".png"), 200

def do_everything(hashtags: list, file_name, start_date, end_date, plot_type):
    # tweet_list a list of tweet objects (not a list of strings)
    tweet_list = web_scraper.get_tweets(500, False, hashtags)

    # tweet_data is a tuple with a list and 2 dicts: tweets: list[dict[str, str]], hashtag_stats: dict, mention_stats: dict
    tweet_data = Preprocessing.get_tweet_data(tweet_list) 

    # Train the model if necessary
    Sentiment_Analysis.train_model_if_necessary()

    # analyzed_tweet_data is a list of tweet dicts with the new data from the SA 
    analyzed_tweet_data = Sentiment_Analysis.analyze_many_tweets(tweet_data[0], 0.25, 0.75)

    # creating new tuple with the updated analyzed data and the stats from the previous tuple (tweet_data)
    # we have to update the data by creating a new tuple because tuples are immutable :)))
    analyzed_data = analyzed_tweet_data, tweet_data[1], tweet_data[2]
    
    # filtering data to get only data between the two specified dates
    filtered_data = presentation.get_tweets_in_daterange(analyzed_data[0], start_date, end_date)

    # Getting plot data from the get_sentiment function 
    PLOT_ME = presentation.get_sentiment(filtered_data)

    # Create plot and save so the endpoint can send the .png file
    if plot_type == "bar":
        presentation.bar_plot(PLOT_ME, file_name, file_name)
    if plot_type == "line":
        presentation.line_plot(PLOT_ME, file_name, file_name)
    if plot_type == "pie":
        presentation.pie_chart(PLOT_ME, file_name, file_name)



if __name__ == '__main__':
    Sentiment_Analysis.train_model_if_necessary()
    app.run(debug=True)

    