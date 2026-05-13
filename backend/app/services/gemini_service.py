import os

import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

print("GEMINI API KEY:", API_KEY)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_answer(question, context):

    try:

        prompt = f"""
        Answer the question based only on the context below.

        Context:
        {context}

        Question:
        {question}
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Gemini Error: {str(e)}"