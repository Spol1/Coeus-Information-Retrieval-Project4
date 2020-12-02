from app import app, conn
from .indexer import hit_solr, process_query
import plotly
import plotly.graph_objects as go
import json
from flask import render_template
import pandas as pd
import json


@app.route("/")
def home():
    return "Welcome to Coecus Home"


@app.route("/search")
def search_tweets():
    query = "covid warriors"
    tweets, numFound = hit_solr(query)
    print(numFound)
    with open("fetched_tweets.json", 'w') as fout:
        json.dump(tweets, fout)

    # Insertion into mongoDB
    db = conn.tweetsDB
    collection = db.tweets_data

    # for t in tweets:
    #     tweet_df = pd.DataFrame.from_dict(t, orient="index")
    #     print(tweet_df)

    tweet_df = pd.DataFrame(tweets)
    print(tweet_df)
    # count = 0
    # for tweet in tweets:
    #     print("count : ", str(count))
    #     collection.insert_one(tweet)
    #     count+=1

    return "Search complete"


@app.route("/faceted")
def facet_solr():
    # '/select?fl=id%2C%20score&q=text_en' + '%3A%20' + "trump%20covid"+'&rows=20&wt=json'
    list1 = json.load(open("person.json", 'r'))
    db = conn.tweetsDB
    collection = db.tweets_data
    for tweet in list1:
        print(tweet['name'])
        collection.insert_one(tweet)
    return "Solr hit Successfully"

