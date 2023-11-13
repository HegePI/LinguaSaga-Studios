from langchain.document_loaders import PyPDFLoader
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from dotenv import load_dotenv
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

load_dotenv()

file_path = "./js_file.pdf"

local_persist_path = "./vector_store"


def get_index_path(index_name):
    return os.path.join(local_persist_path, index_name)

def load_pdf_and_save_to_index(file_path, index_name):
    loader = PyPDFLoader(file_path)
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":get_index_path(index_name)}).from_loaders([loader])
    index.vectorstore.persist()

def load_index(index_name):
    index_path = get_index_path(index_name)
    embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=index_path,embedding_function=embedding)
    return VectorStoreIndexWrapper(vectorstore=vectordb)

def query_index(index,query):
    ans = index.query_with_sources(query,chain_type="map_reduce")
    return ans['answer']

index = load_index("test2")
load_pdf_and_save_to_index(file_path, "test2")
ans = query_index(index,"who is johnny silverhand?")
print(ans)




