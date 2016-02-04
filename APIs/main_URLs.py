from flask import Flask, jsonify, request
from uber_cost_estimate import comparer_address, comparer_coord
from wtforms import Form, TextAreaField, TextField, SubmitField
from gaussian_solver import matrix_class
from APIs import app

geo_api_key = "AIzaSyBp3NVaY0VMCDTx0L4ydgtjUOo6nTqOsy4"
uber_api_key = "GPUdmRVEn6wh81YKtelcX-nX18pLmJcmKpDIiiie"

"""
Address URL call:
http://localhost:5000/estimate/address/?f_addr=7740mccallumblvddallastexas&t_addr=planotexas

Coordinates URL call:
http://localhost:5000/estimate/coord/?f_lat=32.987922&f_long=-96.786982&t_lat=33.019843&t_long=-96.698886
"""

@app.route('/')
def home():
    index = '<p> 1) Uber Estimate - IPAddress/estimate/ </p>' \
            '<p> 2) </p>'
    return index

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


class matrix_form(Form):
    matrix_order = TextField("Matrix Order")
    text_area = TextAreaField("Enter")
    submit = SubmitField("Send")
"""
@app.route('/gaussian-solver/')
def gaussian_solver_form():

    html =
            <h1> Please paste matrix. </h1>
            <form action="." method="POST">
                <input type="text" name="text">
                <input type="submit" name="my-form" value="Send">
            </form>

    return html
"""
@app.route('/gaussian-solver/', methods=['GET', 'POST'])
def gaussian_solver_form_post():
    form = matrix_form(request.form)
    if request.method == 'POST':
        order = form.matrix_order
        text = form.text_area

        text_file = open("gaussian_file.txt", "w")
        text_file.write(text)
        text_file.close()

        matrix = matrix_class()
        if matrix.matrix_checker(order, 'gaussian_file.txt') == False:
            return "Enter proper values"
        else:
            return matrix.gaussian_solver(matrix.matrix_checker(order, 'gaussian_file.txt'), order)

    elif request.method == 'GET':
        return  """
                <form action="{{ url_for('gaussian-solver') }}" method=post>

				{{ form.matrix_order.label }}
				{{ form.matrix_order }}

				{{ form.text_area.label }}
				{{ form.text_area }}


				<span style="display:block; height: 30px;"></span>

				{{ form.submit }}

				</form>
                """






