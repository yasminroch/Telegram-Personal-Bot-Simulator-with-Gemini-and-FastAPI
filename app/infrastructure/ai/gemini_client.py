import google.generativeai as genai
from app.core.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

class GeminiClient:
    def __init__(self, system_prompt: str):
        self.model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",
            system_instruction=system_prompt,
        )

    def generate(self, contents):
        response = self.model.generate_content(
            contents,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                max_output_tokens=600,
            )
        )
        return response.text.strip()
