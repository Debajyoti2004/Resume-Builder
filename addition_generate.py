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
    template="""You are a good resume generator who can make pro level resume from given formated resume 
    whuch already have all the information needed for you to generate resume.
    {query}

    Please generate a resume highlighting relevant skills, experiences, and accomplishments. Ensure the format is clean, with clear headings for 'Projects', 'Experience', 'Education', 'Skills', and 'Contact Information'and make 'Projects' headline contains more information about projects inside it.
    """,
    input_variables=["query"]
)


addn_final_rag_chain = (
    prompt
    | llm
    | StrOutputParser()
)




