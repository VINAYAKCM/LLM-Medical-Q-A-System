## Overview
The LLM Medical Q&A System is a retrieval-augmented generation (RAG) platform designed to answer medical queries using content extracted from medical textbooks. The system extracts text from PDF textbooks, builds a hierarchical index based on chapters and sections, retrieves relevant context using BM25, and leverages the Gemini API to generate detailed, context-aware answers. An interactive user interface built with Streamlit allows users to easily query the system.

## Features
- **Content Extraction:** Extracts text from PDF textbooks using improved extraction techniques.
- **Hierarchical Indexing:** Splits and organizes textbook content into chapters and sections for efficient retrieval.
- **Contextual Retrieval:** Uses BM25 to retrieve the most relevant sections based on user queries.
- **Retrieval-Augmented Generation:** Integrates retrieved context with the Gemini API to generate accurate answers.
- **User Interface:** Provides a clean, interactive UI with Streamlit that displays answers along with contextual references (source textbooks, chapters, and sections).

## Technologies Used
- **Python** for the core implementation.
- **PyPDF2 / pdfplumber** for PDF text extraction.
- **BM25** for information retrieval.
- **Gemini API** for language model generation.
- **Streamlit** for the web-based user interface.
- **Git & GitHub** for version control and source code management.

## Setup Instructions & Dependencies
1. **Clone the Repository:**
   Command: git clone https://github.com/<your-github-username>/LLM-Med-QA-System.git
   Command: cd LLM-Med-QA-System
  
3. **Create a Virtual Environment and Install Dependencies:**
   Command: python -m venv venv
   Command: source venv/bin/activate  #For Windows: venv\Scripts\activate
   Command: pip install -r requirements.txt

5. **Create a Virtual Environment and Install Dependencies:**
   Create a .env file in the project root and add your Gemini API key: GEMINI_API_KEY=your_api_key_here
   
7. **Create a Virtual Environment and Install Dependencies:**
   •Extract content from the PDFs:
   Command: python pdf_extracted.py

   •Build the index:
   Command: python build_index.py

8. **Running the UI:**
   To run the streamlit U.I:
   Command: streamlit run src/ui/app.py

   Open the provided URL in your browser. Enter your medical query in the text box, and view the generated answer along with the contextual references used.
