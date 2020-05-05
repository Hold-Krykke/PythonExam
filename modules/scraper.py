import bs4
import requests as req
import os
import re
import pandas as pd

base_URL = "https://mobile.twitter.com/search?q="
end_URL_part = "&s=typd&x=0&y=0"

def get_soup(URL: str):
    """
    Downloads the html from given URL and returns the content as soup (bs4)
    """
    data = req.get(URL).content
    soup = bs4.BeautifulSoup(data, "html.parser")
    return soup


def extract_tweets(soup: bs4.BeautifulSoup):
    """
    Extracts tweets from given soup and returns an array of strings, each string containing a tweet.
    Each string will contain a lot of newlines right next to characters like this:\n 
    "(...) end of sentence.[newline]Beginning of new sentence (...)"
    """
    tweet_elements = soup.find_all("table", class_=["tweet"])
    tweets = []
    for element in tweet_elements:
        tweet_object = extract_inner_text(element)
        tweet_urls = extract_data_urls(element)
        tweet_object["tweet_urls"] = tweet_urls
        tweet_emoji_descriptions = emoji_description_extractor(tweet_object["raw_text"])
        tweet_object["emojis"] = tweet_emoji_descriptions
        tweets.append(tweet_object)
    return tweets


def extract_inner_text(tweet_element):
    """
    Extracts raw text from a tweet element.
    """
    tweet_fractions = tweet_element.find_all("div", class_=["dir-ltr"])
    tweet_text = ""
    for element in tweet_fractions:
        tweet_text += str(element.text)
    return {"raw_text": tweet_text}


def extract_data_urls(tweet_element):
    """
    Extracts the data-url attributes from a tweet element.
    """
    tweet_a_tags = tweet_element.find_all("a")
    data_urls = []
    for element in tweet_a_tags:
        try:
            data_url = element["data-url"]
            data_urls.append(data_url)
        except:
            pass
    return data_urls


def emoji_description_extractor(text: str):
    """
    Used to extract the decription of emojis used in the given text.
    This function only supports 842 emojis. Some descriptions may be empty if the used emoji is rare or whatever
    """
    # Source of regex: https://gist.github.com/Alex-Just/e86110836f3f93fe7932290526529cd1
    emoji = re.compile(
    "(["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "])"
    )
    # Finding all emojis in text
    matcher_object = emoji.findall(text)

    # Loading list of emojis and their descriptions
    emoji_matrix_df = pd.read_excel("../resources/emoji_unicode.xlsx")

    # Getting the two columns we need from the original dataframe
    utf8 = emoji_matrix_df["UTF8"]
    desc = emoji_matrix_df["Description"]
    # Combining the columns
    emoji_df = pd.concat([utf8, desc], axis=1, keys=['UTF8', 'Description'])

    # Make all the utf-8 codes uppercase. This is needed when we compare utf-8 codes later on
    emoji_df["UTF8"] = emoji_df["UTF8"].apply(lambda x: x.upper())

    # Initializing the result list
    emoji_descriptions = []

    # Function creating a mask matching a given emoji
    def get_emoji_mask(emoji):
        emoji_mask = (emoji_df["UTF8"] == str(emoji.encode())[2:-1].upper())
        return emoji_mask

    # Running through all found emojis and adding their desciptions to the result list
    for element in matcher_object:
        # Getting the index of the current emoji (the index representing the emojis position in the dataframe)
        index_of_smiley = emoji_df[get_emoji_mask(element)].index.values
        emoji_description = ""
        try:
            # Trying to get the description
            emoji_description = emoji_df["Description"][index_of_smiley].values[0]
        except:
            # If we can't extract description just let the description stay empty
            pass
        # Adding description of emoji to the result list
        emoji_descriptions.append(emoji_description)
    # Returning all descriptions 
    return emoji_descriptions


def get_next_page_link(soup: bs4.BeautifulSoup):
    """
    Used to get the link to the next twitter page with older tweets. Extracts the link from given soup (bs4).
    """
    more_element = soup.find("div", class_=["w-button-more"])
    a_tag = more_element.find("a")
    next_page_link = a_tag["href"]
    url_part = "https://mobile.twitter.com"
    return url_part + next_page_link


def get_tweets(tweet_count: int, fresh_search: bool, *hashtags: str):
    """
    This is the MOTHER FUNCTION of this module. Use this function to get tweets.\n
    Omit the # when providing the search parameter. If you want to search for "#trump", provide "trump".\n
    The amount of tweets searched for will always be at least 20 and will be rounded down to the nearest number that can be divided by 20. 
    Providing 39 will result in 20 tweets. Providing 41 will result in 40 tweets.
    Returns an array of string - each string containing a single tweet.
    This function saves the tweets using utf-8 encoding which is not very well suited for emojis. 
    Provide multiple strings as parameters after the tweet_count parameter to search for tweets that contain multiple hashtags.
    Pass True as the fresh_search parameter if you want to make sure you get the newest results from Twitter.
    """
    # Creating initial URL
    URL = base_URL
    file_name = ""
    for index, hashtag in enumerate(hashtags):
        URL += ("%23" + hashtag + "+")
        if ((len(hashtags) - index) == 1):
            file_name += hashtag
        else:
            file_name += (hashtag + "_")
    URL += end_URL_part

    # If we don't want to do a fresh search and if the file corresponding to the hashtag(s) exists then return the file content
    if not (fresh_search):
        if os.path.isfile("../tweets/" + file_name):
            with open("../tweets/" + file_name, 'r', encoding="utf-8") as f:
                return f.read()


    # Result array with all the tweets
    tweets = []

    # Calculating the amount of Twitter pages to go through
    temp_count = 20
    if not (tweet_count < 20):
        temp_count = tweet_count
    loop_count = int(temp_count / 20)

    # Going through twitter pages and collecting tweets
    for i in range(loop_count):
        soup = get_soup(URL)
        extractions = extract_tweets(soup)
        for element in extractions:
            tweets.append(element)
        URL = get_next_page_link(soup)
    
    # Saving tweets in file
    with open("../tweets/" + file_name, 'w', encoding="utf-8") as f:
        for element in tweets:
            f.write(str(element))
            # Adding newline so it's easier to read one tweet at a time later on by using .readlines()
            f.write("\n")
    
    return tweets

# Usage example: 20: number of tweets, False: fresh search?, anything after this == search parameters (hashtags)
# tweets = get_tweets(20, True, "trump", "biden")
# print("Tweets downloaded")
# for tweet in tweets:
#     print("\n")
#     print(str(tweet))
#     print("\n")
    
# print(tweets)
# print("\n")
# print(len(tweets))

# for tweet in tweets:
#     desciptions = emoji_description_extractor(tweet)
#     print(desciptions)
