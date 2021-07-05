from config import mailchimpKEY, mailchimpPrefix, audienceID, mongoUrl
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import pymongo

client = pymongo.MongoClient(mongoUrl)
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

def emails_to_chimp():
    """Gets all documents from the emails collection and checks if they are all present in Mailchimp."""
    all_emails = EMAILS.find()

    duplicate_addresses = 0
    new_addresses = 0
    errors = 0

    for email in all_emails:
        if email == "":
            continue
            
        res = mailchimp.searchMembers.search(email['email'])

        if len(res['exact_matches']['members']) > 0:
            if len(res['exact_matches']['members']) > 1:
                # theoretically impossible, mailchimp has duplicate prevention
                print(f"{email} exists multiple times")
            
            # User already exists in chimp, continue because they are not of interest
            duplicate_addresses += 1
            continue

        try:
  
            payload = {
                "email_address": email['email'],
                "merge_fields": {
                    "FNAME": email['first_name'],
                    "LNAME": email['last_name'],
                },
                "status": 'subscribed' if email['subscribed'] == True else 'unsubscribed',
                "tags": email['tags']
            }

            mailchimp.lists.add_list_member(audienceID, payload)

            new_addresses += 1
                
        except ApiClientError as error:
            print(f"ERROR: {email} throws error")
            errors += 1
        
    print(f"Encountered {new_addresses} new subscribers and added them to mailchimp")
    print(f"Encountered {duplicate_addresses} subscribers that were already in the database")
    print(f"Encountered {errors} errors")

    return {
        'new': new_addresses,
        'duplicate': duplicate_addresses,
        'errors': errors
    }

if __name__ == "__main__":
    emails_to_chimp()
        