import os
from src.retrieval.bm25_retriever import BM25Retriever, load_index_data
from google import genai
from dotenv import load_dotenv

# Load environment variables (if using a .env file)
load_dotenv()

# Initialize the Gemini API client with your API key from environment.
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

client = genai.Client(api_key=api_key)

def call_llm(prompt):
    """
    Uses the Gemini API to generate a response based on the provided prompt.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # Use the model name provided by Gemini.
            contents=prompt
            # Note: If you find a supported parameter for longer outputs, add it here.
        )
        # Return the generated text.
        return response.text.strip()
    except Exception as e:
        return f"An error occurred while generating the answer: {str(e)}"

def truncate_text(text, max_words=150):
    """
    Truncates the input text to the first `max_words` words.
    (A simple heuristic for controlling prompt length.)
    """
    words = text.split()
    return " ".join(words[:max_words])

def generate_rag_answer(query, top_n=3):
    """
    Retrieves context using BM25 and then generates an answer using the Gemini API.
    Returns both the answer and a string of contextual references (source textbook, chapter, section).
    """
    # Load the extracted textbook data.
    sections = load_index_data()
    retriever = BM25Retriever(sections)
    
    # Retrieve the top relevant section(s) for the given query.
    retrieved_sections = retriever.retrieve(query, top_n=top_n)
    
    # Build a concise context string that includes the source (filename) and section title.
    context = "\n\n".join(
        [f"Source: {sec.get('filename', 'Unknown')} - {sec['title']}\n{truncate_text(sec['content'], max_words=150)}"
         for sec in retrieved_sections]
    )
    
    # Build a separate references string to display in the UI.
    references = "\n".join(
        [f"{sec.get('filename', 'Unknown')}: {sec['title']}" for sec in retrieved_sections]
    )
    
    # Debug: print the retrieved context.
    print("Retrieved Context:\n", context)
    
    # Construct the prompt with clear instructions.
    prompt = (
        "You are a knowledgeable and helpful medical expert. Based on the context provided below, "
        "please answer the following question as accurately as possible. If the context is insufficient, "
        "indicate that further information is needed.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        "Answer:"
    )
    
    # Call the Gemini API with the constructed prompt.
    answer = call_llm(prompt)
    return answer, references

def main():
    # Simple command-line loop for testing.
    while True:
        query = input("Enter your medical query (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        answer, refs = generate_rag_answer(query, top_n=3)
        print("\nGenerated Answer:")
        print(answer)
        print("\nContextual References:")
        print(refs)
        print("-" * 50)

if __name__ == "__main__":
    main()

# To run the code, use this: python -m src.rag.rag_integration


