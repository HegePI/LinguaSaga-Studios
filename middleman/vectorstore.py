import os

from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.indexes.vectorstore import (
    VectorstoreIndexCreator,
    VectorStoreIndexWrapper,
)

from langchain.vectorstores.chroma import Chroma


def get_index_path(
    index_name,
):
    return os.path.join(os.environ["LOCAL_PERSIST_PATH"], index_name)


def load_pdf_and_save_to_index(file_path, index_name):
    loader = PyPDFLoader(file_path)
    index = VectorstoreIndexCreator(
        vectorstore_kwargs={"persist_directory": get_index_path(index_name)}
    ).from_loaders([loader])
    index.vectorstore.persist()


def load_index(index_name):
    index_path = get_index_path(index_name)
    embedding_function = OpenAIEmbeddings()
    vectordb = Chroma(
        persist_directory=index_path, embedding_function=embedding_function
    )
    return VectorStoreIndexWrapper(vectorstore=vectordb)


def query_index(index, query):
    ans = index.query_with_sources(query, chain_type="map_reduce")
    return ans["answer"]


if __name__ == "__main__":
    load_dotenv()

    DATA_PATH = os.environ["DATA_PATH"]
    LOCAL_PERSIST_PATH = os.environ["LOCAL_PERSIST_PATH"]
    INDEX_NAME = os.environ["INDEX_NAME"]

    index = load_index(INDEX_NAME)
    # load_pdf_and_save_to_index(DATA_PATH, INDEX_NAME)

    while True:
        question = input("Ask a question: ")
        print("\n\n")
        print(query_index(index, question))
        print("\n\n")
