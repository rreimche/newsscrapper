import sys
import argparse
import pymongo
from pymongo.errors import InvalidName
from twitterscraper import query_tweets


# parse command line arguments
parser = argparse.ArgumentParser("Scrapper")
parser.add_argument("database", help="Database to save to", type=str)
parser.add_argument("collection", help="Collection to save to", type=str)
parser.add_argument("query", help="Query", type=str)
parser.add_argument("limit", help="Limit of tweets to download", type=int, default=None)
args = parser.parse_args()

# if args.limit == "":
#     limit = None
# else:
#     limit = args.limit

# connect to database
client = pymongo.MongoClient()
db = client[args.database]
collection = db[args.collection]

# get tweets
for tweet in query_tweets(args.query, args.limit):
    t = {
        "_id" : tweet.id,
        "timestamp" : tweet.timestamp,
        "user" : tweet.user,
        "fullname" : tweet.fullname,
        "text" : tweet.text
    }

    collection.insert_one(t)