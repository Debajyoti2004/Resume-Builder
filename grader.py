from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os

load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp-01-21", google_api_key=os.getenv("GOOGLE_API_KEY"))

template = """You are a grader assessing whether an answer is useful to resolve a question. 
Here is the answer:
-------
{doc} 
-------
Here is the question: {question}
Give a binary score 'yes' or 'no' to indicate whether the answer is useful to resolve a question.
Provide the binary score as a JSON with a single key 'score' and no preamble or explanation."""

prompt = PromptTemplate(
    template=template,
    input_variables=["doc", "question"]
)

retrieval_grader = (
    prompt 
    | llm 
    | JsonOutputParser()
)

