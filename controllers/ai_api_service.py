import openai
import google.generativeai as genai
import os
from flask import requests


class Aimodelfactory:
    @staticmethod
    def get_model(model_type):
        if model_type == "gpt-4":
            return Openai_service()
        elif model_type == "huggingface":
            return Huggingface_service()
        elif model_type == "gemini":
            return Gemini_service()
        else:
            raise ValueError("Unsupported model type")
class Openai_service:
    def __init__(self, model="gpt-4"):
        self.model = model
        self.api_key = os.getenv("OPEN_AI_API_KEY")
        openai.api_key = self.api_key

    def generate_response(self, system, prompt):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                message = [{"role": "system", "content": system},
                           {"role": "user", "content": prompt}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return {"error": str(e)}
        
class Gemini_service:
    def __init__(self, model="gemini"):
        self.model = model
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)

    def generate_response(self, system, prompt):
        try:
            response = self.model.generate_content(
                [system, prompt],
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=500,
                    top_p=0.9,
                    top_k=40
                )
            )
            return response.txt
        except Exception as e:
            return("error": str(e))

class Huggingface_service:
    def __init__(self, model="huggingface"):
        self.model = model
        self.api_key = os.getenv("HF_API_KEY")
        self.headers = {"Authorization": f"Bearer YOU_HF_API_KEY"}
    
    def generate_response(self, system, prompt):
        try:
            response = requests.post(self.api_key, headers=self.headers, json=prompt )
            return response.json
        except Exception as e:
            return("error": str(e))
