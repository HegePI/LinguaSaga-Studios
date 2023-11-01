from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.llms.base import LLM
from langchain.chains import LLMChain

from threading import Thread
from typing import Optional
from transformers import TextIteratorStreamer


def initialize_model_and_tokenizer(model_name="bigscience/bloom-1b7"):
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer


def init_chain(model, tokenizer):
    llm = CustomLLM(model, tokenizer)
    llm_chain = LLMChain(llm=llm)

    return llm, llm_chain


class CustomLLM(LLM):
    streamer: Optional[TextIteratorStreamer] = None
    model = None
    tokenizer = None

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def _call(self, prompt, stop=None, run_manager=None) -> str:
        self.streamer = TextIteratorStreamer(
            self.tokenizer, skip_prompt=True, Timeout=5
        )
        inputs = self.tokenizer(prompt, return_tensors="pt")
        kwargs = dict(
            input_ids=inputs["input_ids"], streamer=self.streamer, max_new_tokens=20
        )
        thread = Thread(target=self.model.generate, kwargs=kwargs)
        thread.start()
        return ""

    @property
    def _llm_type(self) -> str:
        return "custom"
