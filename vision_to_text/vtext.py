import io
import os

# Imports the Google Cloud client library
from google.cloud import vision

# Instantiates a client
vision_client = vision.Client()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),'sign.png')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()
    image = vision_client.image(
    content=content)

#performs text detection
texts = image.detect_text()

#outputs the language code
print texts[0].locale

#outputs the detected text
print texts[0].description