from datetime import datetime
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

scraped_tweets = [{'raw_text': '  THANK YOU @LindseyGrahamSC . I know you are #Trump ‘s ally; it’s gratifying to see you stand by #Biden. twitter.com/sarahmucha/sta…\n', 'tweet_urls': ['https://twitter.com/sarahmucha/status/1256404280875114499'], 'emojis': [], 'date': '2020,5,1'},
                  {'raw_text': '  Tomorrow I’ll be joined by @SebGorka, @STEPHMHAMILL and other distinguished guests to discuss the 2020 Presidential Election. \n\nTune into WJLA 24/7 tomorrow from 10:30-11:30 AM EST for another edition of The Armstrong Williams Show. #AWS #Election2020 #Trump #Biden @ABC7News pic.twitter.com/TTldPAD5RL\n',
                      'tweet_urls': ['https://twitter.com/Arightside/status/1256364526741729288/video/1'], 'emojis': [], 'date': '2020,5,1'},
                  {'raw_text': '  The Narc In Chief is eyeing the November Election\n\nCue the nonstop lying and gaslighting through tweets, positive spin TV and his parade of sycophants\n\n@realDonaldTrump is a proven Liar and Divider, and is profoundly Unfit to serve as #POTUS\n#Trump #GoJoe #Biden #TrumpIsAnIdiot pic.twitter.com/SEm270Og9M\n',
                      'tweet_urls': ['https://twitter.com/rightNtruthMat/status/1257304920039940097/photo/1'], 'emojis': [], 'date': '2020,5,4'},
                  {'raw_text': '  God bless America . In #trump we trust. Saved the word from #Covid19 single handed.holy moly ...talk about believing your own PR. Can you actually lose #biden\npic.twitter.com/GTRFbuq3f4\n',
                   'tweet_urls': ['https://twitter.com/realDonaldTrump/status/1257129479455080448/video/1'], 'emojis': [], 'date': '2020,5,6'},
                  {'raw_text': "  If you're a woman, a person of color, an immigrant, a suburbanite, a senior, college student, college grad, a white male w/a conscience & ANYONE w/a moral center who respects decency, the rule of law & democracy you must vote for @JoeBiden...#Trump #Biden nydailynews.com/opinion/ny-ope…\n",
                   'tweet_urls': ['https://www.nydailynews.com/opinion/ny-oped-nelson-jacobus-never-trump-20200505-o6w35mfyd5ffvk2jeddgfl4x5i-story.html?fbclid=IwAR1uJj6cyy1yRRcl_8P66Owud-OjHbUy3vW7iO6KsXnSi5TuZeQ6OXyrl0c'], 'emojis': [], 'date': '2020,5,5'},
                  {'raw_text': '  In the most recent Monmouth Poll...#Biden widens his lead over #trump by 9 points...50-41%.\n\n#RidenWithBiden\n#LetsEndTheNightmare\n#VoteBlue2020 @JoeBiden\n',
                   'tweet_urls': [], 'emojis': [], 'date': '2020,5,6'},
                  {'raw_text': ' #Election2020 #ElectoralCollege #Projection\nExpected: #Biden: 352 | #Trump: 186 | +166 EV\n#Biden  Best 412-126  | +286 EV\n#Trump Best: 269-269 Tie\n\nThe tipping point state is North Carolina where Biden is ahead by 4.2%.\n\nelectiongraphs.com/2020ec/\n',
                   'tweet_urls': ['https://electiongraphs.com/2020ec/'], 'emojis': [], 'date': '2020,5,6'},
                  {'raw_text': '  RCP Average of 8 #Polls from 5/6-5/24 in 2016:\n#Clinton: 44.1% (Net +1)\n#Trump:  43.1%\n\nRCP Average of 8 #Polls from 4/13-5/5 in 2020:\n#Biden:  47.6% (Net +5.5)\n#Trump: 42.1%\n\nDid 5/6-5/24 for 2016 because that is when Trump was leading in the most polls all year.\n', 'tweet_urls': [
                  ], 'emojis': [], 'date': '2020,5,6'},
                  {'raw_text': "  If #Trump grabbed'em by the p*ssy...\n and #Biden slipped a finger in... \nThen #AlexJones should run...\nand he's more likely to win.............. pic.twitter.com/q2RulmpJp7\n",
                   'tweet_urls': ['https://twitter.com/ElreoCarlos/status/1257762877114470400/video/1'], 'emojis': [], 'date': '2020,5,5'},
                  {'raw_text': '  .@realDonaldTrump: "I am not fucking losing to @JoeBiden" \n\nOh yes you are, bud. And in a landslide. The biggest, most embarrassing, humiliating, devastating landslide in history. There\'s still time to quit and save orange face... #Trump #Biden huffpost.com/entry/trump-er…\n',
                   'tweet_urls': ['https://www.huffpost.com/entry/trump-erupt-campaign-team-poll-numbers_n_5eaa44eec5b633a8544528f4'], 'emojis': [], 'date': '2020,4,30'},
                  {'raw_text': '  🇺🇸#USA, presidential election #poll :\n\n🔼#Biden (D) : 50 % (+2)\n⏬#Trump (R) : 41 % (-3)\n\n#MonmouthUniversity, 04/05/20 pic.twitter.com/L39hSBfg7m\n', 'tweet_urls': [
                      'https://twitter.com/ElectsWorld/status/1258108199733022720/photo/1'], 'emojis': ['', '', 'UP-POINTING SMALL RED TRIANGLE'], 'date': '2020,5,6'},
                  {'raw_text': '  Context: DEMOCRAT state & local leaders. They oppose everything Trump says, does, breathes, exists, etc. \n\n#BigMommaYamiche always leaves out that the people attacking #Trump are not attacking him on policy. They hate his guts. So does #NotroiousBMY & other @whca #Biden activists pic.twitter.com/R5E1hmIwad\n',
                   'tweet_urls': ['https://twitter.com/TYGRRRREXPRESS/status/1258142894839361536/photo/1'], 'emojis': [], 'date': '2020,5,6'},
                  {'raw_text': '  Stop feeding me with #TRUMP news. It is like a broken record, repeating repeating repeating! Get some new contents up for the poor man. #america #biden #china #northkorea #COVIDー19\n',
                   'tweet_urls': [], 'emojis': [], 'date': '2020,5,6'},
                  {'raw_text': '  Dear America: our country is being ravaged by a deadly #pandemic and economic meltdown and THIS is how #Trump spends his time. Is THIS who we want at the controls for another four years? We have a choice. VOTE #BIDEN twitter.com/realDonaldTrum…\n',
                   'tweet_urls': ['https://twitter.com/realDonaldTrump/status/1256702883199881216'], 'emojis': [], 'date': '2020,5,3'},
                  {'raw_text': "  The same people who screeched all over Twitter about the #Trump pussy comment are the same people that are now saying they don't care what #Biden did they will vote for him anyway \n\nAbsolute fucking Left wing hypocrites\n",
                   'tweet_urls': [], 'emojis': [], 'date': '2020,5,6'},
                  {'raw_text': '  🗳️US Elections Betting Tips🗳️\n\n🗣️Trump Is Struggling In Polls And Needs A Strong Third-Party Challenge\n\n☑️Where is the betting value in the US Elections?\n\nHERE ▶️ bettingtips4you.com/us-election-be…\n#uselection #Trump #Biden pic.twitter.com/4egqsrQAUp\n',
                   'tweet_urls': ['https://bettingtips4you.com/us-election-betting/', 'https://twitter.com/BTips4you/status/1258037698838880256/photo/1'], 'emojis': ['', '', ''], 'date': '2020,5,6'},
                  {'raw_text': '  Tara #Reade has changed her story. Now says she NEVER said sexual harassment! #Biden says let her talk and produce any records from the Senate! #Trump has 33 sexual harassment claims, 2 in court and 100’s of NDA’s. @realDonaldTrump let the women speak! twitter.com/summitandnuffi…\n',
                   'tweet_urls': ['https://twitter.com/summitandnuffin/status/1258137679327346688'], 'emojis': [], 'date': '2020,5,6'},
                  {'raw_text': '  Monmouth Univ poll  #Trump 41%  #Biden 50%.   Among men Trump leads 44-46, Among women,  Biden leads 56% to 36%. Women hold the purse strings! Not looking good for your rally cry!\n',
                   'tweet_urls': [], 'emojis': [], 'date': '2020,5,6'},
                  {'raw_text': ' @haydentiff While 777.77 777 Amash has don\'t some positives follow/follow in foreign policy; overall he scores a D on the SCOPE test. He, #Trump & #Biden will have to bust a— to earn my endorsement & vote! twitter.com/jackhunter74/s…\n',
                   'tweet_urls': ['https://twitter.com/jackhunter74/status/1258041753493520384'], 'emojis': [], 'date': '2020,5,6'}]


