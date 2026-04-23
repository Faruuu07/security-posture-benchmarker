import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_description(user_input):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert. Explain clearly in simple terms."},
                {"role": "user", "content": f"Explain this security issue: {user_input}"}
            ]
        )

        # Clean output
        result = response.choices[0].message.content.strip()
        return result

    except Exception as e:
        return f"Error: {str(e)}"