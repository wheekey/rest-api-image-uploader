import os
import urllib.request

from werkzeug.datastructures import FileStorage

from app import app
from flask import Flask, request, redirect, jsonify, Response
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_requested_file(file: FileStorage) -> int:
    if file.filename == '':
        return 400
    if file and allowed_file(file.filename):
        return 201
    else:
        return 400


def save_file(file: FileStorage):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


def form_response(status_code: int) -> Response:
    if status_code == 400:
        resp = jsonify({'message': 'Allowed file types are png, jpg, jpeg'})
        resp.status_code = status_code


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_files = request.files.getlist("file")

    for file in uploaded_files:
        status_code = validate_requested_file(file)
        if status_code != 201:
            resp = jsonify({'message': 'Allowed file types are png, jpg, jpeg'})
            resp.status_code = status_code
            return resp

    for file in uploaded_files:
        save_file(file)

    resp = jsonify({'message': 'File(s) successfully uploaded'})
    resp.status_code = 201
    return resp


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
