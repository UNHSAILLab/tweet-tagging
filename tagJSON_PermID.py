import rdflib
import rdflib_jsonld
import json
import re
from collections import defaultdict
from OpenPermID import OpenPermID

opid = OpenPermID()
opid.set_access_token('MMusuM0Fh3Y55ce6iePuF7nYpSfRXC40')

untagged_path = 'C:/Users/Brynn/PycharmProjects/TwitterScraping/filtered_PermID.json'
tagged_path = 'C:/Users/Brynn/PycharmProjects/TwitterScraping/tagged_tweets_PermID.json'

obj_list = []

# parse json
with open(untagged_path, encoding="utf8") as f:
    for jsonObj in f:
        data_dict = json.loads(jsonObj)
        obj_list.append(data_dict)

tweets = []
for obj in obj_list:
    tweets.append(obj["text"])


"""
tagged_data = [] 
graph = rdflib.Graph()   
for x in range(5):
    
    tweet = tweets[x]
    tweet = re.sub(r'[^a-zA-Z ]+', '', tweet)
    try:
        output, err = opid.calais(tweet, outputFormat = 'rdf')
        graph.parse(data=output, format='application/rdf+xml')
        print(tweet)
        print(json.dumps(output, indent=2))
        
    except Exception as ex:
        print("Exception: ", ex)

    json_string = graph.serialize(format = 'json-ld')
    json_data = json.loads(json_string)
    tagged_data.append({"tweet":json_data, "tags": output})
with open(tagged_path, 'w') as out_path:
    json.dump(tagged_data, out_path, indent=4)

"""
json_data = {}
json_data["tag_results"] = []


for x in range(5):
    # configure dictionary
    tagged_data = {}
    tagged_data["tweet"] = ""
    tagged_data["permID_tags"] = {"tags": defaultdict(list), "topics": defaultdict(list)}
    # configure/clean tweet to be tagged and save to tagged_data dict
    tweet = tweets[x]
    tweet = re.sub(r'[^a-zA-Z ]+', '', tweet)
    tagged_data["tweet"] = tweet

    # tag tweet with permID
    try:
        output, err = opid.calais(tweet, outputFormat = 'json')
    except Exception as ex:
        print("Exception: ", ex)
    
    # load output into json_string
    json_string = json.loads(output)

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
    json_data["tag_results"].append(tagged_data)
with open(tagged_path, 'w') as out_path:
    json.dump(json_data, out_path, indent=4)


    
