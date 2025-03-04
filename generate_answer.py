from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-thinking-exp-01-21",
    api_key = os.getenv("GOOGLE_API_KEY")
)

prompt = PromptTemplate(
    template="""You are an expert resume writer. Using the provided information and question, craft a professional, concise, and impactful resume.

    Information provided:
    -------
    {docs}
    -------

    Specific request or question:
    {question}

    Please generate a resume highlighting relevant skills, experiences, and accomplishments. Ensure the format is clean, with clear headings for 'Projects', 'Experience', 'Education', 'Skills', and 'Contact Information'. 
    """,
    input_variables=["docs", "question"]
)


rag_chain = (
    prompt
    | llm
    | StrOutputParser()
)



