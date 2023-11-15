import streamlit as st
from config.templates import bot_template, user_template
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from models.llm_model import (
    HugginfaceInferenceClientCustomLLM,
    HuggingfaceConversationalRetrievalModel,
)
from PyPDF2 import PdfReader


def extract_text_from_PDF(files):
    text = ""
    for pdf in files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def split_content_into_chunks(text):
    text_spliter = CharacterTextSplitter(
        separator="\n", chunk_size=500, chunk_overlap=80, length_function=len
    )
    chunks = text_spliter.split_text(text)
    return chunks


def save_chunks_into_vectorstore(content_chunks, embedding_model):
    # ① FAISS
    # pip install faiss-gpu (if you don`t have GPU，then pip install faiss-cpu)
    vectorstore = FAISS.from_texts(texts=content_chunks, embedding=embedding_model)

    # ② Pinecone
    # https://python.langchain.com/docs/integrations/vectorstores/pinecone
    # Pinecone：https://docs.pinecone.io/docs/quickstart
    # pip install pinecone-client==2.2.2
    # Intial
    # pinecone.init(api_key=Keys.PINECONE_KEY, environment="asia-southeast1-gcp")
    # # create index
    # index_name = "pinecone-chatbot-demo"
    # # check if the index exist
    # if index_name not in pinecone.list_indexes():
    #     pinecone.create_index(name=index_name,
    #                           metric="cosine",
    #                           dimension=1536)
    # vectorstore = Pinecone.from_texts(texts=content_chunks,
    #                                       embedding=embedding_model,
    #                                       index_name=index_name)

    # ③ Milvus, pip install pymilvus
    # https://python.langchain.com/docs/integrations/vectorstores/milvus
    # vectorstore = Milvus.from_texts(texts=content_chunks,
    #                                     embedding=embedding_model,
    #                                     connection_args={"host": "localhost", "port": "19530"},
    # )

    return vectorstore


def get_huggingface_conversational_retrieval_chain(vector_store):
    llm = HugginfaceInferenceClientCustomLLM()
    return HuggingfaceConversationalRetrievalModel(
        retriever=vector_store.as_retriever(), llm=llm
    ).get_conversational_retrieval_chain()


def process_user_input(user_input):
    print("process_user_input", user_input)
    if st.session_state.conversation is not None:
        response = st.session_state.conversation(
            {"question": user_input, "chat_history": ""}
        )

        print(response)

        st.session_state.chat_history = response["chat_history"]

        for i, message in enumerate(st.session_state.chat_history):
            print(message["answer"])
            if i % 2 == 0:
                st.write(
                    user_template.replace("{{MSG}}", message["answer"]),
                    unsafe_allow_html=True,
                )
            else:
                st.write(
                    bot_template.replace("{{MSG}}", message["answer"]),
                    unsafe_allow_html=True,
                )
