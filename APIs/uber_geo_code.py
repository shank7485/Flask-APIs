import requests

class geo_location:
    "API_key is Google Maps API key"
    def __init__(self, API_key):
        self.API_key = API_key

    def geo_locate(self, address):
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&key" + str(self.API_key)

        response = requests.get(url)
        data = response.json()["results"][0]["geometry"]

        coodinates = data["location"]

        lat = coodinates["lat"]
        long = coodinates["lng"]

        return (lat,long)

