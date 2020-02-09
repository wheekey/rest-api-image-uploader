import os
from dotenv import load_dotenv
load_dotenv()


UPLOAD_DIR = str(os.getenv("PROJECT_DIR")) + str(os.getenv("UPLOAD_DIR"))
THUMBS_DIR = str(os.getenv("PROJECT_DIR")) + str(os.getenv("THUMBS_DIR"))
TEST_IMGS_DIR = str(os.getenv("PROJECT_DIR")) + str(os.getenv("TEST_IMGS_DIR"))