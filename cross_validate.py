from config import mailchimpKEY, mailchimpPrefix, audienceID
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import pymongo

DEBUG = True

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['circuitsortie']
PLEKJES = db['plekjes']
MATCHES = db['matches']
EMAILS = db['email']

mailchimp = Client()
mailchimp.set_config({
    "api_key": mailchimpKEY,
    "server": mailchimpPrefix
})

def db_to_chimp():
    """Retrieves all unique email addresses from both matches and plekjes from the database, compares them with mailchimp and adds new unique ones to mailchimp"""
    new_addresses = 0
    errors = 0

    all_emails = MATCHES.distinct('email') + PLEKJES.distinct('owner')
    unique_emails = set(all_emails)

    if DEBUG:
        print(f"Total amount of addresses: {len(all_emails)}")
        print(f"Unique amount of addresses: {len(unique_emails)}")

    for email in unique_emails:
        if email == "":
            continue

        res = mailchimp.searchMembers.search(email)

        if len(res['exact_matches']['members']) > 0:
            print(f"{email} is already in chimp")

            if len(res['exact_matches']['members']) > 1:
                print(f"{email} exists multiple times")
        else:
            user_details = PLEKJES.find_one({'owner': email})
            
            # Is user_details filled? No => there is no plekje for this email, search matches instead
            if not user_details:
                user_details = MATCHES.find_one({'email': email})
            
            # If there is no first and last name, ignore this row
            if not user_details['firstname'] == "" and not user_details['lastname'] == "":
                try:
                    mailchimp.lists.add_list_member(audienceID, {
                        "email_address": email,
                        "merge_fields": {
                            "FNAME": user_details['firstname'],
                            "LNAME": user_details['lastname'],
                        },
                        "status": "subscribed"
                    })

                    new_addresses += 1
                    print(f"Addded {email} to mailchimp")
                except ApiClientError as error:
                    print(f"ERROR: {email} throws error")
                    errors += 1
    
    print(f"Added {new_addresses} new subscribers to mailchimp")
    print(f"Encountered {errors} errors")


def chimp_to_db():
    """Retrieves all email addresses from mailchimp and compares them to the email database. Ignores duplicates and adds unknown ones to the database."""
    duplicates = 0
    new_addresses = 0

    for l in mailchimp.lists.get_all_lists()['lists']:
        for member in mailchimp.lists.get_list_members_info(l['id'], count=1000)['members']:
            user_email = EMAILS.find_one({'email': member['email_address']})

            if user_email:
                duplicates += 1
                continue

            EMAILS.insert_one({
                'email': member['email_address'],
                'first_name': member['merge_fields']['FNAME'],
                'last_name': member['merge_fields']['LNAME'],
                'tags': member['tags']
            })
            new_addresses += 1
        
    print(f"Encountered {duplicates} emails that were already stored")
    print(f"Wrote {new_addresses} new emails to the database")