from config import mailchimpKEY, mailchimpPrefix
from mailchimp_marketing import Client

mailchimp = Client()
mailchimp.set_config({
    "api_key": mailchimpKEY,
    "server": mailchimpPrefix
})

for l in mailchimp.lists.get_all_lists()['lists']:
    print("> found list:",  l["name"])
    print('members:')
    for member in mailchimp.lists.get_list_members_info(l['id'])['members']:
        print(member['email_address'],
              member['full_name'], member['tags'])
