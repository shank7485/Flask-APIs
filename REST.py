from flask import Flask, jsonify, request
from comparer import comparer_address, comparer_coord

app = Flask(__name__)

geo_api_key =  #Enter your Google Maps API Key
uber_api_key =  #Enter your Uber API Key
"""
Address URL call:
http://localhost:5000/estimate/address/?f_addr=7740mccallumblvddallastexas&t_addr=planotexas

Coordinates URL call:
http://localhost:5000/estimate/coord/?f_lat=32.987922&f_long=-96.786982&t_lat=33.019843&t_long=-96.698886
"""
@app.route('/estimate/')
def estimate_home():
    index = '<h2>Welcome to the Uber cost Estimate web service app.</h2>' \
            '<p>URL call format:</p>' \
            '<p>Addresses: /estimate/address/?f_addr="From address"&t_addr="To address"</p>' \
            '<p>Coordinates: /estimate/coord/?f_lat="From lat"&f_long="From long"&t_lat="To lat"&t_long="To long"</p>' \
            '<p>Created by <b>Shashank Kumar Shankar</b>. For questions, Email me at: <b>shank7485@gmail.com</b></p>'
    return index

@app.route('/estimate/address/')
def estimate_address():
    from_address = request.args.get('f_addr')
    to_address = request.args.get('t_addr')

    comp = comparer_address(from_address, to_address, geo_api_key, uber_api_key)
    return jsonify(comp.services_prices())

@app.route('/estimate/coord/')
def estimate_coord():
    from_latitude = request.args.get('f_lat')
    from_longitude = request.args.get('f_long')
    to_latitude = request.args.get('t_lat')
    to_longitude = request.args.get('t_long')

    comp = comparer_coord(from_latitude, from_longitude, to_latitude, to_longitude, uber_api_key)
    return jsonify(comp.services_prices())

if __name__ == "__main__":
    app.run(debug=True)
