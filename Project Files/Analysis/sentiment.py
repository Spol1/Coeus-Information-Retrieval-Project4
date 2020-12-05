from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

endpoint = 'https://sentiment-analysis-irf20p4.cognitiveservices.azure.com/'
key = '98ad5c4c006c450cb927415c0ea05278'
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = ['this is good','this sucks']#<---------- Sending the text

result = text_analytics_client.analyze_sentiment(documents)
docs = [doc for doc in result if not doc.is_error]

print("Sentiments are as follows\n")
for id,doc in enumerate(docs):
            #print(doc)
            print("Document ID: {}".format(id))
            print("Document text: {}".format(documents[id]))
            print("Overall sentiment: {}\n".format(doc.sentiment))