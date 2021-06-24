from config import mailchimpKEY, mailchimpPrefix, audienceID
from mailchimp_marketing import Client
import pymongo
from datetime import datetime

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

def chimp_to_db():
    """Retrieves all email addresses from mailchimp and compares them to the email database. Ignores duplicates and adds unknown ones to the database."""
    duplicates = 0
    new_addresses = 0
    updated_addresses = 0

    for l in mailchimp.lists.get_all_lists()['lists']:
        for member in mailchimp.lists.get_list_members_info(l['id'], count=1000)['members']:
            user_email = EMAILS.find_one({'email': member['email_address']})

            if user_email:
                if user_email['first_name'] == member['merge_fields']['FNAME'] and user_email['last_name'] == member['merge_fields']['LNAME'] and user_email['tags'] == [tag['name'] for tag in member['tags']]:
                    # No fields were changed for this document, continue
                    duplicates += 1
                    continue

                payload = {
                    'first_name': member['merge_fields']['FNAME'],
                    'last_name': member['merge_fields']['LNAME'],
                    'tags': [tag['name'] for tag in member['tags']]
                }

                EMAILS.update_one({'email': member['email_address']}, {
                    '$set': payload
                })

                # Log this request for further audit
                AUDIT.insert_one({
                    'target': 'mongo',
                    'action': 'update',
                    'payload': payload,
                    'createdAt': datetime.now()
                })

                updated_addresses += 1
                continue

            payload = {
                'email': member['email_address'],
                'first_name': member['merge_fields']['FNAME'],
                'last_name': member['merge_fields']['LNAME'],
                'tags': [tag['name'] for tag in member['tags']]
            }

            EMAILS.insert_one(payload)

            # Log this request for further audit
            AUDIT.insert_one({
                'target': 'mongo',
                'action': 'insert',
                'payload': payload,
                'createdAt': datetime.now()
            })

            new_addresses += 1
        
    print(f"Encountered {duplicates} emails that were already stored and had no changes")
    print(f"Encountered {updated_addresses} emails that had changes, updated them")
    print(f"Encountered {new_addresses} new emails, added them")

if __name__ == '__main__':
    chimp_to_db()