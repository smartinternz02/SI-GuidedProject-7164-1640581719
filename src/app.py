import os
from flask import Flask, request, render_template

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
model = load_model('model.h5')

def predict(img):
    x = image.img_to_array(img)
    x = x/255.0
    x = np.expand_dims(x,axis=0)
    proba = model.predict(x)[0][0]
    y = "Uninfected" if proba > 0.9 else "Parasitized"
    return y


@app.route("/")
def about():
	return render_template("about.html")

@app.route("/about")
def home():
	return render_template("about.html")

@app.route("/info")
def information():
	return render_template("info.html")

@app.route("/upload")
def test():
	return render_template("index6.html")

@app.route("/predict", methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		f = request.files['file']
		basepath = os.path.dirname('__file__')
		filepath = os.path.join(basepath, "uploads", f.filename)
		f.save(filepath)

		img = image.load_img(filepath, target_size=(64,64))
		
		result = predict(img)
		print(result)
		
		# x = image.img_to_array(img)
		# x = np.expand_dims(x, axis=0)

		# pred = model.predict(x)
		# print("prediction", pred)
		# if(pred == 1):
		# 	result = "Uninfected"
		# else:
		# 	result = "Infected"

		return result

if __name__ == "__main__":
	app.run(host='127.0.0.1', port=8080)
