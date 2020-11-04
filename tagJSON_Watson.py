import json
import os
import re
from ibm_watson import NaturalLanguageUnderstandingV1 as NLU
from ibm_watson import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions
from sshtunnel import SSHTunnelForwarder

# acess tokens
api_key = 'wLer7NnOejSljCZKyx-lFg1fccXoFgsBqQYKX7PRYkJG'
api_URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/3750a739-2688-44ea-a78d-5bcd3017d07a'

authenticator = IAMAuthenticator(api_key)

# configure api
nlu = NLU(
    version='2020-08-01',
    authenticator=authenticator
)
nlu.set_service_url(api_URL)

# path to tweets file
untagged_path = 'C:/Users/Brynn/PycharmProjects/TwitterScraping/filtered_PermID.json'
tagged_path = 'C:/Users/Brynn/PycharmProjects/TwitterScraping/tagged_tweets_Watson.json'

# parse json
obj_list = []
with open(untagged_path, encoding="utf8") as f:
    for jsonObj in f:
        data_dict = json.loads(jsonObj)
        obj_list.append(data_dict)

tweets = []
for obj in obj_list:
    #print(obj, "\n\n\n")
    for sub in obj:
        #print(sub)
        for x in sub:
            #print(x)
    tweets.append(obj["text"])


tagged_data = [] 
# make api call to tag tweets, print result as json
for tweet in tweets:
    if (tweet != ""):
        try:
            response = nlu.analyze(
                        text=tweet,
                        features = Features(categories = CategoriesOptions(limit=6))
                    ).get_result()
            print(tweet)
            print(json.dumps(response, indent=2))
            tagged_data.append({"tweet": tweet, "tags": response})
        except ApiException as ex:
            print("Method failed with status code", str(ex.code), ": ", ex.message)
with open(tagged_path, 'w') as out_path:
    json.dump(tagged_data, out_path, indent=4) 
"""
for x in range(5):
    tweet = tweets[x]
    tweet = re.sub(r'[^a-zA-Z ]+', '', tweet)
    if (tweet != ""):
        try:
            response = nlu.analyze(
                        text=tweet,
                        features = Features(categories = CategoriesOptions(limit=6))
                    ).get_result()
            #print(tweet)
            #print(json.dumps(response, indent=2))
            tagged_data.append({"tweet": tweet, "tags": response})
        except ApiException as ex:
            print("Method failed with status code", str(ex.code), ": ", ex.message)
with open(tagged_path, 'w') as out_path:
    json.dump(tagged_data, out_path, indent=4)
"""


