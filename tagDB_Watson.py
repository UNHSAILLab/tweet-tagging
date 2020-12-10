
import pymongo
from pymongo import MongoClient
#from watson_developer_cloud import NaturalLanguageUnderstandingV1
#from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_watson import NaturalLanguageUnderstandingV1 as NLU
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions
from sshtunnel import SSHTunnelForwarder


api_key = ''
api_URL = 'https://api'
authenticator = IAMAuthenticator(api_key)
natural_language_understanding = NLU(
    version='2020-08-01',
    authenticator=authenticator
)
nlu = natural_language_understanding.set_service_url(api_URL)


MONGO_HOST = "138.68.245.43"
MONGO_DB = "preTwittAnnotate"
MONGO_USER = "abose20"
MONGO_PASS = "threatIntel20"

# Configure connection
server = SSHTunnelForwarder(
    MONGO_HOST,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASS,
    remote_bind_address=('127.0.0.1', 27017)
)
server.start()
connection=pymongo.MongoClient("138.68.245.43")
print("line 23")

#db = connection.filteredTwittCrawl
#filterd_kwTweets_Collection = db.filter_kw_tweets

db = connection.filteredTwittCrawl
tweet_collection = db.filter_kw_tweets
cursor = tweet_collection.find()

for doc in cursor:
    print (doc)

#cursor.toArray()


""" for doc in cursor:
    courpus = doc['tweet']['text']
    corpus=unicodedata.normalize('NFKD', corpus).encode('ascii','ignore')
    corpus=corpus.decode("utf-8")

    for data in corpus: #assuming data is the raw text
        response = nlu.analyze(
            text=data,
            features = Features(categories = CategoriesOptions(limit=4))
        ).get_result()
        print(json.dumps(response, indent=2))
     """






