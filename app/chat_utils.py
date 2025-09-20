import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
# !pip install -q langchain-google-genai

# Configure API key
genai.configure(api_key="AIzaSyCjOMCMBOOS7e6s0n2zAvWQZDgbxqFYBJ8")

# Create the model
model = genai.GenerativeModel("gemini-2.0-flash")

# Generate response
response = model.generate_content("Explain how AI works in a few words")

print(response.text)