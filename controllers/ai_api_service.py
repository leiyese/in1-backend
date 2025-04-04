# import openai
from google import genai
from google.genai.types import GenerateContentConfig
from huggingface_hub import InferenceClient
import os
import requests


class Aimodelfactory:
    @staticmethod
    def get_model(model_type):
        if model_type == "gpt-4":
            pass
            # return Openai_service()
        elif model_type == "huggingface":
            return Huggingface_service()
        elif model_type == "gemini":
            return Gemini_service()
        else:
            raise ValueError("Unsupported model type")


# class Openai_service:
#     def __init__(self, model="gpt-4"):
#         self.model = model
#         self.api_key = os.getenv("OPEN_AI_API_KEY")
#         openai.api_key = self.api_key

#     def generate_response(self, system, prompt):
#         try:
#             response = openai.ChatCompletion.create(
#                 model=self.model,
#                 message = [{"role": "system", "content": system},
#                            {"role": "user", "content": prompt}]
#             )
#             return response["choices"][0]["message"]["content"]
#         except Exception as e:
#             return {"error": str(e)}


class Gemini_service:
    def __init__(self, model="gemini-2.0-flash"):
        self.model = model
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)

    def generate_response(self, system, prompt):
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=GenerateContentConfig(
                    system_instruction=[system],
                    max_output_tokens=500,
                    temperature=0.1,
                    top_p=0.9,
                    top_k=40,
                ),
            )
            # for chunk in response:
            #     print(chunk.text, end="")
            return response.text

        except Exception as e:
            return {"error": str(e)}

        """
        self.client = genai.Client(api_key=self.api_key)
        self.chat = client.chats.create(model="gemini-2.0-flash")

        response = chat.send_message("I have 2 dogs in my house.")
        print(response.text)

        response = chat.send_message("How many paws are in my house?")
        print(response.text)

        for message in chat.get_history():
            print(f'role - {message.role}',end=": ")
            print(message.parts[0].text)

        https://ai.google.dev/gemini-api/docs/text-generation#python
        """


class Huggingface_service:
    def __init__(self, model="Qwen/Qwen2.5-Coder-32B-Instruct"):
        self.model = model
        self.api_key = os.getenv("HF_API_KEY")
        # self.api_url = "https://api-inference.huggingface.co/models/DeepSeek-R1"
        # self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.client = InferenceClient(provider="hf-inference", api_key=self.api_key)

    def generate_response(self, system, prompt):
        # try:
        #     response = requests.post(self.api_key, headers=self.headers, json=prompt)
        #     return response.json
        # except Exception as e:
        #     return {"error": str(e)}
        try:
            response = self.client.text_generation(model=self.model, prompt=prompt)
            print(response)
            return response
        except Exception as e:
            return {"error": str(e)}
