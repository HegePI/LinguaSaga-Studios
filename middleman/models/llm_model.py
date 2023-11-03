from typing import Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings

from middleman.utils.utils import (
    extract_text_from_PDF,
    save_chunks_into_vectorstore,
    split_content_into_chunks,
)


class HuggingfaceConversationalRetrievalModel:
    repo_id: str
    model_kwargs: Dict
    llm: HuggingFaceHub
    memory: ConversationBufferMemory
    chain: ConversationalRetrievalChain
    vector_store: FAISS
    embedding: HuggingFaceInstructEmbeddings
    files: Any

    def __init__(self, model_kwargs, repo_id="mistralai/Mistral-7B-v0.1") -> None:
        self.repo_id = repo_id
        self.model_kwargs = model_kwargs
        self.embedding = HuggingFaceInstructEmbeddings()

    def set_files(self, files):
        self.files = files
        return self

    def set_llm(self):
        self.llm = HuggingFaceHub(repo_id=self.repo_id, model_kwargs=self.model_kwargs)
        return self

    def set_conversation_buffer_memory(self):
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        return self

    def set_chain(self):
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(),
            memory=self.memory,
            verbose=True,
        )
        return self

    def set_vector_store(self):
        text = extract_text_from_PDF(files=self.files)
        chunks = split_content_into_chunks(text)
        self.vector_store = save_chunks_into_vectorstore(chunks, self.embedding)
        return self

    def predict(self, query, history):
        # Needs to be implemented
        pass


def get_openai_model():
    llm_model = ChatOpenAI()
    return llm_model


def get_huggingfacehub(model_name=None):
    llm_model = HuggingFaceHub(repo_id=model_name)
    return llm_model
