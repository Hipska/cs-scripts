from config import mailchimpKEY, mailchimpPrefix, audienceID
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import pymongo
import csv

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['circuitsortie']
PLEKJES = db['plekjes']
MATCHES = db['matches']
EMAILS = db['email']
AUDIT = db['audit']

mailchimp = Client()
mailchimp.set_config({
    "api_key": mailchimpKEY,
    "server": mailchimpPrefix
})

chimp_emails = set()
csv_emails = set()

with open('mails.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        csv_emails.add(row[0])

for l in mailchimp.lists.get_all_lists(count=1000)['lists']:
    for i in range(0, 10000, 1000):
        for member in mailchimp.lists.get_list_members_info(l['id'], count=1000, offset=i)['members']:
            chimp_emails.add(member['email_address'])

print(len(chimp_emails - csv_emails))
print(chimp_emails - csv_emails)

with open('result.csv', 'w') as writefile:
    writer = csv.writer(writefile)

    for row in csv_emails - chimp_emails:
        writer.writerow(row)