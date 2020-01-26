import unittest


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = self.app.test_client

    def test_upload(self):
        """ Test API can upload an image (POST request) """
        pass

    def test_multiple_upload(self):
        """ Test API can upload multiple files (POST request) """
        pass

    def test_accept_multipart_requests(self):
        """ Test API can accept multipart/form-data requests (POST request) """
        pass

    def test_accept_base64_upload(self):
        """ Test API can accept JSON requests with BASE64 encoded images. (POST request) """
        pass

    def test_upload_file_given_url(self):
        """ Test API can upload images at a given URL (image posted somewhere on the Internet). """
        pass

    def test_creates_square_image(self):
        """ Create a square image of 100 by 100 pixels. """
        pass
