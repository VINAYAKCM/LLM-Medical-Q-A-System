import os
import json
import re

def extract_sections(text):
    """
    Splits text into sections based on a simple pattern for chapter headings.
    For example, it looks for "Chapter 1", "CHAPTER 2", etc.
    """
    # Define a regex pattern for chapters (this may need tweaking based on the actual PDFs)
    pattern = re.compile(r'(Chapter\s+\d+[\:.-]?)', re.IGNORECASE)
    splits = pattern.split(text)
    
    # If no chapters are found, return the full text as one section.
    if len(splits) < 2:
        return [{"title": "Full Text", "content": text.strip()}]
    
    sections = []
    # `splits` contains alternating non-heading and heading elements.
    for i in range(1, len(splits), 2):
        title = splits[i].strip()
        # Combine the heading with the following text chunk if available.
        content = splits[i+1].strip() if (i + 1) < len(splits) else ""
        sections.append({"title": title, "content": content})
    
    return sections

def build_index_for_file(extracted_file):
    """
    Reads an extracted JSON file, merges its text chunks, and builds a simple section index.
    """
    with open(extracted_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Combine all chunks into a single text blob
    full_text = " ".join(data.get("chunks", []))
    sections = extract_sections(full_text)
    
    index_data = {
        "filename": data.get("filename"),
        "sections": sections
    }
    return index_data

def main():
    extracted_dir = os.path.join("data", "extracted")
    index_dir = os.path.join("data", "indexed")
    os.makedirs(index_dir, exist_ok=True)
    
    json_files = [f for f in os.listdir(extracted_dir) if f.lower().endswith(".json")]
    if not json_files:
        print("No extracted JSON files found. Please run the extraction module first.")
        return

    for json_file in json_files:
        file_path = os.path.join(extracted_dir, json_file)
        index_data = build_index_for_file(file_path)
        output_path = os.path.join(index_dir, json_file)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(index_data, f, ensure_ascii=False, indent=4)
        print(f"Built index for {json_file} and saved to {output_path}")

if __name__ == "__main__":
    main()