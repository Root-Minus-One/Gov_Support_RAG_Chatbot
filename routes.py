# routes.py
from fastapi import APIRouter, UploadFile, File, Request
#import chunker
#import extractor # still need this for the extraction function call

router = APIRouter()

@router.post("/process-pdf")
async def process_pdf(request: Request, file: UploadFile = File(...)):
    # 1. Access the 'Warm' converter from main.py
    converter = request.app.state.converter
    
    # 2. Use your modular pipeline
    # doc_obj, assets = extractor.extract_to_doc_and_assets(temp_path, converter)
    # ... rest of your logic ...
    
    return {"status": "success", "filename": file.filename}



@router.get("/")
def home():
    return render_template("chat.html")


@router.get("/msg")
def chat():
    msg= request.form["msg"]
    input= msg
    print(input)
    response = rag_chain.invoke({"input" : msg})
    print("Response : ", response["answer"])
    return str(response["answer"])



if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8080, debug = True)