from flask import Flask, render_template, request, render_template, redirect
import PIL as PIL
from PIL import Image
import base64
from io import BytesIO
from image_encoder.image_encoder import *


###########################################
#           define flask app
###########################################
app = Flask(__name__)


###########################################
# resize image to 50% of width keep aspect
#                 ratio.
###########################################
# route = localhost/image/response
# request method = POST
# @param = string of base64 encoded image
# @response = base64 encoded string of
#             resized image.
###########################################
@app.route("/image/response", methods=['GET', 'POST'])
def image():

    try:
        base64_image = request.form["base64_image"].split(',')[1]
        image = Image.open(BytesIO(base64.b64decode(base64_image)))
    except:
        return render_template('error.html')

    ###########################################
    # calculate by how much % image is resized
    #               width wise.
    ###########################################
    w_size = (image.size[0] // 2) + image.size[0]
    w_percent = w_size / float(image.size[0])

    ###########################################
    # calculate new height to keep aspect ratio
    ###########################################
    h_size = int((float(image.size[1]) * float(w_percent)))

    ###########################################
    # resize image with new width and height
    #               and save
    ###########################################
    image = image.resize(
        (((image.size[0] // 2) + image.size[0]), h_size), PIL.Image.ANTIALIAS)
    image.save('image.jpg', 'JPEG')

    ###########################################
    # serialize image by encoding it and send
    #       response to endpoint
    ###########################################
    to_send = encode('image.jpg')
    return to_send


###########################################
# render form index.html on hitting request
###########################################
# route = localhost/image
# request method = GET
# @param = None
# @response = rendered form
###########################################
@app.route("/image", methods=['GET'])
def home():

    return render_template('index.html')


###########################################
# render error.html on hitting exception
###########################################
# route = localhost/error
# request method = GET
# @param = None
# @response = None
###########################################
@app.route("/error", methods=['GET'])
def error():

    return render_template('index.html')


###########################################
#          run the flask app
###########################################
app.run()
