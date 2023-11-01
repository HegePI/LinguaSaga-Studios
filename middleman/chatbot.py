import streamlit as st
from utils.utils import extract_text_from_PDF, split_content_into_chunks
from utils.utils import save_chunks_into_vectorstore, get_chat_chain, process_user_input
from models.embedding_model import (
    get_openaiEmbedding_model,
    get_huggingfaceEmbedding_model,
)
from dotenv import load_dotenv

load_dotenv()


def main():
    # Temporary interface
    st.set_page_config(page_title="Cyberpunk NPCs ChatBot", page_icon=":NPC:")

    st.header("Cyberpunk NPCs ChatBot")

    # Initial
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # User input
    # we can get the username and npcs` names through the former steps
    user_input = st.text_input(
        "Hi, V I am Johnny Silverhand, What questions do you have?: "
    )
    if user_input:
        process_user_input(user_input)

    with st.sidebar:
        st.subheader("NPC`s background stories")
        files = st.file_uploader("Input background stories", accept_multiple_files=True)
        if st.button("submission"):
            with st.spinner("wait... processing the dialogue"):
                texts = extract_text_from_PDF(files)
                # split the text
                content_chunks = split_content_into_chunks(texts)
                # st.write(content_chunks)
                # embedding each chunks and store it into the vector store
                # embedding_model = get_openaiEmbedding_model()

                # also we can use the hugging face
                embedding_model = get_huggingfaceEmbedding_model()

                # create the vector store and store the chunks
                vector_store = save_chunks_into_vectorstore(
                    content_chunks, embedding_model
                )

                # 7. create the chain
                st.session_state.conversation = get_chat_chain(vector_store)


if __name__ == "__main__":
    main()
