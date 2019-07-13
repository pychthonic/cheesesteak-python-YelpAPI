from math import sqrt

from geopy.geocoders import Nominatim
import requests

import YelpAPI


class Cheesesteak:
    """User inputs address and how far they're willing to go. App
    returns a list of all places to get a cheesesteak within that area,
    along with reviews containing the word 'cheesesteak'.
    """
    def __init__(self):
        self.endpoint = "https://api.yelp.com/v3/businesses/search"
        self.get_api_verification()
        self.get_search_parameters()
        self.get_geocoordinates()
        self.headers = {'Authorization': 'bearer {}'.format(self.yelp_api_key)}
        self.parameters = {
                'term': 'cheesesteak',
                'limit': self.max_results,
                #'location': self.full_address,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'radius': self.radius,
                'location': self.city_state}
        response = requests.get(
            url=self.endpoint,
            params=self.parameters,
            headers=self.headers)
        response_data = response.json()
        print("full address: {}\n".format(self.full_address))
        for biz in response_data['businesses']:
            if biz['distance'] < self.radius:
                print("{}: {}\nDistance: {}\n\n".format(
                    biz['name'], biz['location']['address1'], biz['distance']))
        print(
            "Center point:\nLatitude: {}\nLongitude: {}\n".format(
            response_data["region"]["center"]["latitude"], 
            response_data["region"]["center"]["longitude"]))

    def get_search_parameters(self):
        """Get address from user and store it within instance variables.
        Find out how large an area will be searched.
        """
        self.street_number = input("Enter number and street for search: ")
        self.city = input("Enter city or town: ")
        self.state = input("What state is {} in? ".format(self.city))
        self.city_state = "{}, {}".format(self.city, self.state)
        self.full_address = "{} {}".format(self.street_number, self.city_state)
        self.distance = int(input(
            "How many blocks are you willing to travel for cheesesteak? "))
        self.distance *= 120
        self.radius = int(
            sqrt((self.distance // 2) ** 2 + (self.distance // 2) ** 2 )) + 1
        print("self.radius = {}".format(self.radius))
        self.max_results = int(input("Maximum number of results? "))

    def get_geocoordinates(self):
        """Use geopy module to determine coordinates of address to 
        anchor the search for cheesesteak.
        """
        self.geolocator = Nominatim(user_agent="philly_cheesesteak_finder")
        self.location = self.geolocator.geocode(self.full_address)
        print(self.location)
        print("Searching from {}".format(
              self.geolocator.reverse(
              "{}, {}".format(
              self.location.latitude, self.location.longitude)).address))
        print("Searching from {}\n".format(self.location.address))
        self.latitude = self.location.latitude
        self.longitude = self.location.longitude

    def get_api_verification(self):
        """Uses a module I wrote with two functions, one to get the API
        key, the other to get the client id, so that we can use the API.
        """
        self.yelp_api_key = YelpAPI.get_key()
        self.yelp_client_id = YelpAPI.get_client_id()

    def convert_meters_to_blocks(self, distance_meters):
        """Meter to block conversion method."""
        distance_blocks = distance_meters // 120
        return distance_blocks

if __name__ == "__main__":
    cheesesteak = Cheesesteak()
