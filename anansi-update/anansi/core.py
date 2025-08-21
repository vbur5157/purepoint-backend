
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    messages = [
        {"role": "system", "content": "You are Anansi, a helpful, sarcastic, and professional assistant loyal to Vadim. Remember user preferences and adapt over time."},
        {"role": "user", "content": prompt}
    ]
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
