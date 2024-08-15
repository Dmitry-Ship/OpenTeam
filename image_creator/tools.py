from typing import Annotated
from urllib.parse import urlparse
import requests
from infra.art_generation import ArtGeneration
from dotenv import load_dotenv
import os
import replicate
import openai
from pydantic import BaseModel

load_dotenv()

def download_image(url) -> tuple[int, str]:
    # Parse the URL and extract the filename
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # If no filename could be extracted, provide a default one
    if not filename:
        filename = "default_image.jpg"
    
    # Send a GET request to the specified URL
    response = requests.get(url, stream=True)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open a file with the specified filename in binary-write mode
        with open("images/" + filename, 'wb') as file:
            # Write the contents of the response to the file
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return 0, f"Image saved as {filename}"
    else:
        return 1, print(f"Failed to retrieve the image. Status code: {response.status_code}")

class ArtGenerationTools:
    def __init__(self):
        self.art_generation = ArtGeneration(
            email=os.getenv("ART_GENERATION_EMAIL"),
            password=os.getenv("ART_GENERATION_PASSWORD"),
        )

        
    def generate_images(self, prompt: Annotated[str, "Prompt"]) -> list[str]:
        """
        Generate images using ArtGeneration
        """
        print("🖼 Generating images ...")
        status, images = self.art_generation.generate_images(prompt)
        if status == 1:
            print("❌ Generating image failed")
            return "failed to generate image"

        print("⬇️ Downloading images ...")
        for image_url in images:
            status, message = download_image(image_url['link'])
            if status == 1:
                print("❌ Downloading image failed", message)
                return "failed to download image"

        return images

class GenerateImages(BaseModel):
    prompt: str

generate_images_params = openai.pydantic_function_tool(GenerateImages, name="generate_images", description="Generate images")

def generate_images_flux(prompt):
    print("🖼 Generating images ...")

    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={
            "prompt": prompt,
        }
    )

    print("⬇️ Downloading images ...")
    
    for image_url in output:
        status, message = download_image(image_url)
        if status == 1:
            print("❌ Downloading image failed", message)
            return "failed to download image" 


    return output