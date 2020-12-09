import pandas as pd
import numpy as np
import json

# tfile = open("solr_local.json", 'r', encoding= 'utf-8')

def jsonToDF(tweets):
    tweets_list = []
    #assuming solr returned json will be a file I used load function below else we can directly use json object of
    #returned docs as paarmeter for this function and directly loop over json objects within
    # tweets = json.load(tjson_file)
    for t in tweets:
        t_dict={}
        t_dict['tweet_id']= t.get('id')
        t_dict['full_text']= t.get('full_text')[0]
        # t_dict['tweet_text']=t.get('tweet_text')[0]
        t_dict['text_en']=t.get('text_en')[0]
        t_dict['hashtags']=t.get('hashtags')
        t_dict['tweet_lang']=t.get('lang')[0]
        t_dict['country']=t.get('country')[0]
        t_dict['tweet_date']=str(t.get('tweet_date')[0])[0:10]
        t_dict['sentiment']=t.get('sentiment')[0]
        
        t_dict['followers']=t.get('user.followers_count')[0]
        #t_dict['user_verified']=t.get('user.verified')[0]
        t_dict['friends']=t.get('user.friends_count')[0]
        t_dict['fav_count']=t.get('user.favourites_count')[0]
        t_dict['listed_count']=t.get('user.listed_count')[0]
        t_dict['retweet_count'] = t.get('retweet_count')[0]
        #t_dict['statuses_count'] = t.get('user.statuses_count')[0]
        if t.get('poi_id'):
            t_dict['is_poi'] = 1
        else:
            t_dict['is_poi'] = 0
        
        if t.get('user.verified')[0] is True:
            t_dict['is_verified'] = 1
        else:
            t_dict['is_verified'] = 0
        
        t_dict['follow_ratio']=round(t.get('user.followers_count')[0]/t.get('user.friends_count')[0],4)
            
        #testing print statements
        #print(type(t.get('poi_id')), "&&&&&&&&&&&&&&&&&&")
        #print(type(t.get('user.verified')[0]), "&&&$$$$$$$*(**&^&*%%^&&&&")
        tweets_list.append(t_dict)
        
    #dataframe from the entire corpus
    tweet_df = pd.DataFrame(tweets_list)
    
    return tweet_df

def facetsToDF(facets):
    poi_list = facets.get('poi_name')
    return 0