# coding: utf-8

import os
import re
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import simplejson as json
import urllib
import base64
import uuid
from io import BytesIO
from PIL import Image
from mimetypes import guess_extension, guess_type

UPLOAD_FOLDER = 'images'
THUMBS_FOLDER = 'images/thumbs'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['THUMBS_FOLDER'] = THUMBS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_valid_url(filename: str) -> bool:
    try:
        urllib.request.urlopen(filename)
    except IOError:
        return False
    return True


def create_thumbnail(filepath):
    img = Image.open(filepath)
    img_resized = img.resize((100, 100))
    filename = get_random_filename() + '.' + filepath.rsplit('.', 1)[1].lower()
    img_resized.save(os.path.join(app.config['THUMBS_FOLDER'], filename))


def validate_filename(filename, content_type: str) -> int:
    if request.content_type == 'application/json':
        if is_base64(filename):
            return 201
        if is_valid_url(filename) and allowed_file(filename):
            return 201
        else:
            return 400
    else:
        if filename == '':
            return 400
        if allowed_file(filename.filename):
            return 201
        else:
            return 400


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def save_files(uploaded_files: list, content_type: str):
    filepath = ''
    if content_type.startswith('application/json'):
        for resource in uploaded_files:
            if is_valid_url(resource) and allowed_file(resource):
                filepath = save_from_url(resource)
            if is_base64(resource):
                filepath = save_base64(resource)
            create_thumbnail(filepath)
    else:
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            create_thumbnail(filepath)


def save_from_url(url: str) -> str:
    filename = re.search('.*/(.*)', url).group(1)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    urllib.request.urlretrieve(url, filepath)
    return filepath


def get_random_filename() -> str:
    return str(uuid.uuid4())


def save_base64(res: str) -> str:
    file_ext = guess_extension(guess_type(res)[0])
    filename = get_random_filename() + file_ext

    starter = res.find(',')
    image_data = res[starter + 1:]
    image_data = bytes(image_data, encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data)))
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    im.save(filepath)
    return filepath


def is_valid_content_type(content_type: str) -> bool:
    if content_type.startswith('application/json') or content_type.startswith('multipart/form-data'):
        return True

    return False


def is_base64(s: str) -> bool:
    starter = s.find(',')
    image_data = s[starter + 1:]
    image_data = bytes(image_data, encoding="ascii")
    try:
        return base64.b64encode(base64.b64decode(image_data)) == image_data
    except Exception:
        return False


@app.route('/upload', methods=['POST'])
def upload_file():
    if not is_valid_content_type(request.content_type):
        resp = jsonify({'message': 'Invalid content-type. Must be application/json or multipart/form-data.'})
        resp.status_code = 400
        return resp

    if request.content_type == 'application/json':
        try:
            uploaded_files = json.loads(request.data)
        except Exception as e:
            raise e
    else:
        uploaded_files = request.files.getlist("file")

    for filename in uploaded_files:
        status_code = validate_filename(filename, request.content_type)
        if status_code != 201:
            resp = jsonify({'message': 'Allowed file types are png, jpg, jpeg'})
            resp.status_code = status_code
            return resp

    save_files(uploaded_files, request.content_type)
    resp = jsonify({'message': 'File(s) successfully uploaded'})
    resp.status_code = 201

    return resp


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
