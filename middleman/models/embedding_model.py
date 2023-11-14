from langchain.embeddings import HuggingFaceInstructEmbeddings, OpenAIEmbeddings


def get_openaiEmbedding_model():
    return OpenAIEmbeddings()


def get_huggingfaceEmbedding_model():
    return HuggingFaceInstructEmbeddings()
