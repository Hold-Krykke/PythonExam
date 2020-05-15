import bs4
import requests as req
import os
from datetime import date, datetime
import emoji
import ast

_base_URL = "https://mobile.twitter.com/search?q="
_end_URL_part = "&s=typd&x=0&y=0"

def _get_soup(URL: str):
    """
    Downloads the html from given URL and returns the content as soup (bs4)
    """
    data = req.get(URL).content
    soup = bs4.BeautifulSoup(data, "html.parser")
    return soup


def _create_tweet_object(tweet_element, hashtags):
    # Create a tweet object and store the raw text and the hashtags searched for in it
    tweet_object = {}
    tweet_object["search_hashtags"] = hashtags
    tweet_object["raw_text"] = _extract_inner_text(tweet_element)
    # Creating tweet_urls property which is a list of strings
    tweet_urls = _extract_data_urls(tweet_element)
    tweet_object["tweet_urls"] = tweet_urls
    # Creating emojis property which is a list of strings
    tweet_emoji_descriptions = _emoji_description_extractor(tweet_object["raw_text"])
    tweet_object["emojis"] = tweet_emoji_descriptions
    # Creating the date property
    tweet_date = _get_tweet_date(tweet_element)
    tweet_object["date"] = tweet_date
    return tweet_object


def _create_tweet_objects(soup: bs4.BeautifulSoup, hashtags):
    """
    Extracts tweets from given soup and returns an array of strings, each string containing a tweet.
    """
    tweet_elements = soup.find_all("table", class_=["tweet"])
    tweets = []

    for element in tweet_elements:
        tweet_object = _create_tweet_object(element, hashtags)
        tweets.append(tweet_object)
    # Return result
    return tweets


def _extract_inner_text(tweet_element):
    """
    Extracts raw text from a tweet element.
    """
    # The content of the tweet is put into several divs so we find all those divs and extract their inner text
    tweet_fractions = tweet_element.find_all("div", class_=["dir-ltr"])
    tweet_text = ""
    for element in tweet_fractions:
        tweet_text += str(element.text)
    # Return raw text from tweet
    return tweet_text


def _extract_data_urls(tweet_element):
    """
    Extracts the data-url attributes from a tweet element.
    """
    # Getting all <a>-tags
    tweet_a_tags = tweet_element.find_all("a")
    data_urls = []
    for element in tweet_a_tags:
        try:
            # If the tag has an attribute "data-url" then we take the link from this URL
            # Only html tags that contain actual links like "www.checkoutthissite.com" will have the "data-url" attribute
            data_url = element["data-url"]
            data_urls.append(data_url)
        except:
            # Do nothing if we can't find a data-url. 
            pass
    # Return all found URLs as a list of strings
    return data_urls


def _get_tweet_date(tweet_element):
    """
    Returns a string with the date contained in the tweet.
    If the tweet is from before 2020 it will still be returned as if it was from 2020
    """
    # Finding element that contains the timestamp
    timestamp_element = tweet_element.find("td", class_=["timestamp"])
    # Inner element with timestamp or date
    timestamp_inner_element = timestamp_element.find("a")
    # The date is stored as inner text
    timestamp = timestamp_inner_element.text
    # If the timestamp contains "min" or "h"(hour) etc. it means the tweet is from today so we just return the date today
    if "min" in timestamp or timestamp[-1] == "m" or timestamp[-1] == "s" or "h" in timestamp or "now" in timestamp:
        return "{},{},{}".format(datetime.now().date().year, datetime.now().date().month, datetime.now().date().day)
    # Extract date to ensure proper formatting
    # None of the tweet dates contain a year so we add 2020 to the date to be able to create a proper date object using strptime()
    tweet_date = datetime.strptime(timestamp + " 2020", "%b %d %Y")
    # The weird looking return statement is made to make it easier for other parts of the program to read the date (2020,5,6)
    return "{},{},{}".format(tweet_date.date().year, tweet_date.date().month, tweet_date.date().day)


def _emoji_description_extractor(text: str):
    """
    Used to extract the decription of emojis used in the given text.
    """
    emoji_list = emoji.emoji_lis(text)
    emoji_descriptions = [str.strip(emoji.demojize(vars.get("emoji")).replace("_", " ").replace(":", "")) for vars in emoji_list]
    return emoji_descriptions


def _get_next_page_link(soup: bs4.BeautifulSoup):
    """
    Used to get the link to the next twitter page with older tweets. Extracts the link from given soup (bs4).
    """
    more_tweets_element = soup.find("div", class_=["w-button-more"])
    a_tag = more_tweets_element.find("a")
    next_page_link = a_tag["href"]
    # "https://mobile.twitter.com" is not part of the next-page link so we add it our selves
    url_part = "https://mobile.twitter.com"
    return url_part + next_page_link


