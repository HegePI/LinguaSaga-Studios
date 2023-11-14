import os

from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from langchain.indexes.vectorstore import (
    VectorstoreIndexCreator,
    VectorStoreIndexWrapper,
)
from langchain.vectorstores.chroma import Chroma


def get_index_path(index_name):
    return os.path.join(LOCAL_PERSIST_PATH, index_name)


def load_pdf_and_save_to_index(file_path, index_name):
    loader = PyPDFLoader(file_path)
    index = VectorstoreIndexCreator(
        vectorstore_kwargs={"persist_directory": get_index_path(index_name)}
    ).from_loaders([loader])
    index.vectorstore.persist()


def load_index(index_name):
    index_path = get_index_path(index_name)
    embedding_function = OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"],
        model_name="text-embedding-ada-002",
    )
    vectordb = Chroma(
        persist_directory=index_path, embedding_function=embedding_function
    )
    return VectorStoreIndexWrapper(vectorstore=vectordb)


def query_index(index, query):
    ans = index.query_with_sources(query, chain_type="map_reduce")
    return ans["answer"]


if __name__ == "__main__":
    load_dotenv()

    DATA_PATH = "./js_file.pdf"
    LOCAL_PERSIST_PATH = "./vector_store"
    INDEX_NAME = "test2"

    index = load_index(INDEX_NAME)
    load_pdf_and_save_to_index(DATA_PATH, INDEX_NAME)
    ans = query_index(index, "who is johnny silverhand?")
    print(ans)
