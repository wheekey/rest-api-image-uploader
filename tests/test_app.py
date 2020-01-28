# coding: utf-8
import unittest
from app import app

from io import BytesIO, StringIO


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def test_upload(self):
        """ Test API can upload an image (POST request) """

        img1 = open('static/img1.jpg', 'rb')

        data = {
            'file': img1
        }
        rv = self.client.post('/upload', data=data)
        img1.close()
        assert rv.status_code == 201

    def test_multiple_upload(self):
        """ Test API can upload multiple files (POST request) """

        img1 = open('static/img1.jpg', 'rb')
        img2 = open('static/img2.jpg', 'rb')

        data = {
            'file': [img1, img2],
        }
        rv = self.client.post('/upload', data=data)
        assert rv.status_code == 201

    def test_accept_multipart_requests(self):
        """ Test API can accept multipart/form-data requests (POST request) """
        img1 = open('static/img1.jpg', 'rb')

        data = {
            'file': img1
        }
        rv = self.client.post('/upload', data=data, content_type='multipart/form-data')
        img1.close()
        assert rv.status_code == 201

    def test_accept_base64_upload(self):
        """ Test API can accept JSON requests with BASE64 encoded images. (POST request) """
        pass

    def test_upload_file_given_url(self):
        """ Test API can upload images at a given URL (image posted somewhere on the Internet). """
        pass

    def test_creates_square_image(self):
        """ Create a square image of 100 by 100 pixels. """
        pass