def get_tweets(tweet_count: int, fresh_search: bool, hashtags: list):
    """
    #### Returns \n
    >>> List of strings. The contents of each string will be structured as a dictionary

    #### Parameters \n
    tweet_count: integer - The amount of tweets you want. Provide a number in an interval of 20.\n
    fresh_search: boolean - Pass True if you want newly downloadet tweets. When passing False the function will return tweets from a file if a file with matching content exists\n
    *hashtags: string - Pass as many strings as you want. Omit the # when passing this parameter.

    #### Description \n
    This is the MOTHER FUNCTION of this module. Use this function to get tweets.\n
    Omit the # when providing the search parameter. If you want to search for "#trump", provide "trump".\n
    The amount of tweets searched for will always be at least 20 and will be rounded down to the nearest number divisible by 20. 
    Providing 39 will result in 20 tweets. Providing 41 will result in 40 tweets.
    Returns an array of string - each string containing a single tweet.
    This function saves the tweets in the /tweets folder for faster searching if fresh_search == False 
    Provide multiple strings as parameters after the fresh_search parameter to search for tweets that contain multiple hashtags.
    Pass True as the fresh_search parameter if you want to make sure you get the newest results from Twitter.
    """
    # Creating initial URL
    URL = _base_URL
    # Name of the file the tweets will be saved in
    file_name = ""
    # This list is used to add the hashtags searched for to the tweet objects
    hashtag_list = []
    # Creating file name and updating initial URL 
    for index, hashtag in enumerate(hashtags):
        # %23 is URL language for #. Adding + between each search parameter because whitespace is converted to + in the URL
        URL += ("%23" + hashtag + "+")
        hashtag_list.append("#" + hashtag)
        # If we've reached the last search parameter we end the file name with the last search parameter (the last hashtag)
        if ((len(hashtags) - index) == 1):
            file_name += hashtag
        # If there is more than one search parameter left we add both the current search parameter and an underscore to the file name
        else:
            file_name += (hashtag + "_")
    # Adding the end-part of the URL to URL after all search parameters have been added
    URL += _end_URL_part

    # If we don't want to do a fresh search and if the file corresponding to the hashtag(s) exists then return the file content
    if not (fresh_search):
        if os.path.isfile("./tweets/" + file_name):
            with open("./tweets/" + file_name, 'r', encoding="utf-8") as f:
                # The first line in each save file will contain a number which is the amount of tweets in the file
                # If the user requests more tweets than what has previously been saved in the file then we have to do a fresh search
                amount_of_tweets_in_file = int(f.readline())
                if amount_of_tweets_in_file >= tweet_count:  
                    result = []
                    count = 0
                    for line in f.readlines():
                        if count > tweet_count - 1:
                            break
                        result.append(ast.literal_eval(line))
                        count += 1
                    return result


    # Result array with all the tweets
    tweets = []

    # Calculating the amount of Twitter pages to go through
    # Minimum of tweets = 20
    temp_count = 20
    # Checking if the user provided a number larger than 20. If they did - update the counter
    if not (tweet_count < 20):
        temp_count = tweet_count
    # Creating the number used to choose how many Twitters we need to scrape data from
    # There are 20 tweets pr page that's why we divide the number of tweets by 20
    loop_count = int(temp_count / 20)

    soups = []
    for i in range(loop_count):
        # Getting soup from the Twitter page
        soup = _get_soup(URL)
        soups.append(soup)
        # Updating the URL to the next-page URL of the current page
        try:
            URL = _get_next_page_link(soup)
        except:
            print("No more tweets available")
            print("Tried to find {} tweets".format(str( tweet_count )))
            print("Number of tweets found: ~{}".format(str( len(soups) * 20 )))
            break

    # Going through twitter pages and collecting tweets
    for soup in soups:
        # extractions will be an array of "tweet objects" that contain the raw tweet, an array of URLs, and more
        extractions = _create_tweet_objects(soup, hashtag_list)
        # Adding each tweet object to the result array (tweets)
        for element in extractions:
            tweets.append(element)
    
    # Saving tweets in file
    with open("./tweets/" + file_name, 'w', encoding="utf-8") as f:
        f.write(str(loop_count*20) + "\n")
        for index, element in enumerate(tweets):
            f.write(str(element))
            # Adding newline so it's easier to read one tweet at a time later on by using .readlines()
            f.write("\n")
    return tweets


# Usage example: 20: number of tweets, False: fresh search?, anything after this == search parameters (hashtags)
# tweets = get_tweets(100, True, ["trump", "biden"])
# print("Tweets downloaded")

