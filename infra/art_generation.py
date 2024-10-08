from typing import Annotated
import requests
import time

class ArtGeneration:
    def __init__(self, email: str, password: str, model_id=137):
        self.url_base = 'https://api-gateway.artgeneration.me/api'
        self.email = email
        self.password = password
        self.base_data = {
            "model_id": model_id,
            "width": 1216,
            "height": 832,
            "is_private": True,
            "num_inference_steps": 41,
            "guidance_scale": 5,
            "scheduler_id": "4d04b1ec-1ec7-4a04-b8c4-7683f55df775",
            "self_attention": False,
            "clip_skip": 1,
            "highres_fix": False,
            "sharpness": 2,
            "samples": 1
        } 

        self.user_id = None
        result = self.authenticate()
    
    def authenticate(self):
        auth_url = f"{self.url_base}/v1/user/auth"
        auth_data = {
            "email": self.email,
            "password": self.password
        }
        print("Authenticating into ArtGeneration...")
        response = requests.post(auth_url, json=auth_data).json()
        if "data" in response:
            self.base_data["token"] = response["data"]["token"]
            self.user_id = response["data"]["id"]
            print("Authentication Successful")
            return True, "Authentication Successful"
        else:
            print("Authentication Failed")
            return False, "Authentication Failed"
    def send_request(self, prompt):
        data = self.base_data.copy()
        data["prompt"] = prompt
        response = requests.post(f"{self.url_base}/v1/image/init", json=data)

        return response.json()

    def fetch_generation_list(self):
        params = {
            'user_id': self.user_id,
            'subscription_type': 'premium',
        }
        response = requests.get(f"{self.url_base}/v1/image/fetch/", params=params)
        return response.json()

    def generate_images(self, prompt: Annotated[str, "Prompt"]) -> Annotated[tuple[int, list[str]], "Status code and message"]:
        request_response = self.send_request(prompt)
        print("Response: ", request_response)

        generation_id = request_response["data"]["generation_id"]

        start_time = time.time()
        timeout = 120  # seconds

        time.sleep(30) 
        while time.time() - start_time < timeout:
            time.sleep(10)  # Wait for 5 seconds before checking again
            generation_list_response = self.fetch_generation_list()

            generation_list = generation_list_response["data"]["generation_list"]

            for generation in generation_list:
                if generation["id"] == generation_id and "image_list" in generation:
                    if len(generation["image_list"]) > 0:
                        return 0, generation["image_list"]
        return 1, "Error: Image generation timed out or not found."

