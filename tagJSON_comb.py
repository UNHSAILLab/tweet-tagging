import rdflib
import rdflib_jsonld
import json
import re
import os
from collections import defaultdict
from OpenPermID import OpenPermID
from ibm_watson import NaturalLanguageUnderstandingV1 as NLU
from ibm_watson import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions

# configure PermID API
opid = OpenPermID()
opid.set_access_token('76kCI3Qdcdjdk33oubYOsXg0NjGrAaq4')

# configure Watson NLU API
api_key = 'wLer7NnOejSljCZKyx-lFg1fccXoFgsBqQYKX7PRYkJG'
api_URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/3750a739-2688-44ea-a78d-5bcd3017d07a'
authenticator = IAMAuthenticator(api_key)
nlu = NLU(
    version='2020-08-01',
    authenticator=authenticator
)
nlu.set_service_url(api_URL)

untagged_path = 'C:/Users/Brynn/PycharmProjects/TwitterScraping/filtered_PermID.json'
tagged_path = 'C:/Users/Brynn/PycharmProjects/TwitterScraping/tagged_tweets_comb.json'

# parse json
obj_list = []
with open(untagged_path, encoding="utf8") as f:
    for jsonObj in f:
        data_dict = json.loads(jsonObj)
        obj_list.append(data_dict)

tweets = []
for obj in obj_list:
    tweets.append(obj["text"])

json_data = []


for tweet in tweets:
    # configure dictionary
    tagged_data = {}
    tagged_data["tweet"] = ""
    tagged_data["permID_tags"] = {"tags": defaultdict(list), "topics": defaultdict(list)}

    # configure/clean tweet to be tagged and save to tagged_data dict
    tweet = re.sub(r'[^a-zA-Z ]+', '', tweet)
    tagged_data["tweet"] = tweet

    # tag tweet with permID
    try:
        output, err = opid.calais(tweet, outputFormat = 'json')
        # load output into json_string
        json_string = json.loads(output)
    except Exception as ex:
        print("Exception: ", ex)

    # keeping track of how many categories and tags are present for each tweet for formatting
    cat_count = 1
    tag_count = 1
    # parse through tags
    for x in json_string:
        #print(x)

        if('SocialTag/' in x):
            tagged_data["permID_tags"]["tags"]["tag_"+str(cat_count)].append({"name":json_string[x]["name"], "importance": json_string[x]["importance"]})
            #print(json_string[x]["name"], json_string[x]["importance"])
            cat_count += 1
        if('cat/' in x):
            # append name and score of category to tagged_data dict
            tagged_data["permID_tags"]["topics"]["topic_"+str(tag_count)].append({"topic":json_string[x]["name"], "score":json_string[x]["score"]})
            #print(json_string[x]["name"], json_string[x]["score"])
            tag_count += 1 

    try:
        response = nlu.analyze(
                    text=tweet,
                    features = Features(categories = CategoriesOptions(limit=6))
                    ).get_result()
        #print(tweet)
        #print(json.dumps(response, indent=2))
        tagged_data["watson_tags"] = response
    except ApiException as ex:
        print("Method failed with status code", str(ex.code), ": ", ex.message)
    json_data.append(tagged_data)
    print(tagged_data)
with open(tagged_path, 'w') as out_path:
    json.dump(json_data, out_path, indent=4)