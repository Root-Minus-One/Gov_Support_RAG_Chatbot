import streamlit as st

def pdf_uploader():
    return st.file_uploader("Upload the pdf file", 
                            type = ["pdf"], 
                            accept_multiple_files = True, 
                            help = "Upload one or more PDF files to process.")

