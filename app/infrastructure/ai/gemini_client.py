from google import genai
from google.genai import types

from app.core.config import GEMINI_API_KEY


class GeminiClient:

    def __init__(self, system_prompt: str):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.system_prompt = system_prompt


    def generate(self, contents):

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=0.9,
                max_output_tokens=600,
            )
        )

        return response.text.strip()