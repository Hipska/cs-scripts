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

def keep():
    for l in mailchimp.lists.get_all_lists()['lists']:
        print("> found list:",  l["name"])
        print('members:')
        for member in mailchimp.lists.get_list_members_info(l['id'])['members']:
            print(member['email_address'],
                member['full_name'], member['tags'])


def cross_validate_db_to_chimp():
    new_addresses = 0
    errors = 0

    all_emails = MATCHES.distinct('email') + PLEKJES.distinct('owner')
    unique_emails = set(all_emails)

    if DEBUG:
        print(f"Total amount of addresses: {len(all_emails)}")
        print(f"Unique amount of addresses: {len(unique_emails)}")

    for email in unique_emails:
        if not email == "":
            res = mailchimp.searchMembers.search(email)

            if len(res['exact_matches']['members']) > 0:
                print(f"{email} is already in chimp")
                if len(res['exact_matches']['members']) > 1:
                    print(f"{email} exists multiple times")
            else:
                user_details = PLEKJES.find_one({'owner': email})
                
                if not user_details:
                    user_details = MATCHES.find_one({'email': email})
                
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

def get_mailchimp_tags():
    tags = set()

    for l in mailchimp.lists.get_all_lists()['lists']:
        for member in mailchimp.lists.get_list_members_info(l['id'], count=1000)['members']:
            for tag in member['tags']:
                tags.add(tag['name'])

    return tags

print(get_mailchimp_tags())