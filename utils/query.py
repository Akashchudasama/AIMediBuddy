import google.generativeai as genai
import os

# Load from environment or hardcoded key
genai.configure(api_key=os.getenv("AlzaSyA371G2dW7VTW4yxXqpljg XW3XgqFnBiYU") or "AIzaSyAb-OokqqGkHSaBilBOkxTLjHccH76l0Uo")

# Choose between 'models/gemini-1.5-pro' (better) or 'models/gemini-1.5-flash' (faster)
model = genai.GenerativeModel("models/gemini-1.5-flash")  # or "models/gemini-1.5-flash"


def query_llm(question, context_chunks):
    """
    Ask Gemini a question based on the provided context.
    """
    context = "\n\n".join(context_chunks)
    prompt = f"""
You are a helpful and knowledgeable medical assistant. Analyze the following medical document content and answer the user's question.

Medical Document:
{context}

Question: {question}

Answer:"""

    response = model.generate_content(prompt)
    return response.text.strip()
