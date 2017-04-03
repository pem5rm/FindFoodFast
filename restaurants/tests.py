# from django.test import TestCase
#
# # Create your tests here.

import requests

def getToken():
    res = requests.request("POST", "https://api.yelp.com/oauth2/token",
                           data = "client_secret=d1jim4Jcc3fpxvfAQFxBrjRnsWLWxzD0kmP8cWnDh5rGyBbrLe8TtjqFZ5SAtBda&client_id=UhlMhAL5tgCRnkWD_Q67Vg&grant_type=client_credentials",
                           headers = {
        'content-type': 'application/x-www-form-urlencoded'}
    )

    token = res.json()['access_token']

    return token

def search(term, location):
    url = "https://api.yelp.com/v3/businesses/search/ "
    header = {
        "Authorization": "Bearer " + getToken(),
    }
    urlParams =  {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+')
    }
    res = requests.request("GET", "https://api.yelp.com/v3/businesses/search", headers = header, params = urlParams )
    return res.json()


retDict = search("dinner", "palmyra virginia")
restaurantNames = []
restaurantLocations = []
restaurantDict = {}
restaurantInfo = []
for key in retDict['businesses']:
    # r = Restaurant(name=key["name"], address=key["location"]["display_address"])
    # r.save()
    restaurantNames.append(key["name"])
    restaurantLocations.append(" ".join(key["location"]["display_address"]))
    restaurantDict[key["name"]] = key["name"] + " " + " ".join(key["location"]["display_address"])
for restaurant in restaurantDict:
    restaurantInfo.append(restaurantDict[restaurant])

print(restaurantInfo)
