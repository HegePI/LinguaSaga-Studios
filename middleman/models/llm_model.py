from socket import timeout
from threading import Thread
from langchain.chat_models import ChatOpenAI
from langchain.llms.huggingface_hub import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, StuffDocumentsChain
from langchain.schema.retriever import BaseRetriever
from langchain.prompts import PromptTemplate
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun

from huggingface_hub import InferenceClient


from typing import Optional, List, Any


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
    # model: str = None
    # tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast = None
    # streamer: TextStreamer = None

    def __init__(self, model="mistralai/Mistral-7B-Instruct-v0.1") -> None:
        super(HugginfaceInferenceClientStreamingCustomLLM, self).__init__()
        self.inference_client = InferenceClient(model=model)
        # self.model = AutoModelForCausalLM.from_pretrained(model)
        # self.tokenizer = AutoTokenizer.from_pretrained(model)
        # self.streamer = TextStreamer(tokenizer=self.tokenizer, Timeout=5)

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
        kwargs = dict(prompt=prompt, stream=True, max_new_tokens=2**10)
        thread = Thread(target=self.inference_client.text_generation, kwargs=kwargs)
        thread.start()

        return ""
