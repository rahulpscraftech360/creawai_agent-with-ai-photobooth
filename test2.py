# test_api.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key="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")

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, world!"}]
    )
    print("API key is valid!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"API key is invalid or there was an error: {e}")