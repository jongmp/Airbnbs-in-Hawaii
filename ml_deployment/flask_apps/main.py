import base64
import numpy as np
import io
from PIL import Image
'''
import os
os.environ['KERAS_BACKEND'] = 'theano'
'''

import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import request
from flask import jsonify
from flask import Flask
import json
from flask import render_template
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


app = Flask(__name__)

def get_model():
    global model
    model = load_model('model_keras.h5')
    print(" * Model Loaded!")

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    return image

print(" * Loading Keras model...")
get_model()

@app.route("/predict", methods=["GET","POST"])
def predict():
    if request.method == "POST":
        message = request.get_json(force=True)
        encoded = message['image']
        decoded = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(decoded))
        processed_image = preprocess_image(image, target_size=(150,150))

        prediction = model.predict(processed_image)
        print(prediction)
        response = prediction[0][0]
        print(response)
        if response == 1.0:
            response = 'This picture is likely to succeed'
        else:
            response = "This picture is not likely to succeed"
        return json.dumps(str(response))
    else:
        return render_template('predict.html')

if __name__ == "__main__":
    #decide what port to run the app in
    port = int(os.environ.get('PORT', 5000))
    #run the app locally on the givn port
    app.run(host='0.0.0.0', port=port)
    #optional if we want to run in debugging mode
    #app.run(debug=True)

'''
# Get the image from my computer to test
img = Image.open('/Users/jpar746/Desktop/5065.0nots.png')
predict(img)
'''

