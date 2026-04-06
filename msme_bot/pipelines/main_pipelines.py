#import extractor
#import chunker

def run_ingestion_pipeline(pdf_list):
    # 1. Initialize the AI engine once (Production best practice)
    converter = extractor.get_docling_converter()
    
    for i, pdf_path in enumerate(pdf_list):
        file_id = f"PDF_BATCH_{i:03}"
        
        # 2. EXTRACTION: Get Smart Map and Physical Assets
        doc_obj, physical_assets = extractor.extract_assets(pdf_path, converter)
        
        # 3. CHUNKING: Slices the Smart Map for the Database
        searchable_chunks = chunker.get_smart_chunks(doc_obj, file_id)
        
        # 4. STORAGE STRATEGY
        # Bucket A: Physical Assets -> UPLOAD TO S3
        # (Save images/tables to cloud storage here)
        
        # Bucket B: Searchable Assets -> APPEND TO DATABASE
        # (Save searchable_chunks into your SQL/Vector DB here)
        
        print(f"File {file_id} processed. Chunks: {len(searchable_chunks)}, Assets: {len(physical_assets['images'])}")

# Usage
# run_production_pipeline([r"C:\Docs\report1.pdf", r"C:\Docs\report2.pdf"])
