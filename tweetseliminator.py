import argparse
import pymongo

parser = argparse.ArgumentParser("Scrapper")
parser.add_argument("database", help="Database", type=str)
args = parser.parse_args()

# connect to database
client = pymongo.MongoClient()
db = client[args.database]

#collections = sorted([col for col in db.collection_names()])

collections = ['test']

# some testing
for i in range(10):
    db['test'].add_one({
        "user":"user1",
        "_id": i
        "timestamp": datetime.datetime(now) # now + i days
    })

for collection in collections:
    # gather users
    users = set([uname.user for uname in db[collection].find({},{"user":1})])

    for user in users:
        # gather tweets
        tweets = list(db[collection].find({"user": user},{"_id":1}).sort("timestamp", pymongo.ASCENDING))
        for tweet in tweets[1:]:
            # delete all tweets of this user that
            db[collection].delete_one({"_id": tweet._id})

# TODO: seed data
# TODO