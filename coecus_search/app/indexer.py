from app import app,db
import urllib.request
from urllib.parse import quote
from googletrans import Translator
import re
import json
translator = Translator()

def process_query(query):
    return urllib.parse.quote_plus(query)

def hit_solr(query):

    core_name = "IRF20P4"
    ip_address = "http://localhost:8983/solr/"
    select_ = "/select?"
    or_string = " OR "
    and_string = " AND "
    querylang = translator.detect([query])[0].lang
    hashtags = re.findall(r"#(\w+)", query)
    hashtags = str(hashtags)
    hashtags = hashtags.replace('[','')
    hashtags = hashtags.replace(']','')
    hashtags = quote(hashtags)
    query_en = translator.translate(query, dest='en').text
    query_it = translator.translate(query, dest='it').text
    query_hi = translator.translate(query, dest='hi').text
    # print(query_en + " || " + query_hi + " || " + query_it)

    select_fields = "fl=id, country, user.screen_name, full_text, tweet_text, tweet_lang, tweet_date"

    limit = "&rows=5&wt=json"
    inurl = ip_address + core_name + select_ + select_fields + "&q=" + "tweet_hashtags" + ': ' + hashtags + or_string + 'text_en' + ': ' + query_en + or_string + 'text_it' + ': ' + query_it + or_string + 'text_hi' + ': ' + query_hi

    if querylang == 'hi':
        inurl = inurl + "&defType=dismax&qf=tweet_hashtags^1.7 +text_en^1.6 +text_hi^2.0 +text_it^2.2&tie=0.1"
    elif querylang == 'it':
        inurl = inurl + "&defType=dismax&qf=tweet_hashtags^1.7 +text_en^1.6 +text_hi^2.2 +text_it^2.7&tie=0.1"
    else:
        inurl = inurl + "&defType=dismax&qf=tweet_hashtags^1.7 +text_en^2.5 +text_hi^2.0 +text_it^2.0&tie=0.1"

    inurl = inurl + limit
    inurl = process_query(inurl)
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']

    return docs