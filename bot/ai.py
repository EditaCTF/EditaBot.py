import google.generativeai as genai
import os

def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
    model = genai.GenerativeModel("gemini-2.0-flash", generation_config=generation_config)
    return model.start_chat(history=[])