def _handle_date(date_string: str):
    """
    We receive dates from tweets in the format 'yyyy-m-d'.
    This function returns a datetime.date object with proper formatting (yyyy-mm-dd)
    """
    # return date(*[int(date) for date in date_string.split(',')]) # sorry we didnt get to use you ;(
    return datetime.strptime(date_string, '%Y,%m,%d').date()


def _remove_noise(tweet: str):
    """
    Removes noise from the tweets by:
    Tokenizing (Splits sentences into array of words)
    Removes hyperlinks, mentions with regex
    Removes special characters (primarily used for emojis) as well as numbers.
    """
    cleaned_tokens = []
    tweet_tokens = word_tokenize(tweet)
    for token, tag in pos_tag(tweet_tokens):

        # remove hyperlinks
        token = re.sub(
            '(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)  # remove mentions
        # remove special chars, inc emojies
        token = re.sub("[^A-Za-z0-9]", "", token)
        token = re.sub("[0-9]", "", token)  # remove numbers

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        # print('tokenb4', token)
        token = lemmatizer.lemmatize(token, pos)
        # print('tokenAfter', token)
        # remove empty tokens, punctuations and stopwords
        # use substring search (find) instead?
        token = token.lower().strip()
        if len(token) > 1 and token not in string.punctuation and token not in _stop_words:
            cleaned_tokens.append(token)
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
        # remove newline characters (necessary to add spaces between words)
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
        # handle dates
        tweet['date'] = _handle_date(tweet['date'])
        # handle emojis

        # handle punctuation (too aggressive)
        # tweet_text = "".join([char for char in tweet_text if char not in string.punctuation])
        tweet['tweet'] = _remove_noise(tweet_text)  # must finish with this
    # handle hashtag stats
    # handle mention stats
    return tweets


new_tweets = get_tweet_data(scraped_tweets)

for tweet in new_tweets:
    print('-----\n', tweet, '\n')