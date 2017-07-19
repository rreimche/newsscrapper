# text file with headlines must be of format:
# [headline in plain text][one space[nickname/id for this headline]

import argparse
import csv

from requests.utils import quote

parser = argparse.ArgumentParser("Scrapper")
parser.add_argument("inputfile", help="Filename to parse for headlines", type=str)
parser.add_argument("outputfile", help="Filename to parse for headlines", type=str)
parser.add_argument("database", help="Database to save to", type=str)
parser.add_argument("--limit", help="Max number of tweets to scrap", type=int, default=10000, required=False)
args = parser.parse_args()

headlines = open(args.inputfile,"r")
jobs = open(args.outputfile,"w")

rows = csv.reader(headlines, delimiter=" ", quotechar="|")
for row in rows:
    news_id = row[1]
    encoded_query = quote(row[0])
    encoded_query += "%20since%3A2016-01-01%20until%3A2016-12-31"
    for i in range(3):
        job = "python scrapper.py " + args.database + " " + news_id + str(i) + " " + encoded_query + " " + str(args.limit) + "\n"
        jobs.write(job)

headlines.close()
jobs.close()
