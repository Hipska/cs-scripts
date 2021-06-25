from os import read
import pymongo
import csv

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['circuitsortie']
EMAILS = db['email']

with open('./testing/mails.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)

    # Ignore header
    next(reader)

    for row in reader:
        email = row[0]
        first_name = row[1]
        last_name = row[2]
        tags = row[13].split(', ')
        
        EMAILS.insert_one({
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'subscribed': True,
            'tags': tags
        })
