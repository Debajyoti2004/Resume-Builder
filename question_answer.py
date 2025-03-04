from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-thinking-exp-01-21",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

template = """
You are an expert resume writer. Using the provided query, generate a tailored and professional project manager resume in valid JSON format.

Query:
-------
{query}
-------

Provide the resume strictly as a JSON object with the following structure:

{{
    "name": "Full Name",
    "email": "Email Address",
    "phone": "Phone Number",
    "objective": "Concise project manager objective statement.",
    "experience": [
        {{
            "job_title": "Job Title",
            "company_name": "Company Name",
            "years": "Years Worked",
            "projects": [
                {{
                    "project1": "Project Name",
                    "timeline": "Project Timeline",
                    "description": details about that project
                }},
                {{
                     "project2": "Project Name",
                     "timeline": "Project Timeline",
                     "description": details about that project
                }},

                    so on continue if there is any other project in query
            ]
        }}
    ],
    "skills": ["Skill1", "Skill2", "Skill3",...(All skills)],
    "education": [
        {{
            "degree": "Degree",
            "university": "University Name",
            "year": "Graduation Year"
        }}
    ]
}}

Ensure the output is valid JSON with no additional text or explanations.
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["query"] 
)

a_a_chain = (
    prompt
    | llm
    | JsonOutputParser()
)

