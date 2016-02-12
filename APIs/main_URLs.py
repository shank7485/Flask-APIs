from flask import Flask, jsonify, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from uber_cost_estimate import comparer_address, comparer_coord
from gaussian_solver import matrix_class

import os
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
    return render_template('index.html')

@app.route('/estimate/')
def estimate_home():
    return render_template('estimate.html')

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


UPLOAD_FOLDER = '\\Users\\Shashank\\PycharmProjects\\APIs_on_Heroku\\APIs\\files'
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
matrix_order = 0

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/gaussian-solver/', methods = ['GET', 'POST'])
def gaussian_solver():
    if request.method == 'GET':

        html = """
        <!doctype html>
        <title>Upload new File</title>

        <form action="" method=post enctype=multipart/form-data>
            <h1>Enter Matrix Order</h1>
            <p><input type=text name=text>
            <h1>Upload new File</h1>
            <p><input type=file name=file>
                <input type=submit value=Upload>
        </form>

        <p>%s</p>
        """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

        return html
    elif request.method == 'POST':
        file = request.files['file']
        matrix_order = int(request.form['text'])
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            main_file = filename.split('.')
            main_file[0] = 'info'
            main_file = main_file[0] + "." + main_file[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], main_file))
            obj = matrix_class()
            output = obj.gaussian_solver(matrix_order, obj.matrix_checker(matrix_order, '\\Users\\Shashank\\PycharmProjects\\APIs_on_Heroku\\APIs\\files\\info.txt'))
            return """
            <p> %s <p>
            """ % "".join(output)