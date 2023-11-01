from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceHub


def get_openai_model():
    llm_model = ChatOpenAI()
    return llm_model


def get_huggingfacehub(model_name=None):
    llm_model = HuggingFaceHub(repo_id=model_name)
    return llm_model
