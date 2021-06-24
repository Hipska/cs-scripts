from config import mailchimpKEY, mailchimpPrefix, audienceID
from mailchimp_marketing import Client

mailchimp = Client()
mailchimp.set_config({
    "api_key": mailchimpKEY,
    "server": mailchimpPrefix
})

def get_tags():
    """Returns all unique tags present in mailchimp
    
    Returns:
        tags(set):A set with all unique tags
    """
    tags = set()

    for l in mailchimp.lists.get_all_lists()['lists']:
        for member in mailchimp.lists.get_list_members_info(l['id'], count=1000)['members']:
            for tag in member['tags']:
                tags.add(tag['name'])

    return tags


if __name__ == '__main__':
    print(get_tags())