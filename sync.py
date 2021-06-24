import pymongo
from config import mongoUrl

# Link with the database
client = pymongo.MongoClient(mongoUrl)
db = client['circuitsortie']
plekjes = db['plekjes']
matches = db['matches']


def get_cs_users():
    users = {}
    for plekje in plekjes.find({"owner": {"$exists": True}}):
        if plekje["owner"] not in users:
            users[plekje["owner"]] = {
                "firstname": plekje["firstname"],
                "lastname": plekje["lastname"],
                "tags": []
            }

    for match in matches.find({"email": {"$exists": True}}):
        if match["email"] not in users:
            users[match["email"]] = {
                "firstname": match["firstname"],
                "lastname": match["lastname"],
                "tags": []
            }

    for email in users:
        print(email, ':', users[email])
    return users


def main():
    get_cs_users()


if __name__ == '__main__':
    main()
    print('done!')
