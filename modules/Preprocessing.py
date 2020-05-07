import re
import string
from typing import List, Dict
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

# lazy load stopwords
_stop_words = stopwords.words('english')
_stop_words.append('twitter')

scraped_tweets = [
    {'raw_text': '  Tomorrow I’ll be joined by @SebGorka, @STEPHMHAMILL and other distinguished guests to discuss the 2020 Presidential Election. \n\nTune into WJLA 24/7 tomorrow from 10:30-11:30 AM EST for another edition of The Armstrong Williams Show. #AWS #Election2020 #Trump #Biden @ABC7News pic.twitter.com/TTldPAD5RL\n',
        'tweet_urls': ['https://twitter.com/Arightside/status/1256364526741729288/video/1'], 'emojis': []},
    {'raw_text': '  The Narc In Chief is eyeing the November Election\n\nCue the nonstop lying and gaslighting through tweets, positive spin TV and his parade of sycophants\n\n@realDonaldTrump is a proven Liar and Divider, and is profoundly Unfit to serve as #POTUS\n#Trump #GoJoe #Biden #TrumpIsAnIdiot pic.twitter.com/4IimlZfhgi\n',
        'tweet_urls': ['https://twitter.com/rightNtruthMat/status/1257303553380679680/photo/1'], 'emojis': []},
    {'raw_text': '  The #TRUMP FAMILY HISTORY is a history of COWARDS & GRIFTERS.\n\nLazy, spoiled voters sat on their asses Nov 2016 and now he is making life decisions for the country!\n\nWrite your wills ASAP!\n\nSTAY HOME AS MUCH AS YOU CAN SO THAT YOU CAN VOTE FOR #BIDEN IN NOV.\n', 'tweet_urls': [], 'emojis': []},
    {'raw_text': ' #Europe And #USA democrats must stop supporting ISIS ayatollahs ...\nPlease stop supporting islamic republic of #iran !\n\n#Trump\n#Biden\n#MAGA\n#GOP\n#EuPULLtheTrigger\n@realDonaldTrump\n@SecPompeo\n@statedeptspox pic.twitter.com/JgZOu1ETXA\n',
        'tweet_urls': ['https://twitter.com/thedarkknight_q/status/1257250731851239424/photo/1'], 'emojis': []},
    {'raw_text': '  Low IQ #Trump supporters want to believe ONE #Biden accuser who’s changed her story, but NOT 33 women who have accused @realDonaldTrump and have NOT. pic.twitter.com/dL5nykBbtO\n',
        'tweet_urls': ['https://twitter.com/DavidB86318017/status/1257661383585472513/photo/1'], 'emojis': []},
    {'raw_text': '  Donald Trump is a Liar and Divider\n\nThe Narc in Chief sows chaos and division while millions of US citizens struggle during this pandemic\n\n@realDonaldTrump is a Menace to America and the #GOP is complicit. Trump must go.\n\n#Trump #Biden #Biden2020\n#TrumpIsAnIdiot pic.twitter.com/HfQeVEr9UI\n',
        'tweet_urls': ['https://twitter.com/rightNtruthMat/status/1257661943814541313/photo/1'], 'emojis': []},
    {'raw_text': '  🚨🚨Good evening resisters!! 🌊🌊\n\nLooking for more mutuals!! \n\n🚨👉Follow/follow back party for the resistance!! 👈🚨\n\n🎉 🎊 🎉🤣🎉🎊\n\nLess than six months until Nov 3, lets do this! \n\n#Resist #Resistance #Trump #VoteBlueNoMatterWho #VoteBlue2020 #Biden\npic.twitter.com/HAyksU6LDk\n', 'tweet_urls': ['https://twitter.com/LopezLovinLife/status/1257459922951983104/video/1'], 'emojis': [
        'POLICE CARS REVOLVING LIGHT', 'POLICE CARS REVOLVING LIGHT', 'WATER WAVE', 'WATER WAVE', 'POLICE CARS REVOLVING LIGHT', 'WHITE RIGHT POINTING BACKHAND INDEX', 'WHITE LEFT POINTING BACKHAND INDEX', 'POLICE CARS REVOLVING LIGHT', 'PARTY POPPER', 'CONFETTI BALL', 'PARTY POPPER', '', 'PARTY POPPER', 'CONFETTI BALL']},
    {'raw_text': '  Watch the video version of the new episode of the History, Law & Justice podcast, "Would a Biden-Obama, Biden-Clinton or Trump-Bush Ticket Be Constitutional?": youtu.be/dZTjiT_pl90 via @YouTube\n\nBelow is the episode preview.\n\n#constitution #biden #trump #clinton #obama #bush pic.twitter.com/wDrTqZcrr9\n',
        'tweet_urls': ['https://youtu.be/dZTjiT_pl90', 'https://twitter.com/mbucknerlaw/status/1257672120995323907/video/1'], 'emojis': []},
    {'raw_text': '  I don’t care if your name is #Trump, #Kavanaugh or #Biden. The unequivocal answer should be: \n\n“I have never sexually harassed or assaulted ANY woman, ever, and I fully support the review and release of ANY/ALL documents related to this allegation.”\n', 'tweet_urls': [], 'emojis': []},
    {'raw_text': '  This thread should be required reading for every American. \n\nSo give it a moment and You’ll get that “Aha!” moment of understanding like it did me.\n\n#trump #Biden #RepublicansAgainstTrump #Democrats #OpenTheEconomy #MAGA #TrumpVirus twitter.com/radiofreetom/s…\n',
        'tweet_urls': ['https://twitter.com/radiofreetom/status/1257068084856328193'], 'emojis': []},
    {'raw_text': '  Trump’s MENTAL HEALTH needs to be THE national topic of discussion\n\nHe continually exhibits shocking behavior. We can’t be desensitized. #GOP must act\n\nTrump is profoundly Unfit to be the #POTUS\n#Trump #GoJoe #Biden #TrumpIsAnIdiot #Biden2020 pic.twitter.com/xkC1jbiOsR\n',
        'tweet_urls': ['https://twitter.com/rightNtruthMat/status/1257088708513353735/photo/1'], 'emojis': []},
    {'raw_text': '  It’s amazing scrolling news sites and seeing so much on this Biden/Reade story. Was even half this much attention paid to the 26 women who’ve accused #Trump of similar acts?\n\nIs it so one-sided because #Biden spoke out? Whereas Trump simply ignores, denies and deflects. pic.twitter.com/FiZyshFFVi\n',
        'tweet_urls': ['https://twitter.com/rhholt/status/1256677842315853826/photo/1'], 'emojis': []},
    {'raw_text': "  Why is #Trump a bad leader?\n\nWhy is #Biden a better leader? \n\nWhy didn't you credit #Trump for the good work (if any)\n\nWhy didn't they work together? Power? Parties? Mindset?\n", 'tweet_urls': [
    ], 'emojis': []},
    {'raw_text': '  Give #Trump a second term and the US will have the bigliest most beautiful and perfectest deficits ever known to man.\n\nGive #Biden a first term and you will have the same outcome, with the only difference that Joe will have forgotten it before he could brag about it on Twitter.\n', 'tweet_urls': [], 'emojis': []},
    {'raw_text': '  Hey @realDonaldTrump: so you got the awful news today that your polling is DREADFUL and you’re LOSING BIGLY to #Biden. Getting mad at #Parscale won’t change that. But there IS a way out... link.medium.com/bX2vYU4L55 #Trump\n',
        'tweet_urls': ['https://link.medium.com/bX2vYU4L55'], 'emojis': []},
    {'raw_text': "  I think there is another state in the world called the USA and its president is Trump. Fortunately, it's not the country where I live. I am very lucky.\n\n@realDonaldTrump #trump #Biden\n", 'tweet_urls': [], 'emojis': []},
    {'raw_text': '  Republicans (@realDonaldTrump) vs Democrats (Biden) be like #Election2020 #Trump #Biden pic.twitter.com/dIvIx2qajc\n',
     'tweet_urls': ['https://twitter.com/cryptoredpin/status/1257366131825938439/video/1'], 'emojis': []},
    {'raw_text': ' #American #Democrats are trying to pin sexual assault allegations on Joe #Biden in order to lure in republican voters.\n😎 🤭\n\n#JoeBiden #AmericaFirst #TrumpIsALaughingStock #TrumpIsAnIdiot #Trump #Election2020 #MAGA\n',
        'tweet_urls': [], 'emojis': ['SMILING FACE WITH SUNGLASSES', '']},
    {'raw_text': '  The #Biden campaign’s neglect of #digital during the primary has led to an enormous shortfall against #Trump. \nBiden’s digital audience — including followers, subscribers and likes — is skimpy.\n\n#SocialMedia #DigitalMarketing twitter.com/nxthompson/sta…\n',
        'tweet_urls': ['https://twitter.com/nxthompson/status/1257671123581444096'], 'emojis': []},
    {'raw_text': "  AI might defeat #Trump because #Biden's intelligence surely won't.😂 twitter.com/Nieczuja_clan/…\n", 'tweet_urls': ['https://twitter.com/Nieczuja_clan/status/1257593194763685889'], 'emojis': ['FACE WITH TEARS OF JOY']}]


