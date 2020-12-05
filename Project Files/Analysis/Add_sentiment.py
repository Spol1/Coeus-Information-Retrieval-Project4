from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import json

endpoint = 'https://sentiment-analysis-irf20p4.cognitiveservices.azure.com/'
key = '98ad5c4c006c450cb927415c0ea05278'
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = []
tweet = []

f = open("E:\\Uno.json", "r", encoding="utf-8")
tweet = json.loads(f.read())
for _ in range(len(tweet)):
    documents.append(tweet[_]['tweet_text'])
f.close()


result = text_analytics_client.analyze_sentiment(documents)
docs = [doc for doc in result if not doc.is_error]

for id,doc in enumerate(docs):
        tweet[id]['sentiment']=doc.sentiment
        '''print(doc)
        print(tweet[id]['id'])
        print(tweet[id]['tweet_text'])
        print(tweet[id]['sentiment'])
        print("Document ID: {}".format(id))
        print("Document text: {}".format(documents[id]))
        print("Overall sentiment: {}\n".format(doc.sentiment))'''
            
f = open("E:\\New_Uno.json", "a", encoding="utf-8")
f.write(json.dumps(tweet))
f.close()