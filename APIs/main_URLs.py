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
    html = """
    <h1>Welcome. The following are the APIs I have created. Go to each of them to know more. </h1>
    <p> 1) Uber address based cost estimate- <a href="https://shashankkumar.herokuapp.com/estimate/" target="_blank"> https://shashankkumar.herokuapp.com/estimate/</a></p>
    <p> 2) Gaussian NxN Matrix Solver - <a href="https://shashankkumar.herokuapp.com/gaussian-solver/" target="_blank"> https://shashankkumar.herokuapp.com/gaussian-solver/</a></p>
    <p> 3) More to come...
    """
    return html


@app.route('/estimate/')
def estimate_home():
    html = """
    <h2>Welcome to the Uber cost Estimate web service.</h2>
    <p>In this web service, you can estimate the cost of going from one address to another using Uber</p>
    <p>Works with coordinates also.</p>
    <p></p>
    <p>URL call format:</p>
    <p>Addresses: /estimate/address/?f_addr="From address"&t_addr="To address"</p>
    <p>Coordinates: /estimate/coord/?f_lat="From lat"&f_long="From long"&t_lat="To lat"&t_long="To long"</p>
    <p>Created by <b>Shashank Kumar Shankar</b>. For questions, Email me at: <b>shank7485@gmail.com</b></p>
    """
    return html


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

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
matrix_order = 0


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/gaussian-solver/', methods=['GET', 'POST'])
def gaussian_solver():
    if request.method == 'GET':

        html = """
        <!doctype html>
        <title>Gaussian solver</title>
        <h2>Gaussian NxN matrix equation Solver</h2>
        <p>This web service solves a mathematical NxN equation. Upload formatted text files by writing matrix elements in rows and columns.</p>
        <p>Created by <b>Shashank Kumar Shankar</b> with the help of <b><a href="https://www.linkedin.com/in/subramanian-nagarajan-28117223" target="_blank">Subramanian Nagarajan</a></b> from UTD.</p>
        <p>For questions, Email me at: <b>shank7485@gmail.com</b></p>
        
        <form action="" method=post enctype=multipart/form-data>
            <h1>Enter Matrix Order</h1>
            <p><input type=text name=text>
            <h1>Upload new File</h1>
            <p><input type=file name=file>
                <input type=submit value=Upload>
        </form>

        <p>%s</p>
        """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'], ))

        return html

    elif request.method == 'POST':
        file = request.files['file']
        matrix_order = int(request.form['text'])
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            main_file = filename.split('.')
            main_file = "info" + "." + main_file[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], main_file))
            obj = matrix_class()
            flag = obj.matrix_checker(matrix_order,
                                      '/tmp/info.txt')
            if flag != False:
                output = obj.gaussian_solver(flag)
                unknowns = str(output[0])
                results = str(output[1])
                return "<h1> Solution of the Matrix: </h1> \
                        <p> Unknowns on LHS Matrix: <p> \
                        <p> {} </p> \
                        <p> Results: <p> \
                        <p> {} </p> ".format(unknowns, results)
            else:
                return """
                <p> Please check input matrix file, there is an error. </p>
                <p> Check order, or see if all values are not zeros </p>.
                <a href="https://shashankkumar.herokuapp.com/gaussian-solver/"><b>BACK</b></a>
                """
