import argparse

import datetime
import pymongo
import re

from bson import SON

parser = argparse.ArgumentParser("Scrapper")
parser.add_argument("database", help="Database", type=str)
args = parser.parse_args()

# connect to database
client = pymongo.MongoClient()
db = client[args.database]

collections = sorted([col for col in db.collection_names()])

# drop extra collections
for collection in collections:
    counts = dict()

    # get headline id
    headline_id = re.search('([a-zA-Z]+)', collection).group(0)

    # get number of tweets for every of 3 collections related to the same headline
    for i in range(3):
        counts[headline_id + str(i)] = db[headline_id + str(i)].count()

    # find out, which collection has maximum tweets
    the_one = (headline_id + str(0), counts[headline_id + str(0)])
    for i in [1,2]:
        if counts[headline_id + str(i)] >= the_one[1]:
            the_one = (headline_id+str(i), counts[headline_id+str(i)])

    # remove the maximum collection from this dictionary,
    # because it is a list of collections to drop
    del counts[the_one[0]]

    # drop collections and remove their names from "collections"
    for col in counts.keys():
        db[col].drop()
        if col in collections:
            collections.remove(col)

    #db.command('db.' + the_one[0] + '.renameCollection("' +  + '")')
    #client.admin.command(SON([("renameCollection",args.database + "." + the_one[0]),\
    #                         ("to",args.database + "." + the_one[0][:-1])]))
    #db[the_one[0]].renameCollection(the_one[0][:-1])