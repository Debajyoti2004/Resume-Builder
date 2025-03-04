from langchain.document_loaders import WebBaseLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import warnings
import os

load_dotenv()

warnings.filterwarnings('ignore')

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

web_based_loader = WebBaseLoader("https://github.com/Debajyoti2004?tab=repositories")
web_docs = web_based_loader.load()

resume_folder = r"C:\Users\Debajyoti\OneDrive\Desktop\Resume builder\resume_templates"
resume_docs = []
for file in os.listdir(resume_folder):
    if file.endswith(".txt"):
        loader = TextLoader(os.path.join(resume_folder, file))
        resume_docs.extend(loader.load())

all_docs = web_docs + resume_docs

vectorstore = FAISS.from_documents(
    documents=all_docs,
    embedding=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
