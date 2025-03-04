from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import json

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-thinking-exp-01-21",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

template = """
You are given an input JSON containing answers and documents. Your task is to generate a new, coherent document by merging all the information provided.

Input JSON:
{input_json}

Input Document:
{docs}

Instructions:
- Carefully extract key points from each document.
- Combine the answers logically and ensure the flow is smooth.
- The final document should be clear, concise, and factually accurate.

Output:
New Document:
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["input_json", "docs"]
)

doc_chain = (
    prompt
    | llm
    | StrOutputParser()
)

