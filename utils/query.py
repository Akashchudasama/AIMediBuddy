from google import genai

# VITAL FIX: Use a correct, available model name (like gemini-2.5-flash)
# This resolves the google.api_core.exceptions.NotFound error.
MODEL_NAME = "gemini-2.5-flash" 

# Initialize the LLM client once
try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    # This should be handled in App.py, but kept here for completeness
    print(f"Error initializing model: {e}")
    model = None


def generate_prompt(query, chunks):
    """Creates a comprehensive RAG prompt for the LLM."""
    
    context = "\n---\n".join(chunks)

    prompt = f"""
    You are an expert medical document Q&A system. Your task is to answer the user's question
    based *only* on the provided context, which is extracted from a medical document.
    
    If the answer cannot be found in the context, clearly state, "The required information 
    was not found in the provided document." Do not use any external knowledge.

    CONTEXT:
    ---
    {context}
    ---

    QUESTION: "{query}"

    ANSWER:
    """
    return prompt

def query_llm(query, chunks):
    """Generates the prompt and calls the Generative Model."""
    if not chunks:
        return "No relevant information could be retrieved from the document. The document might be empty or the content is irrelevant to the question."

    if model is None:
        return "Error: LLM model is not initialized."

    prompt = generate_prompt(query, chunks)
    
    try:
        # Call the LLM to generate content
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"LLM API Error: {e}")
        return f"An error occurred while querying the LLM: {e}"
