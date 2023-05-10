#!/usr/bin/env python3

from flask import Flask, abort, request, send_file, render_template, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import requests
import ipfshttpclient
import logging
import db
import traceback

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.py')

console = logging.StreamHandler()
root = logging.getLogger('')
root.addHandler(console)

db.__init__()


def download_url(url, hashcode):
    h = {"Accept-Encoding": "identity"}
    my_query = 'select file_name from file_info where cid =?'
    file_name = db.execute_query(my_query, hashcode)
    print(f'The download file name >> {file_name}')
    r = requests.get(url, stream=True, verify=False, headers=h)

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(traceback.format_exc())
        return "IPFS Server Error! \n", 503

    if "content-type" in r.headers:
        return send_file(r.raw, r.headers["content-type"], as_attachment=True, download_name=file_name)
    else:
        return send_file(r.raw)


@app.route('/upload_local', methods=['GET', 'POST'])
def upload_file_local():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


@app.route('/test', methods=['GET'])
def health_check():
    return 'App is UP and RUNNING'


@app.route('/', methods=['GET'])
@app.route('/', methods=['GET'])
def display_ui():
    return render_template('upload.html')


# Experimental to check how to download the file as attachment and to download with the same ext as uploaded
def download_ipfs(hashcode):
    client = ipfshttpclient.connect(app.config['IPFS_CONNECT_URL'])
    my_query = 'select file_name from file_info where cid =?'
    file_name = db.execute_query(my_query, hashcode)
    print(f'The file name >> {file_name}')
    # Download the file from IPFS
    stream = client.cat(hashcode)
    # Return the downloaded file as a Flask response with the correct filename and extension
    return send_file(stream, as_attachment=True, download_name=file_name)


@app.route("/download/<cid>", methods=['GET'])
def down(cid):
    try:
        p = os.path.splitext(cid)
        hashcode = str(p[0])

        if not hashcode or not hashcode.startswith('Qm'):
            return "Invalid CID provided", 404

        print("hashcode:{0}".format(hashcode), {'app': 'dfile-down-req'})

        url = app.config['IPFS_FILE_URL'] + hashcode
        return download_url(url, hashcode)
        # return download_ipfs(hashcode)
    except Exception as e:
        print(traceback.format_exc())
        return "Download Error! \n", 503


@app.route("/", methods=["POST", "PUT"])
@app.route("/upload_ipfs", methods=["POST", "PUT"])
def upload_file_ipfs():
    """
    This function will upload the file into ipfs
    :return: IPFS file URL
    """
    try:
        if "file" in request.files:
            file = request.files["file"]
            file_name = file.filename
            print("file name: {}".format(file_name))
            client = ipfshttpclient.connect(app.config['IPFS_CONNECT_URL'])
            res = client.add(file)

            print("upload res: {}".format(res))
            cid = str(res['Hash'])
            url = app.config['DOMAIN'] + '/' + cid
            db.insert(cid, file_name)
            return url
        abort(400)  # throw exception if the file attribute is not found in the request

    except Exception as e:
        print(traceback.format_exc())
        return "Upload Error! \n", 503


@app.route('/list_files', methods=['GET'])
def show_all_files():
    client = ipfshttpclient.connect(app.config['IPFS_CONNECT_URL'])

    objects = client.pin.ls(type='recursive')['Keys']

    # Create a list to store the file information
    files = []

    # Iterate over the objects and retrieve their information
    for obj in objects:
        file_info = client.object.stat(obj)
        files.append({'CID': obj, 'Size': file_info['CumulativeSize']})

    # Return the list of files as JSON
    return jsonify({'files': files})


if __name__ == "__main__":
    app.run(debug=True, port=5005, host="0.0.0.0")
    print("IPFS Controller  is running.")
