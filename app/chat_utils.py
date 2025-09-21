from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
# !pip install -q langchain-google-genai

<<<<<<< HEAD
# Configure API key

=======
>>>>>>> b06ae4f (Update chat_utils.py)

# Create the model
("gemini-2.0-flash")

# Generate response
<<<<<<< HEAD
response = ("Explain how AI works in a few words")
=======
response = model.generate_content("Explain how AI works in a few words")

print(response.text)
>>>>>>> b06ae4f (Update chat_utils.py)
