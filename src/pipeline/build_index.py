from src.ingest.document_loader import load_all_pdfs
from src.ingest.text_splitter import doc_text_splitter
from src.embed.embedder import HGF_embedder
from src.embed.vectorstore import create_vector_store


def build_index():
    
    load_docs = load_all_pdfs("dataset")
    print(f"Loaded {len(load_docs)} documents")

    String_bits = doc_text_splitter(load_docs)

    embedding = HGF_embedder()

    store = create_vector_store("docstore", embedding, "abcd", "tygkfy")

    store.add_documents(String_bits)