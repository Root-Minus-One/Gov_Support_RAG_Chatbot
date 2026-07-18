#from google import genai
from loguru import logger
from groq import Groq

from app.core.config import settings
from app.rag.prompt_templates import get_prompt_template


client = Groq(api_key=settings.GROQ_API_KEY.get_secret_value())

def generate_answer(question: str, chunks: list[dict]) -> str:

    prompt = get_prompt_template(question, chunks)

    interaction = client.chat.completions.create(
    model=settings.LLM_MODEL_NAME,
    messages=[
        {"role": "user", "content": prompt}
    ])
    
    return interaction.choices[0].message.content or "I was unable to generate an answer."