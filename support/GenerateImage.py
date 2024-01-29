import os
import requests
import uuid
import webbrowser
from dotenv import load_dotenv
from openai import OpenAI


def create_image(prompt_, number_of_images=1, boolReal=False):
    load_dotenv()
    main_dir = os.getenv("MAIN_DIR")
    path_to_images = []
    image_urls = []

    if boolReal:
        
        client = OpenAI(api_key=os.getenv("OPENAI_KEY"))  # Replace YOUR_API_KEY with your OpenAI API key
        random_code = str(uuid.uuid4())
        # Call the API
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt_,
            size="256x256",  # "1024x1024",
            quality="standard",
            n=number_of_images,
        )

        os.makedirs(f"{main_dir}/GeneratedImages/{random_code}")

        for i in range(0, number_of_images):
            webbrowser.open(response.data[i].url)
            image_url = response.data[i].url
            image_data = requests.get(image_url).content
            path_to_image = (
                f"{main_dir}/GeneratedImages/{random_code}/{i}_generated_image.jpg"
            )
            path_to_images.append(path_to_image)
            image_urls.append(image_url)
            with open(path_to_image, "wb") as f:
                f.write(image_data)

    else:
        image_urls = []
        example_images = os.listdir(f"{main_dir}/Examples/Images")
        for exemple_im in example_images:
            path_to_images.append(f"{main_dir}/Examples/Images/{exemple_im}")

    return image_urls, path_to_images


# create_image("A cat riding a car on the moon", 3, True)
