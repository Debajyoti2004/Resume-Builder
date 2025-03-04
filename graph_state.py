from typing import List
from typing_extensions import TypedDict
from langchain.schema import Document

from retriever import retriever
from generate_answer import rag_chain
from grader import retrieval_grader
from question_answer import a_a_chain
from doc_chain import doc_chain
from question_rewriter import q_rewriter
from routing import route_query
from web_search import web_search_chain
from addition_generate import addn_final_rag_chain

class GraphState(TypedDict):
    query: str
    question: str
    generation: str
    json_output: dict
    linkedin_link: str
    documents: List[Document]

def retrieve(state: GraphState) -> GraphState:
    print("---RETRIEVE---")
    question = state["question"]
    documents = retriever.get_relevant_documents(question)
    return {
        **state, 
        "documents": documents
        }

def generate(state: GraphState) -> GraphState:
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    generation = rag_chain.invoke({
        "docs": documents,
        "question": question
    })
    return {
        **state, 
        "generation": generation
        }

def grade_documents(state: GraphState) -> GraphState:
    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]
    filtered_docs = []

    for d in documents:
        score = retrieval_grader.invoke({
            "doc": d.page_content,
            "question": question
        })
        if score.get("score") == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
    
    return {
        **state, 
        "documents": filtered_docs
        }

def generate_resume_json(state: GraphState) -> GraphState:
    print("---CREATE JSON FILE FOR RESUME GENERATION---")
    query = state["query"]
    filtered_documents = state["documents"]

    json_docs = a_a_chain.invoke({"query": query})
    new_docs = []
    for d in filtered_documents:
        new_doc = doc_chain.invoke({
            "input_json": json_docs,
            "docs": d.page_content
        })
        new_docs.append(Document(page_content=new_doc))

    return {
        **state, 
        "documents": new_docs
        }

def transform_query(state: GraphState) -> GraphState:
    print("---TRANSFORM QUERY---")
    question = state["question"]
    better_question = q_rewriter.invoke({"question": question})
    return {
        **state, 
        "question": better_question
        }

def route_question(state: GraphState) -> str:
    print("---ROUTING THE GIVEN QUESTION---")
    question = state["question"]
    passion = route_query(question)
    return "Web_search" if passion == "Unknown" else "Vectorstore"

def decide_to_generate(state: GraphState) -> str:
    print("--ASSESS GRADED DOCUMENTS---")
    filtered_documents = state["documents"]
    return "transform_query" if not filtered_documents else "generate"

def web_search_generation(state: GraphState) -> GraphState:
    print("---START WEB SEARCHING---")
    linkedin_link = state["linkedin_link"]
    question = state["question"]
    result = web_search_chain(
        linkedin_url=linkedin_link,
        question=question
    )
    return {
        **state, 
        "generation": result
        }

def addition_generation_node(state: GraphState) -> GraphState:
    print("---ADDITION GENERATION NODE---")
    generation = state["generation"] + state["query"]
    final_generation = addn_final_rag_chain.invoke({"query": generation})
    return {
        **state, 
        "generation": final_generation
        }

def create_json(state):
    print(" --- CREATING FINAL JSON FILE FROM GENERATED OUTPUT FROM LLM --- ")
    generate = state["generation"]

    json_result = a_a_chain.invoke({
        "query":generate
    })

    return {
        **state,
        "json_output":json_result
    }
