# 4. Semester Python Exam

#### Table of contents
- [Purpose of the program](https://github.com/Hold-Krykke/PythonExam/blob/master/README.md#purpose-of-the-program)
  - [Technologies](https://github.com/Hold-Krykke/PythonExam/blob/master/README.md#technologies)
  - [Things that we would have liked to implement](https://github.com/Hold-Krykke/PythonExam#things-that-we-didnt-implement-but-would-have-liked-to)
- [Using the program](https://github.com/Hold-Krykke/PythonExam/blob/master/README.md#using-the-program)
  - [Using the program with Flask](https://github.com/Hold-Krykke/PythonExam/blob/master/README.md#using-the-program-with-flask)
  - [Using the program with CLI](https://github.com/Hold-Krykke/PythonExam/blob/master/README.md#using-the-program-with-cli)

#### Made by:
* Cph-mh748 - Malte Hviid-Magnussen 
* Cph-rn118 - Rúni Vedel Niclasen 
* Cph-ab363 - Asger Bjarup 
* Cph-cs340 - Camilla Staunstrup 

## Purpose of the program
We would like to delve deeper into text analysis and web scraping.  

We scrape data from Twitter, based on hashtag searches, and use different techniques to clean, analyze and present the data.

Example tweets to perform *sentiment analysis* on could be:  
* __#Trump, #Trump2020__
* __#Biden, #Biden2020__
* __#Election2020__  

### Technologies

* __Web scraping of Twitter, based on hashtags__
  * Technologies:
    * Web scraping with [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
    * Cleaning data with the [emoji](https://pypi.org/project/emoji/) package.
    * File handling with `os`, `Path` modules.
* __Preprocessing of Twitter data (clean-up, removing stop words)__
  * Technologies:
    * Regex
    * Natural Language Toolkit [(NLTK)](http://www.nltk.org/) 
* __Sentiment analysis__
  * Technologies:
    * Natural Language Toolkit [(NLTK)](http://www.nltk.org/) 
* __Presentation (graphs/plots)__
  * Technologies:
    * matplotlib
    * pandas
    * File handling with the `Path` module.
* __Availability (To the user)__
  * Technologies:
    * Flask
    * Argparse for the CLI

### Things that we didn't implement but would have liked to: 
- Other types of text/topic analysis
- More technologies, such as `sklearn`
- Utilize Twitters advanced search functions, such as sorting by popularity, with/without pictures, etc.

## Using the program 
1. Clone the repo and follow the instructions in [setup.ipynb](https://github.com/Hold-Krykke/PythonExam/blob/master/setup.ipynb)  

Note: Not all plots work with all data. A few cases might result in bad output.

### Using the program with Flask

__Starting the server__
* Open terminal in root directory
* `cd` into the `modules` folder
* Use `python` to run the `flask_service.py`
* Wait for a while until it says `Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)` in the terminal (this might take a while (~40 seconds) since the machine learning model is trained once every time the server is started)

__Using the endpoint__

The server exposes a single endpoint `/api/sentiment` where you have to make all your requests.
Use **Postman** or a similar tool to test the server at `http://localhost:5000/api/sentiment` - we have not deployed the server. There is no UI for the server so every request has to be made in a tool like **Postman**.
(Showing examples from **Postman**)
* All requests made must use the HTTP method **POST**
* You can make a request without providing any search options which will result in a code **400** response but will give you an example of what to provide the body of your request:
![image](https://user-images.githubusercontent.com/44898491/82652988-d4b7f900-9c1e-11ea-98a3-cd1d74f7d341.png)
* Click `Preview` and copy everything after `Example: `. Paste it into the body of your request
* All search options must be provided in JSON format. The body of a request can look like this:
![image](https://user-images.githubusercontent.com/44898491/82653511-9a029080-9c1f-11ea-8e5b-fed02980b38d.png)
* You can click beautify to make the JSON look proper 
* Another example of JSON in the request body:
`{
    "hashtags": [
        "trump",
        "biden"
    ],
    "start_date": "2020-5-17",
    "end_date": "2020-5-22",
    "plot_type": "line",
    "remove_sentiment": "Uncertain",
    "tweet_count": 300,
    "fresh_search": true
}`
* The JSON above will result in the following plot:
![image](https://user-images.githubusercontent.com/44898491/82653968-493f6780-9c20-11ea-94db-1dfd69f82e5c.png)
* The y-axis shows the amount of tweets. The x-axis shows the date

__Explanation of search options__
*Data gathering*
* Hashtags - the hashtags you want to search for on twitter
  * Example: `"hashtags": [
        "trump",
        "biden"
    ]`
  * Must be an array of strings with the name `hashtags`

*Data filtering*
* Start date - the start date for the period of time you want tweets from
  * Example: `"start_date": "2020-5-17"`
  * Choosing a start date that is 5 - 10 days before the end date will give the prettiest plot
  * Choosing a start date at a later point in time than the end date will result in no data which means the plot can't be created
* End date - the end date of the period of time you want tweets from
  * Example: `"end_date": "2020-5-22"`
  * We recommend choosing the current date as end date so you can get the latest tweets
  * Choosing an end date that is in the future won't give any future predictions or results
* Plot type - the type of plot you want
  * Example: `"plot_type": "line"`
  * There are 3 types of plots: `bar`, `line` and `pie`
  * We recommend using the `line` plot (the other types may not work)
* Removing sentiment - remove either `Positive` tweets  or `Negative` tweets or the ones with a mixed sentiment (`Uncertain`)
  * Example: `"remove_sentiment": "Uncertain"`
  * All three values must be spelled with the first letter in upper case
* Tweet amount - the amount of tweets you want to scrape from Twitter
  * Example: `"tweet_amount": 300`
  * The higher the tweet count is, the further back in time you can go since the web scraper scrapes tweets in the same order as tweets are view on Twitter (which is somewhat chronologically)
  * Default is 300
* Fresh search - whether or not you want to get new tweets or tweets from previous searches (if available)
  * Example: `"fresh_search": true`
  * Default is false
  * A fresh search of 300 tweets takes ~10 seconds
* Search for mentions or hashtags
  * Example: `"search_for": {
        "mentions": "@JoeBiden"
    }`
  * Example: `"search_for": {
        "hashtags": "#trump"
    }`
  * Requires an object with a single attribute with a key that must be either `mentions` or `hashtags`. The value should match the key so if the key is `mentions` then the value must begin with `@` 
  * We recommend not using this filter (especially the `mentions` option) since it in most cases filters away all the data resulting in an empty plot or no plot at all
* Get statistics - Use this if you want some statistics about the data instead of a plot with an analysis
  * Example: `"get_stats": "hashtags"`
  * There are two options: `"hashtags"` and `"mentions"`
  * You can use this option to look through the list of hashtags or mentions in the gathered tweets and if you e.g. find out that `@realDonaldTrump` has been mentioned ten times then you can do a new search with these options: 
  `{
    "hashtags": [
        "trump",
        "biden"
    ],
    "start_date": "2020-5-17",
    "end_date": "2020-5-22",
    "plot_type": "line",
    "search_for": {
        "mentions": "@realDonaldTrump"
    },
    "tweet_count": 300,
    "fresh_search": false
}` to find the sentiment of those tweets. 

__Overall Recommendation__
* Choose an end that is equal to the current data
* Choose a start date ~ten days before end date
* Search for `"trump"` and `"biden"`
* Remove the `"Uncertain"` sentiment
* Choose `"line"` as plot type
* Choose a tweet amount of 300

JSON: `{
    "hashtags": [
        "trump",
        "biden"
    ],
    "start_date": "2020-5-12",
    "remove_sentiment": "Uncertain",
    "end_date": "2020-5-22",
    "plot_type": "line",
    "tweet_amount": 300
}`

---

### Using the program with CLI
1. In the root folder, run `python app.py -h` to print the **help** output:  

<p align="center">
<img src="https://i.imgur.com/wCrfTY0.png" height=850 width=750/>  
</p>

#### Default values
All the optional arguments have default values.  
The program can run using all default values by simply passing the hashtags you want to gather info from.
 
 #### Examples
**Utilizing default values** to search for the hashtags `#trump` and `#biden`:  
`python app.py trump biden`  
This would run the program using the following values:
```py
{'certainty_high': 0.75,
 'certainty_low': 0.25,
 'date': [datetime.date(2020, 5, 22),
          datetime.date(2020, 5, 27)],
 'fresh_search': False,
 'hashtags': ['trump', 'biden'],
 'plot_type': 'pie',
 'remove_sentiment': None,
 'save_plot': False,
 'search_hashtags': None,
 'search_mentions': None,
 'search_urls': None,
 'tweet_count': 300}
 ```
 *Date by default is set to current day + 5 days*
 
 **Changing `plot type` and filtering on dates**  
 `python app.py -p bar -d 2020-06-01 2020-06-02` or  
 `python app.py --plot bar --date 2020-06-01 2020-06-02`
 
 **Search for a specific amount of tweets (1000) and save the generated plots locally**  
 `python app.py -s -c 1000` or  
 `python app.py --save --count 1000`
