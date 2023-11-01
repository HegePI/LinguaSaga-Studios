from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings


def get_openaiEmbedding_model():
    return OpenAIEmbeddings()


def get_huggingfaceEmbedding_model():
    return HuggingFaceInstructEmbeddings()
