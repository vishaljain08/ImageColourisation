import os
import random
import numpy as np
import tensorflow as tf
from PIL import Image
from matplotlib import pyplot as plt

# Load the generator model
generator = tf.keras.models.load_model('../FrontEnd/generator_model.h5')


def convert_to_bw(img):
    return img.convert('L')


# Set the directories
image_directory = "Pictures/"
bw_image_directory = "BWImages/"
colorized_image_directory = "Colorized/"

# Create the output directories if they don't exist
os.makedirs(bw_image_directory, exist_ok=True)
os.makedirs(colorized_image_directory, exist_ok=True)

# Get a list of all images in the folder
all_images = [img for img in os.listdir(
    image_directory) if img.endswith(('.jpg', '.jpeg', '.png'))]

# Select 50 random images
random_images = random.sample(all_images, 50)

for img_name in random_images:
    # Load the image
    img = Image.open(os.path.join(image_directory, img_name))

    # Convert the image to black and white
    bw_img = convert_to_bw(img)

    # Save the black and white image
    bw_img.save(os.path.join(bw_image_directory, img_name))

    # Resize the black and white image
    bw_img_resized = bw_img.resize((300, 300))

    # Convert the image to an array
    bw_img_array = (np.asarray(bw_img_resized).reshape((300, 300, 1))) / 255

    # Expand the dimensions to match the input shape of the generator
    bw_img_array_expanded = np.expand_dims(bw_img_array, axis=0)

    # Use the generator model to colorize the black and white image
    colorized_img_array = generator.predict(bw_img_array_expanded)
    colorized_img_array = np.clip(colorized_img_array, 0, 1)

    # Convert the colorized image array to a PIL image
    colorized_img = Image.fromarray(
        (colorized_img_array[0] * 255).astype(np.uint8))

    # Save the colorized image
    colorized_img.save(os.path.join(colorized_image_directory, img_name))
