### Question_rewriter

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp-01-21", google_api_key=os.getenv("GOOGLE_API_KEY"))

rewrite_prompt = PromptTemplate(
    template = """You are a question re-writer that converts an input question to a better version that is optimized \n 
     for vectorstore retrieval. Look at the initial and formulate an improved question. \n
     Here is the initial question: \n\n {question}. Improved question with no preamble: \n """,
     input_variables = ["question"]
)

q_rewriter = (
    rewrite_prompt
    | llm
    | StrOutputParser()
)

