import os
import json
from rank_bm25 import BM25Okapi

def load_index_data(index_dir='data/indexed'):
    """
    Loads all indexed JSON files from the `data/indexed` folder.
    Each file is expected to have a structure with 'filename' and a list of 'sections'.
    """
    sections = []
    for filename in os.listdir(index_dir):
        if filename.lower().endswith('.json'):
            file_path = os.path.join(index_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for section in data.get('sections', []):
                    sections.append({
                        'filename': data.get('filename'),
                        'title': section.get('title', 'No Title'),
                        'content': section.get('content', '')
                    })
    return sections

def tokenize(text):
    """
    Simple tokenizer: converts text to lowercase and splits on whitespace.
    You can later swap this out for a more sophisticated tokenizer if needed.
    """
    return text.lower().split()

class BM25Retriever:
    def __init__(self, sections):
        self.sections = sections
        # Prepare the corpus: tokenize the content of each section
        self.corpus = [tokenize(section['content']) for section in sections]
        # Initialize BM25 on the tokenized corpus
        self.bm25 = BM25Okapi(self.corpus)
    
    def retrieve(self, query, top_n=5):
        """
        Given a query, returns the top_n most relevant sections.
        """
        tokenized_query = tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        # Get indices of the highest scoring sections
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
        results = []
        for idx in top_indices:
            section = self.sections[idx]
            results.append({
                'filename': section['filename'],
                'title': section['title'],
                'content': section['content'],
                'score': scores[idx]
            })
        return results

def main():
    # Load indexed data and initialize the BM25 retriever
    sections = load_index_data()
    retriever = BM25Retriever(sections)
    
    # Simple command-line loop for testing
    while True:
        query = input("Enter your query (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        results = retriever.retrieve(query, top_n=5)
        print("\nTop Results:")
        for res in results:
            print(f"File: {res['filename']}, Section: {res['title']}, Score: {res['score']:.2f}")
            # Print a brief excerpt
            print(f"Excerpt: {res['content'][:200]}...\n")

if __name__ == "__main__":
    main()