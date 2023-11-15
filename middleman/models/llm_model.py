import os
from typing import Any, Dict, List, Optional

from huggingface_hub import InferenceClient
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.chains import ConversationalRetrievalChain, StuffDocumentsChain
from langchain.chat_models import ChatOpenAI
from langchain.llms.base import LLM
from langchain.llms.huggingface_hub import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema.retriever import BaseRetriever
from langchain.schema.runnable import RunnableConfig


class HuggingfaceConversationalRetrievalModel:
    llm: HuggingFaceHub
    memory: ConversationBufferMemory
    llm_chain: ConversationalRetrievalChain
    llm_chain_prompt: PromptTemplate
    doc_chain: StuffDocumentsChain
    doc_chain_prompt: PromptTemplate
    doc_variable_name: str
    retriever: BaseRetriever
    conversational_retrieval_chain: ConversationalRetrievalChain

    def __init__(
        self,
        retriever: BaseRetriever,
        model_kwargs=None,
        repo_id="mistralai/Mistral-7B-v0.1",
        llm: None | LLM = None,
    ) -> None:
        # self.memory = ConversationBufferMemory()
        self.llm = HuggingFaceHub(
            repo_id=repo_id,
            model_kwargs=model_kwargs,
        )

        if llm is not None:
            self.llm = llm

        self.retriever = retriever
        self.conversational_retrieval_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            verbose=True,
        )

    def get_conversational_retrieval_chain(self):
        return self.conversational_retrieval_chain


def get_openai_model():
    llm_model = ChatOpenAI()
    return llm_model


def get_huggingfacehub(model_name=None):
    llm_model = HuggingFaceHub(repo_id=model_name)
    return llm_model


class HugginfaceInferenceClientCustomLLM(LLM):
    inference_client: InferenceClient = None
    model: str = None

    def __init__(self, model="facebook/blenderbot-400M-distill") -> None:
        super(HugginfaceInferenceClientCustomLLM, self).__init__()
        self.inference_client = InferenceClient(model)

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any
    ) -> str:
        response = self.inference_client.conversational(prompt)
        return response["generated_text"]


class HugginfaceInferenceClientStreamingCustomLLM(LLM):
    inference_client: InferenceClient = None

    def __init__(self, model="mistralai/Mistral-7B-Instruct-v0.1") -> None:
        super(HugginfaceInferenceClientStreamingCustomLLM, self).__init__()
        self.inference_client = InferenceClient(
            model=model, token=os.environ["HUGGINGFACEHUB_API_TOKEN"]
        )

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any
    ) -> str:
        return self.inference_client.text_generation(prompt)

    def stream(self, input: Dict[str, Any], config: RunnableConfig | None = None):
        print("stream", input["content"])
        return self.inference_client.text_generation(
            input, max_new_tokens=2**10, stream=True
        )