def remove_noise(tweet: str):
    """
    Removes noise from the tweets by:
    Tokenizing (Splits sentences into array of words)
    Removes hyperlinks, mentions with regex

    """
    cleaned_tokens = []
    tweet_tokens = word_tokenize(tweet)
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)  # remove hyperlinks
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)  # remove mentions

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        #print('tokenb4', token)
        token = lemmatizer.lemmatize(token, pos)
        #print('tokenAfter', token)
        # remove empty tokens, punctuations and stopwords
        # and (token not in string.punctuation) #previous code
        if len(token) > 1 and (token.lower() not in _stop_words):
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_tweet_data(tweets: List[Dict[str, str]]):
    """
    This function takes a list of tweets, containing web scraped dicts (in particular raw_text) and grabs useful information from it.

    As of now it looks for hashtags (#) and mentions (@)
    """
    # print(tweets)
    # create for-loop on argument "tweets"
    for tweet in tweets:
        # prepare format
        if 'hashtags' not in tweet:  # check unnecesary?
            tweet['hashtags'] = []
        if 'mentions' not in tweet:  # check unnecesary?
            tweet['mentions'] = []
        tweet_text = tweet.get('raw_text')
        # remove newline characters
        tweet_text = tweet_text.replace('\n', ' ')

        # check text for hashtags or mentions
        if (tweet_text != None and '#' or '@' in tweet_text):  # might not be necessary
            for word in tweet_text.split(' '):
                if word.startswith('#'):
                    tweet['hashtags'].append(word)
                    tweet_text = tweet_text.replace(word, '')  # remove hashtag
                if word.startswith('@'):
                    tweet['mentions'].append(word)
                    tweet_text = tweet_text.replace(word, '')  # remove mention
        # handle emojis
        # handle urls
        # handle punctuation (too aggressive)
        #tweet_text = "".join([char for char in tweet_text if char not in string.punctuation])
        tweet['tweet'] = remove_noise(tweet_text)  # must finish with this
    # handle hashtag stats
    # handle mention stats
    return tweets


new_tweets = get_tweet_data(scraped_tweets)

for tweet in new_tweets:
    print('-----\n', tweet, '\n')
