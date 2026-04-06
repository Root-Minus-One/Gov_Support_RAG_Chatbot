from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import load_config
from utils.config import get_api_key
from typing import List, Dict

config = load_config()

def initialize_llm():
    """Purpose: To set up and return an instance of the LLM client (e.g., OpenAI, Hugging Face, Anthropic). This function would handle API key loading, model specification, and any initial configuration.
Example: Loading an OpenAI client or a HuggingFacePipeline.
"""
    try:

        ## get details from config file
        # get api key 
        ## load the llm with the details
        chat_model = config["llm"]
        llm_model = chat_model["model"]
        temp = chat_model["temperature"]
        max_tokens = chat_model["max_output_tokens"]


        return ChatGoogleGenerativeAI(
            model= llm_model,
            temperature=temp,
            max_output_tokens = max_tokens)
    except:
        pass




def generate_response():
    pass
"""Purpose: The primary function to send a prompt to the LLM and get a text completion or response.
Inputs: The initialized LLM client and the prompt string.
Outputs: The generated text response from the LLM.
generation_kwargs could include parameters like temperature, max_tokens, top_p, n (for multiple completions), stop_sequences, etc.
"""



def generate_chat_completion(llm_client, messages: List[Dict[str, str]], **generation_kwargs):
    pass

"""Purpose: If you're working with chat-based models (e.g., GPT-3.5-turbo, GPT-4), this function handles the structured input of messages (user, system, assistant roles) and retrieves a chat completion.
Inputs: The LLM client and a list of message dictionaries.
Outputs: The assistant's response in the chat format.
"""