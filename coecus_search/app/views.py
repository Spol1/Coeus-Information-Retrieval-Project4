from app import app,db
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
    query = "trump killing usa"
    tweets = hit_solr(query)
    with open("fetched_tweets.json", 'w') as fout:
        json.dump(tweets , fout)

    # indexer 
    # data = [
    #     go.Bar(
    #         x = ['Boy','Girl'],
    #         y = [10, 15],
    #         hovertemplate= '<i>%{x}</i> : ' + '<b>%{y}</b>'
    #     )
    # ]
    # graphJson = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    # return render_template("index.html", graph = graphJson)
    return "Search complete"


@app.route("/faceted")
def facet_solr():
    # '/select?fl=id%2C%20score&q=text_en' + '%3A%20' + "trump%20covid"+'&rows=20&wt=json'
    list1 = json.load(open("person.json", 'r'))
    posts = db.tweets
    for tweet in list1:
        print(tweet['name'])
        posts.insert(tweet)
    return "Solr hit Successfully"

@app.route("/indian_poi_counts")
def plot_graph():
    mycol = db["tweets"]
    mycol.drop()
    posts = db.tweets
    list1 = json.load(open("new_india_pois.json", 'r', encoding="utf8"))
    dict = {}
    list2 = []
    for tweet in list1:
        if tweet['poi_id'] is not None:
            # print(tweet['poi_name'])
            dict['id'] = tweet['id']
            dict['poi_name'] = tweet['poi_name']
            list2.append([tweet['id'],tweet['poi_name']])
    print("Length: "+ str(len(list1)))
    df = pd.DataFrame(list2, columns=['id','name'])
    df = df.groupby(['name']).size().reset_index(name='count')
    # print(df['count'].tolist())
    data = [
        go.Bar(
            x = df['name'].tolist(),
            y = df['count'].tolist(),
            hovertemplate= '<i>%{x}</i> : ' + '<b>%{y}</b>'
        )
    ]
    graphJson = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', graph = graphJson)