from app import app,db
import urllib.request
from urllib.parse import quote
# from googletrans import Translator
# translator = Translator()

import re
import json


def process_query(query):
    return urllib.parse.quote_plus(query)

def hit_solr(query):
    
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
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']

    return docs