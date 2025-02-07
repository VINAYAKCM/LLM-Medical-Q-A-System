import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
from src.rag.rag_integration import generate_rag_answer

def main():
    st.title("Medical Q&A System")
    st.write("Enter your medical query below and receive an answer based on textbook data along with the relevant contextual references.")
    
    query = st.text_input("Enter your query:")
    
    if st.button("Get Answer"):
        if query:
            with st.spinner("Generating answer..."):
                answer, references = generate_rag_answer(query, top_n=3)
            st.markdown("### Answer:")
            st.write(answer)
            st.markdown("### Contextual References:")
            st.write(references)
        else:
            st.warning("Please enter a query.")

if __name__ == '__main__':
    main()

# To run the code, use this: streamlit run src/ui/app.py 


