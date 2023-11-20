import os
import requests
import concurrent.futures

access_key = "6ehPELpkYx0Zkzu5dluwhe7c2vrBYbj9i5K6T8tFV5g"
query = "architecture"
count = 2500
page = 1
concurrency = 10

# create a folder named "Pictures" if it doesn't already exist
if not os.path.exists("Pictures"):
    os.mkdir("Pictures")

# function to download an image and save it to a file


def download_image(url, filename):
    filepath = os.path.join("Pictures", filename)
    with open(filepath, "wb") as f:
        print("Creatting file", filename)
        f.write(requests.get(url).content)


# loop through the pages of results and download each image
with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
    while count > 0:
        # make a request to the Unsplash API to get the images
        response = requests.get(
            f"https://api.unsplash.com/search/photos/?query={query}&per_page=30&page={page}&client_id={access_key}")

        # create a list of tasks to download the images
        tasks = []
        for i, photo in enumerate(response.json()["results"]):
            if count == 0:
                break
            url = photo["urls"]["regular"]
            filename = f"Image-{page*30-i}.jpg"
            tasks.append(executor.submit(download_image, url, filename))
            count -= 1

        # wait for all tasks to complete
        concurrent.futures.wait(tasks)

        # increment the page number for the next request
        page += 1
