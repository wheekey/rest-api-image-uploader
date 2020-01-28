# coding: utf-8

import os
from werkzeug.datastructures import FileStorage
from flask import Flask, request, redirect, jsonify, Response
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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


def is_valid_content_type(content_type: str) -> bool:
    if content_type.startswith('application/json') or content_type.startswith('multipart/form_data'):
        return True

    return False


@app.route('/upload', methods=['POST'])
def upload_file():
    if not is_valid_content_type(request.content_type):
        resp = jsonify({'message': 'Invalid content-type. Must be application/json or multipart/form-data.'})
        resp.status_code = 400
        return resp

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
