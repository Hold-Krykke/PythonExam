import bs4
import requests as req

base_URL = "https://mobile.twitter.com/search?q=%23"
end_URL_part = "&s=typd&x=0&y=0"
example_URL_part = "trump&s=typd&x=0&y=0"

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
    tweet_strings = []
    for element in tweet_elements:
        tweet_strings.append(extract_inner_text(element))
    return tweet_strings

def extract_inner_text(tweet_element):
    """
    Extracts raw text from a tweet element.
    """
    tweet_fractions = tweet_element.find_all("div", class_=["dir-ltr"])
    tweet_text = ""
    for element in tweet_fractions:
        tweet_text += element.text
    # Change the encoding to something better if possible (find a better way to handle emojis)
    return tweet_text.encode("utf-8")

def get_next_page_link(soup: bs4.BeautifulSoup):
    """
    Used to get the link to the next twitter page with older tweets. Extracts the link from given soup (bs4).
    """
    more_element = soup.find("div", class_=["w-button-more"])
    a_tag = more_element.find("a")
    next_page_link = a_tag["href"]
    url_part = "https://mobile.twitter.com"
    return url_part + next_page_link

def get_tweets(hashtag: str, tweet_count: int):
    """
    This is the MOTHER FUNCTION of this module. Use this function to get tweets.\n
    Omit the # when providing the search parameter. If you want to search for "#trump", provide "trump".\n
    The amount of tweets searched for will always be at least 20 and will be floored to 20. Providing 39 will result in 20 tweets. Providing 41 will result in 40 tweets.
    Returns an array of string - each string containing a single tweet.
    This is the prototype function. It uses utf-8 encoding which is not very well suited for emojis. 
    The strings will contain a lot of confusing characters if the original tweet had emojis in it.
    """
    # Creating initial URL
    URL = base_URL + hashtag + end_URL_part
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
    
    return tweets

tweets = get_tweets("trump", 40)
print(tweets)
print("\n")
print(len(tweets))