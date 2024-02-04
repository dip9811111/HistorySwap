import os
import requests
import uuid
import webbrowser
from openai import OpenAI
from general.predefined_strings import OPEN_AI_KEY, MAIN_DIR


def create_image(prompt_, number_of_images=1, boolReal=False):
    path_to_images = []
    image_urls = []

    if boolReal:

        client = OpenAI(api_key=OPEN_AI_KEY)
        random_code = str(uuid.uuid4())
        # Call the API
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_,
            size="1024x1024",  # "1024x1024",
            quality="standard",
            n=number_of_images,
        )

        os.makedirs(f"{MAIN_DIR}/GeneratedImages/{random_code}")

        for i in range(0, number_of_images):
            webbrowser.open(response.data[i].url)
            image_url = response.data[i].url
            image_data = requests.get(image_url).content
            path_to_image = (
                f"{MAIN_DIR}/GeneratedImages/{random_code}/{i}_generated_image.jpg"
            )
            path_to_images.append(path_to_image)
            image_urls.append(image_url)
            with open(path_to_image, "wb") as f:
                f.write(image_data)

    else:
        image_urls = []
        example_images = os.listdir(f"{MAIN_DIR}/Examples/Images")
        for exemple_im in example_images:
            path_to_images.append(f"{MAIN_DIR}/Examples/Images/{exemple_im}")

    return image_urls, path_to_images


# create_image("A cat riding a car on the moon", 3, True)
