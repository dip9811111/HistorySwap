import os
import requests
import uuid
import webbrowser
from dotenv import load_dotenv
from openai import OpenAI


def create_image(prompt_, number_of_images=1, boolReal=False):   
    if boolReal:
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_KEY"))  # Replace YOUR_API_KEY with your OpenAI API key
        main_dir = os.getenv("MAIN_DIR")
        random_code = str(uuid.uuid4())
        # Call the API
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt_,
            size="256x256",  # "1024x1024",
            quality="standard",
            n=number_of_images,
        )

        path_to_images = []
        image_urls = []

        os.makedirs(f"{main_dir}/{random_code}")

        for i in range(0, number_of_images):
            webbrowser.open(response.data[i].url)
            image_url = response.data[i].url
            image_data = requests.get(image_url).content
            path_to_image = (
                f"{main_dir}/{random_code}/{i}_generated_image.jpg"
            )
            path_to_images.append(path_to_image)
            image_urls.append(image_url)
            with open(path_to_image, "wb") as f:
                f.write(image_data)

        return image_urls, path_to_images

    else:
        path_to_image = (
            "C:/Users/lucad/OneDrive/Desktop/HistorySwap/generated_image.jpg"
        )
        return "ok", path_to_image


# create_image("A cat riding a car on the moon", 3, True)
