from flask import Flask, render_template, request, redirect, url_for, send_from_directory

from werkzeug.utils import secure_filename
import os
import tensorflow as tf
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

app = Flask(__name__)

# Load the pre-trained model
model = tf.keras.models.load_model("generator_model.h5")


def convert_greyscale_to_color(image_path, model):
    image_size = 300
    img = Image.open(image_path).convert('L').resize((image_size, image_size))
    img_array = np.asarray(img).reshape((1, image_size, image_size, 1)) / 255
    colorized_image = model.predict(img_array)[0]
    # clip values to ensure they are in the 0..1 range
    colorized_image = np.clip(colorized_image, 0, 1)
    return colorized_image


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join("uploads", filename))
        colorized_image = convert_greyscale_to_color(
            os.path.join("uploads", filename), model)
        plt.imsave(os.path.join("static", "result.png"), colorized_image)
        return redirect(url_for("result"))
    return render_template("index.html")


@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/download_model")
def download_model():
    return send_from_directory(".", "generator_model.h5", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
