import os
import json
import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF using pdfplumber, preserving basic layout
    and inserting page markers.
    """
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                # Prepend a page marker to help identify where text comes from.
                full_text += f"\n--- Page {page_num} ---\n"
                full_text += page_text + "\n"
            else:
                print(f"Warning: No text found on page {page_num} of {pdf_path}")
    return full_text

def chunk_text(text, chunk_size=1000, overlap=100):
    """
    Splits the text into chunks based on word count.
    You might later consider splitting on paragraphs (using newline characters)
    if that better preserves context.
    """
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += (chunk_size - overlap)
    return chunks

def process_pdf(pdf_filename, output_dir):
    """
    Processes a single PDF:
      - Extracts text using pdfplumber.
      - Splits the text into chunks.
      - Saves the result in JSON format.
    """
    pdf_path = os.path.join("data", "raw_pdfs", pdf_filename)
    print(f"Processing {pdf_path}...")
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    output_data = {
        "filename": pdf_filename,
        "chunks": chunks
    }
    output_filename = os.path.splitext(pdf_filename)[0] + ".json"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    
    print(f"Saved extracted data to {output_path}")

def process_all_pdfs():
    """
    Processes all PDF files found in the raw_pdfs directory.
    """
    raw_pdfs_dir = os.path.join("data", "raw_pdfs")
    output_dir = os.path.join("data", "extracted")
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(raw_pdfs_dir) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("No PDF files found in the raw_pdfs directory.")
        return

    for pdf_file in pdf_files:
        process_pdf(pdf_file, output_dir)

if __name__ == "__main__":
    process_all_pdfs()