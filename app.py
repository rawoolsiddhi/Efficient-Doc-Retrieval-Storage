import streamlit as st
from src.retrieve_documents import retrieve_documents, get_top_searches
import os

st.set_page_config(page_title="Doc Search", layout="wide")
st.title("📄 Semantic Document Retrieval using Vector Space & Clustering")

query = st.text_input("🔍 Enter your search query")

st.sidebar.title("📌 Top Searches")
top_searches = get_top_searches()
if top_searches:
    for search in top_searches:
        st.sidebar.write(f"🔍 {search}")
else:
    st.sidebar.write("No top searches yet.")

if st.sidebar.button("➕ Upload Document"):
    st.sidebar.warning("⚠️ Upload not implemented yet.")

if st.button("Search"):
    if query:
        try:
            results = retrieve_documents(query)
            if results:
                st.write("### Results:")
                for result in results:
                    st.markdown(f"**📄 {result['filename']}**")
                    if result["pdf_link"] != "#":
                        # Check if the link is a valid file path or a base64 encoded string
                        if result["pdf_link"].startswith("data:application/pdf;base64"):
                            st.markdown(result["pdf_link"], unsafe_allow_html=True)  # Display inline PDF
                        else:
                            # Optionally, provide a download button if the file path is available
                            with open(result["pdf_link"], "rb") as f:
                                st.download_button(
                                    label="📥 Download PDF",
                                    data=f,
                                    file_name=os.path.basename(result["pdf_link"]),
                                    mime="application/pdf"
                                )
                    else:
                        st.write("🚫 PDF not found.")
                    st.write(f"🧠 Similarity Score: `{result['similarity_score']}`")
                    st.write(f"🧬 Cluster: `{result['cluster']}`")
                    st.write("---")
            else:
                st.warning("No relevant documents found.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Please enter a search query.")
