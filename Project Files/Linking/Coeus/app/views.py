from app import app,conn 
from .indexer import hit_solr, process_query
import plotly
import plotly.graph_objects as go
import json
from flask import jsonify, request, render_template
import pandas as pd
import json

import pandas as pd
import urllib.request

search = {}

@app.route("/")
def home():
    return "Welcome to Coecus Home"

@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      #p_data = data.items()
      
      return render_template("results.html",result = result)

@app.route("/search", methods=['POST'])
def search_tweets():
    sentiment = []
    name = []
    lang = []
    country = []
    # query = "covid warriors"
    #req_data = request.get_json(force=True)
    #search['search'] = request.form.get('search')
    #print(search)
    #data = hit_solr(search)
    req_data = request.form
    for key,value in req_data.items():
        if key[:9] == 'sentiment':
            sentiment.append(key[10:-1])
        elif key[:4] == 'name':
            name.append(key[5:-1])
        elif key[:4] == 'lang':
            lang.append(key[5:-1])
        elif key[:7] == 'country':
            country.append(key[8:-1])
        else:
            search[key]=value
    search['sentiment']=sentiment
    search['name']=name
    search['lang']=lang
    search['country']=country
    print(search)
    data = hit_solr(search)

    docs = data.read().decode('utf-8')
    fin_docs = json.loads(docs)
    numFound = fin_docs['response']['numFound']
    docs = fin_docs['response']['docs']
    #tweets_df = jsonToDF(docs)
    #print(tweets_df['tweet_id'])
    
    poi_name = {}
    lang = {}
    country = {}
    hashtags = {}
    sentiment = {}

    facet_fields = fin_docs['facet_counts']['facet_fields']
    for key in facet_fields.keys():
        temp = {facet_fields[key][i]: facet_fields[key][i + 1] for i in range(0, len(facet_fields[key]), 2)}
        #print(type(temp))
        if key == "poi_name": poi_name = temp
        if key == "lang": lang = temp
        if key == "country": country = temp
        if key == "hashtags": hashtags = temp
        if key == "sentiment": sentiment = temp
    print('***************************** VIEW BEFORE FINAL **************')
    final_result = {}
    final_result = {
        'tweets': docs,
        'analysis': {
            'poi_name': poi_name,
            'lang': lang,
            'country': country,
            'hashtags': hashtags,
            'sentiment': sentiment
            # 'time_series': time_series
        },
        'total': numFound
    }
    result = final_result
    #print(result)
    '''for key, value in result['analysis']:
        print(key)
        print(value)'''
    print('***************************** VIEW BEFORE RETURN **************')
    return render_template("base.html",result = result)

'''@app.route("/solr_query")
def hit_solr():
    core_name = "IRF20P4"
    ip_address = "localhost:8983/solr/"
    select_ = "/select?"
    or_string = "%20OR%20"
    and_string = "%20AND%20"

    # querylang = translator.detect(query).lang
    query = 'Modi'
    querylang = 'en'
    hashtags = re.findall(r"#(\w+)", query)
    hashtags = str(hashtags)
    hashtags = hashtags.replace('[','')
    hashtags = hashtags.replace(']','')
    hashtags = quote(hashtags)
    # query_en = translator.translate(query, src='', dest='en').text
    # query_it = translator.translate(query, src='', dest='it').text
    # query_hi = translator.translate(query, src='', dest='hi').text
    # print(query_en + " || " + query_hi + " || " + query_it)
    query_en = query
    query_en = process_query(query_en)
    query_hi = process_query(query_en)
    query_it = process_query(query_en)

    # select_fields = "fl=" + process_query("id, country, user.screen_name, full_text, tweet_text, tweet_lang, tweet_date, score")
    select_fields = ""
    limit = "&indent=true&rows=5&wt=json"
    inurl = select_fields + "&q=" + "tweet_hashtags" + '%3A%20' + hashtags + or_string + 'text_en' + '%3A%20' + query_en + or_string + 'text_it' + '%3A%20' + query_it + or_string + 'text_hi' + '%3A%20' + query_hi

    if querylang == 'hi':
        inurl = inurl + "&defType=dismax&qf=tweet_hashtags%5E1.7%20text_en%5E1.6%20text_hi%5E2.5%20text_it%5E2.0&tie=0.1"
    elif querylang == 'it':
        inurl = inurl + "&defType=dismax&qf=tweet_hashtags%5E1.7%20text_en%5E1.6%20text_hi%5E2.2%20text_it%5E2.7&tie=0.1"
    else:
        inurl = inurl + "&defType=dismax&qf=tweet_hashtags%5E1.7%20text_en%5E2.5%20text_hi%5E2.0%20text_it%5E2.0&tie=0.1"

    inurl = ip_address + core_name + select_ + inurl + limit
    data = urllib.request.urlopen('http://localhost:8983/solr/IRF20P4/select?fl=user.name%2C%20tweet_text&q=tweet_text%3ATrump&wt=json')
    docs = json.load(data)['response']
    dataframe = []
    for data in docs['docs']:
        df = []
        df.append(data['user.name'][0])
        df.append(data['tweet_text'][0])
        dataframe.append(df)
    
    dataframe = {'person':['Yash','Arshad','Saurabh','Yohanth'],'language':['English','Hindi','RUssian'],'country':['United States','India','Russia'],'hashtags':['covid','goverment','corrupt']}
    return render_template('base.html', dataframe = dataframe)
    #return render_template('base.html')'''

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