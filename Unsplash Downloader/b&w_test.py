from PIL import Image
import os

# Set the directory path
directory = "Pictures/"

# Loop through all the files in the directory
for filename in os.listdir(directory):
    # Check if the file is an image
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Get the full path of the image
        image_path = os.path.join(directory, filename)
        image = Image.open(image_path)  # Open the image with Pillow

        # Check if the image is monochrome (black and white)
        if image.mode == '1' or image.mode == 'L':
            print(filename + " is a monochrome image")
