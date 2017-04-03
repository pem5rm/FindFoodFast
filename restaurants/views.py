from django.views import generic
import requests
import urllib.request
from django.http import HttpRequest
import json
from geopy.distance import great_circle

class IndexView(generic.ListView):
    template_name = 'restaurants/index.html'
    context_object_name = 'list'
    def get_queryset(self):
        ret = []
        return ret

    def get_context_data(self, **kwargs):
        request =self.request
        user_ip = str(request.META.get('HTTP_X_REAL_IP'))
        context = super(IndexView, self).get_context_data(**kwargs)
        try:
            location_site = urllib.request.urlopen("http://freegeoip.net/json/" + user_ip)
            location_str = ""
            for line in location_site:
                location_str += line.strip().decode("UTF-8")

            location_dict = json.loads(location_str)
            city = location_dict['city']
            state = location_dict['region_name']
            myLatitude = location_dict["latitude"]
            myLongitude = location_dict["longitude"]

            myLocation = (myLatitude, myLongitude)
            retDict = search("dinner", state + " " + city)
        except:
            retDict = {}

        restaurantDict = {}
        restaurantInfo = []
        try:
            for key in retDict['businesses']:
                if not key["is_closed"]:
                    restaurantLocation = (key["coordinates"]["latitude"], key["coordinates"]["longitude"])
                    distance = great_circle(myLocation,restaurantLocation).miles
                    type = ""
                    for word in key["categories"]:
                        type += word["title"] + ",  "
                    restaurantDict[key["name"]] = [str(float("{0:.2f}".format(distance))) + " miles away: " + \
                                                "  " + key["name"] +\
                                                   "\nType:  " + type +\
                                                  "\nAddress:  " + " ".join(key["location"]["display_address"])+\
                                                   "\nPhone:  " + key["display_phone"]+\
                                                   "\nPrice:  " + key["price"]+\
                                                    "\nRating:  " + (str(key["rating"])),
                                                   key["url"], "https://www.google.com/maps/dir/" + str(myLatitude) + "," + str(myLongitude) + "/" + str(key["coordinates"]["latitude"]) + "," + str(key["coordinates"]["longitude"])]

            for restaurant in restaurantDict:
                restaurantInfo.append(restaurantDict[restaurant])

            if restaurantInfo == []:
                restaurantInfo = None
        except:
            restaurantInfo = None
        if restaurantInfo != None:
            context['restaurant_info'] = sorted(restaurantInfo)

        return context


# Yelp Functions

def getToken():
    res = requests.request("POST", "https://api.yelp.com/oauth2/token",
                           data = "client_secret=d1jim4Jcc3fpxvfAQFxBrjRnsWLWxzD0kmP8cWnDh5rGyBbrLe8TtjqFZ5SAtBda&client_id=UhlMhAL5tgCRnkWD_Q67Vg&grant_type=client_credentials",
                           headers = {
        'content-type': 'application/x-www-form-urlencoded'}
    )

    token = res.json()['access_token']

    return token

def search(term, location):
    header = {
        "Authorization": "Bearer " + getToken(),
    }
    urlParams =  {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit' : 40,
    }
    res = requests.request("GET", "https://api.yelp.com/v3/businesses/search", headers = header, params = urlParams )
    return res.json()
