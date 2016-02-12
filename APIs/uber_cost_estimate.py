from uber_estimate import uber_estimate
from uber_geo_code import geo_location


class comparer_address:
    def __init__(self, from_address, to_address, geo_api_key, uber_api_key):
        self.from_address = from_address
        self.to_address = to_address
        self.geo_api_key = geo_api_key
        self.uber_api_key = uber_api_key

    def services_prices(self):
        geo = geo_location(self.geo_api_key)

        (from_lat, from_long) = geo.geo_locate(self.from_address)
        (to_lat, to_long) = geo.geo_locate(self.to_address)

        uber = uber_estimate(self.uber_api_key, from_lat, from_long, to_lat, to_long)

        prices = uber.estimate()["prices"]

        dct = {}
        for name in prices:
            dct.update({name["display_name"]: name["estimate"]})

        return dct


class comparer_coord:
    def __init__(self, from_lat, from_long, to_lat, to_long, uber_api_key):
        self.from_lat = from_lat
        self.from_long = from_long
        self.to_lat = to_lat
        self.to_long = to_long
        self.uber_api_key = uber_api_key

    def services_prices(self):
        uber = uber_estimate(self.uber_api_key, self.from_lat, self.from_long, self.to_lat, self.to_long)

        prices = uber.estimate()["prices"]

        dct = {}
        for name in prices:
            dct.update({name["display_name"]: name["estimate"]})

        return dct
