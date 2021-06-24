from config import mailchimpKEY, mailchimpPrefix, audienceID
from mailchimp_marketing import Client

mailchimp = Client()
mailchimp.set_config({
    "api_key": mailchimpKEY,
    "server": mailchimpPrefix
})

def get_tags(amount):
    """Returns all unique tags present in mailchimp
    
    Returns:
        tags(set):A set with all unique tags
    """
    tags = set()
    for l in mailchimp.lists.get_all_lists(count=1000)['lists']:
        for i in range(0, amount, 1000):
            for member in mailchimp.lists.get_list_members_info(l['id'], count=1000, offset=i, sort_field="timestamp_signup")['members']:              
                for tag in member['tags']:
                    tags.add(tag['name'])

    return tags

if __name__ == '__main__':
    print(get_tags(10000))