import requests

class uber_estimate:
    """
    Uber API key is server_token.
    Rest are latities and longitudes
    """
    def __init__(self, server_token, start_lat, start_long, end_lat, end_long):
        self.server_token = server_token
        self.start_lat = start_lat
        self.start_long = start_long
        self.end_lat = end_lat
        self.end_long = end_long

    def estimate(self):
        url = "https://api.uber.com/v1/estimates/price"

        parameters = {
            'server_token' : self.server_token,
            'start_latitude' : float(self.start_lat),
            'start_longitude' : float(self.start_long),
            'end_latitude' : float(self.end_lat),
            'end_longitude' : float(self.end_long)
        }

        response = requests.get(url, params=parameters)
        data = response.json()
        return data
