
from langgraph.graph import END, StateGraph, START
from graph_state import (
    transform_query, decide_to_generate, generate, generate_resume_json,
    addition_generation_node, grade_documents, retrieve,
    web_search_generation, route_question, create_json
)
from graph_state import GraphState

def compile_workflow():
    workflow = StateGraph(GraphState)

    workflow.add_node("Web_search", web_search_generation)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("transform_query", transform_query)
    workflow.add_node("generate", generate)
    workflow.add_node("additional generation", addition_generation_node)
    workflow.add_node("json_to_doc", generate_resume_json)
    workflow.add_node("json_result", create_json)

    workflow.add_conditional_edges(
        START,
        route_question,
        {
            "Vectorstore": "retrieve",
            "Web_search": "Web_search"
        },
    )
    workflow.add_edge("Web_search", "additional generation")
    workflow.add_edge("retrieve", "json_to_doc")
    workflow.add_edge("json_to_doc", "grade_documents")

    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate"
        },
    )
    workflow.add_edge("transform_query", "retrieve")
    workflow.add_edge("generate", "additional generation")
    workflow.add_edge("additional generation", "json_result")

    return workflow.compile()

app = compile_workflow()
print("---App Successfully compiled---")
