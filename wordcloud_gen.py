from twitter import *
import json
import oauth2 as oauth
from flask import Flask, render_template, request, send_file

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import urllib
import requests
import numpy as np
import matplotlib.pyplot as plt


consumer_key = "BoSJMv0ZyhvahGXlgsByPb2aJ"
consumer_secret = "UqsphplOdh5nSB3ygcTG9IyFvhW1FLdxjB1fVQTSfJCIcBo05f" 
access_token_key = "938932912870658048-tbGES2bhLZxaeXiVcArnjVSjfWURTK5"
access_token_secret = "GjgdFyD5NoyLogeO1PhsGHglYpbduzDJmT34m4KKWDPqg"

all_stopwords = STOPWORDS
more_stopwords = ['https','co','RT','alright','txt','tk','retweet','txties','chop chop']
for word in more_stopwords:
    all_stopwords.add(word)

TWITTER_API_URL = "https://api.twitter.com/1.1/search/tweets.json"

def endpoint_gen(word):
    # timeline_endpoint = "https://api.twitter.com/1.1/search/tweets.json?q=" + word + "&count=100"
    search_term = "abortion"
    # search_term = search_term.replace("","+")
    # search_terms = [search_term_1, search_term_2]
    # search_terms = '+'.join(search_terms)
    url = "https://api.twitter.com/1.1/search/tweets.json?result_type=recent&count=100&lang=en&tweet_mode=extended&q=" + search_term
    # payload = {
    #     'result_type': 'recent',
    #     'count':100,
    #     'lang':'en',
    #     'tweet_mode':'extended',
    #     'q': word,
    # }
    # r = requests.get(TWITTER_API_URL, params=payload)
    # return r.url
    return url

def query(endpoint):
    consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    access_token = oauth.Token(key=access_token_key, secret=access_token_secret)
    client = oauth.Client(consumer, access_token)
    endpoint_url = endpoint_gen(endpoint)
    response, data = client.request(endpoint_url)
    parsed = json.loads(data)
    return parsed

def tweet_text(statuses):
    # print(type(statuses))
    statuses = statuses['statuses']
    tweets = []
    for stat in statuses:
        tweets.append(stat['full_text'])
    tweets = ''.join(tweets)
    return tweets

#words = open(path.join(d, 'alice_in_wonderland.txt')).read()


# This function takes in your text and your mask and generates a wordcloud. 
def generate_wordcloud(words, mask):
    word_cloud = WordCloud(width = 512, height = 512, background_color='white', stopwords=all_stopwords, mask=mask).generate(words)
    # word_cloud.generate(words, mask).to_image()
    plt.figure(figsize=(10,8),facecolor = 'white', edgecolor='black')
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig("wordcloud.png")
    file = open("wordcloud.png", mode="rb")
    return file
    # plt.show()
    # plt.to_file("static/wordcloud.png")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/gen_cloud') #, methods=['GET', 'POST'])
def render_results():
    word = request.args['search_term']

    endpoint = endpoint_gen(word)
    tweet_data = query(endpoint)
    text = tweet_text(tweet_data)
    mask = np.array(Image.open(requests.get('https://static01.nyt.com/images/2014/08/10/magazine/10wmt/10wmt-master1050-v4.jpg', stream=True).raw))
    cloud = generate_wordcloud(text, mask)
    #puzzle = request.args['puzzle']
    #Contents of a form are stored in a dictionary
    # We can also pass the data to the html to have a more dynamic handling
    #solutions = solve(puzzle)
    #return str(solutions)
    # return render_template('results.html') #, data=sorted(solutions))
    return send_file(cloud, 'image/png')