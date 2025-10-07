from langchain.text_splitter import RecursiveCharacterTextSplitter



def doc_text_splitter(data):
    text_chunker = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
    chunks = text_chunker.split_documents(data)

    return chunks