#!flask/bin/python
from flask import Flask, jsonify, abort, request, send_file
import presentation
import web_scraper
import Preprocessing
import Sentiment_Analysis
from datetime import datetime, date 

app = Flask(__name__)

@app.route('/api/sentiment', methods=['POST'])
def get_burglaries():
    # Check there is a body in request
    if not request.json:
        abort(400, 'Please provide search data. Example: {"hashtags": ["trump","biden"],"start_date": "2020-5-3","end_date": "2020-5-12","plot_type": "line","remove_sentiment": "uncertain"}')
    

    # Check if user wants a specific amount of tweets scraped
    tweet_amount = 300
    if 'tweet_amount' in request.json:
        tweet_amount = int(request.json['tweet_amount'])
    
    # Check if user wants a fresh search
    fresh_search = False
    if 'fresh_search' in request.json:
        fresh_search = request.json['fresh_search']
    
    # Check if there is a hashtag list in the JSON
    if not 'hashtags' in request.json:
        abort(400, 'Please provide search hashtags: {"hashtags": ["trump", "biden"]}')
    hashtags = request.json['hashtags']

    if 'get_stats' in request.json:
        get_stats = request.json['get_stats']
        stats = prepare_data_and_create_stats(hashtags, tweet_amount, fresh_search, str.lower(get_stats))
        return jsonify(stats), 200

    search_for = {}
    if 'search_for' in request.json:
        search_for = request.json['search_for']

    file_name = ""
    for index, hashtag in enumerate(hashtags):
        # If we've reached the last search parameter we end the file name with the last search parameter (the last hashtag)
        if ((len(hashtags) - index) == 1):
            file_name += hashtag
        # If there is more than one search parameter left we add both the current search parameter and an underscore to the file name
        else:
            file_name += (hashtag + "_")

    if(list(search_for.keys())):
        file_name = list(search_for.values())[0]

    rm_sentiment = ""
    if 'remove_sentiment' in request.json:
        rm_sentiment = request.json['remove_sentiment']

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
    prepare_data_and_create_plot(hashtags, tweet_amount, fresh_search, file_name, start_date, end_date, plot_type, search_for, rm_sentiment)

    return send_file("./plots/" + file_name + ".png"), 200

def prepare_data_and_create_stats(hashtags: list, tweet_amount: int, fresh_search: bool, stat_type: str):
    # tweet_list a list of tweet objects (not a list of strings)
    tweet_list = web_scraper.get_tweets(tweet_amount, fresh_search, hashtags)
    print("Done scraping...")

    # tweet_data is a tuple with a list and 2 dicts: tweets: list[dict[str, str]], hashtag_stats: dict, mention_stats: dict
    tweets, hashtag_stats, mention_stats = Preprocessing.get_tweet_data(tweet_list) 
    print("Done preprocessing...")
    print("Statistics created...")
    if stat_type == "mentions":
        return mention_stats
    elif stat_type == "hashtags":
        return hashtag_stats
    else:
        return {"Message": "No statistics available. Options: mentions, hashtags"}

def prepare_data_and_create_plot(hashtags: list, tweet_amount: int, fresh_search: bool, file_name, start_date, end_date, plot_type, search_for: dict, remove_sentiment: str):
    # tweet_list a list of tweet objects (not a list of strings)
    tweet_list = web_scraper.get_tweets(tweet_amount, fresh_search, hashtags)
    print("Done scraping...")

    # tweet_data is a tuple with a list and 2 dicts: tweets: list[dict[str, str]], hashtag_stats: dict, mention_stats: dict
    tweets, hashtag_stats, mention_stats = Preprocessing.get_tweet_data(tweet_list) 
    print("Done preprocessing...")
    
    # analyzed_tweet_data is a list of tweet dicts with the new data from the SA 
    analyzed_tweet_data = Sentiment_Analysis.analyze_many_tweets(tweets)
    print("Done analyzing...")

    # filtering data to get only data between the two specified dates
    filtered_data = presentation.get_tweets_in_daterange(analyzed_tweet_data, start_date, end_date)
    print("Done filtering on date...")

    # filter for specific hashtag, mention or url
    if (list(search_for.keys())):
        filtered_data = presentation.get_by_key_value(filtered_data, list(search_for.keys())[0], list(search_for.values())[0])
        print("Done filtering for hashtag, mention or url...")

    # filter sentiment if possible
    if (remove_sentiment):
        filtered_data = presentation.remove_sentiment(filtered_data, remove_sentiment)
        print("Done removing sentiment...")
    
    # Getting plot data from the get_sentiment function 
    PLOT_ME = presentation.get_sentiment(filtered_data)
    print("Done getting sentiment df for plotting...")

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

    