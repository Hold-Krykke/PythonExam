import json
import pandas as pd
print('preprocessing - first commit')
whole_string = 'This is the tweet of the year. #MyFirstTweet @folketinget www.runivn.dk'
author = 'Runi Vedel'
date = '01/05/2020'
#inbound = {'tweet': whole_string}, {'author': author}, {'date': date}
inbound = {}
inbound['tweet'] = whole_string
inbound['author'] = author
inbound['date'] = date
print('Inbound data\n', inbound)
#### handling data ####
handled_hashtags = ['#MyFirstTweet']
handled_people = ['@folketinget']
handled_urls = ['runivn.dk']
handled_tweet = 'This tweet year'
#### handling data ####
outbound = {}
# outbound = [{'tweet': handled_tweet}, {'hashtags': handled_hashtags}]
# outbound = {handled_tweet, handled_hashtags, handled_people, handled_urls}
#print('outbound here:', outbound)
outbound['tweet'] = handled_tweet
outbound['hashtags'] = handled_hashtags
outbound['people'] = handled_people
outbound['urls'] = handled_urls
outbound['author'] = author
outbound['date'] = date
print('Outbound data\n', outbound)
print('-----------------')
inbound_json = json.dumps(inbound)
outbound_json = json.dumps(outbound)
print(inbound_json)
print(outbound_json)
