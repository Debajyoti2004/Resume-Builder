from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
from langchain.tools import DuckDuckGoSearchRun

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-thinking-exp-01-21",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

search = DuckDuckGoSearchRun()

template = """
You are an expert resume writer. Using the LinkedIn profile data and the provided question, generate a tailored and professional resume.

LinkedIn Profile Data:
-------
{linkedin_data}
-------

Question:
{question}

Please generate a resume highlighting relevant skills, experiences, and accomplishments. Ensure the format is clean, with clear headings for 'Summary', 'Experience','Projects', 'Education', 'Skills', and 'Contact Information'. 
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["linkedin_data", "question"]
)

resume_chain = (
    prompt
    | llm
    | StrOutputParser()
)

def web_search_chain(linkedin_url, question):
    try:
        if linkedin_url:
            search_results = search.run(f"site:linkedin.com/in {linkedin_url}")
        else:
            search_results = None

        result = resume_chain.invoke({
            "linkedin_data": search_results,
            "question": question
        })

        return result
    except Exception as e:
        print(f"Error during LinkedIn search or resume generation: {e}")
        return None
