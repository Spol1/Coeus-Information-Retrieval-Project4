from app import app,db
import urllib.request
from urllib.parse import quote
from googletrans import Translator
import re
import json
translator = Translator()

def process_query(query):
    query = query.replace("\n", " ")
    query = query.replace(":", r"\:")
    query = "(" + query + ")"
    query = quote(query)
    print(query)
    return query

def hit_solr(query):

    core_name = "IRF20P4"
    ip_address = "http://localhost:8983/solr/"
    
    select_ = "/select?"
    or_string = "%20OR%20"
    and_string = "%20AND%20"
    querylang = translator.detect([query])[0].lang
    hashtags = re.findall(r"#(\w+)", query)
    hashtags = str(hashtags)
    hashtags = hashtags.replace('[','')
    hashtags = hashtags.replace(']','')
    hashtags = quote(hashtags)
    query = process_query(query)
    query_en = translator.translate(query, dest='en').text
    query_it = translator.translate(query, dest='it').text
    query_hi = translator.translate(query, dest='hi').text
    query_en = process_query(query_en)
    query_it = process_query(query_it)
    query_hi = process_query(query_hi)

    select_fields = "fl=id%2C%20country%2C%20user.screen_name%2C%20full_text%2C%20tweet_text%2C%20tweet_lang%2C%20tweet_date"

    limit = "&rows=10&wt=json"
    inurl = ip_address + core_name + select_ + select_fields + "&q=" + "tweet_hashtags" + '%3A%20' + hashtags + or_string + 'text_en' + '%3A%20' + query_en + or_string + 'text_it' + '%3A%20' + query_it + or_string + 'text_hi' + '%3A%20' + query_hi
    
    # '&defType=dismax&qf=tweet_hashtags^1.7%20+text_en^1.6%20+text_de^2.0%20+text_ru^2.2&tie=0.1'
    if querylang == 'hi':
        inurl = inurl + "&defType=dismax&qf=tweet_hashtags^1.7%20+text_en^1.6%20+text_hi^2.0%20+text_it^2.2&tie=0.1"
    elif querylang == 'it':
        inurl = inurl + "&defType=dismax&qf=tweet_hashtags^1.7%20+text_en^1.6%20+text_hi^2.2%20+text_it^2.7&tie=0.1"
    else:
        inurl = inurl + "&defType=dismax&qf=tweet_hashtags^1.7%20+text_en^2.5%20+text_hi^2.0%20+text_it^2.0&tie=0.1"

    inurl = inurl + limit

    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']
    

    return "Solr hit"