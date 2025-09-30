from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    load_index_from_storage,
    StorageContext
)
import os
from dotenv import load_dotenv

os.environ['HTTP_PROXY'] = 'http://35.243.0.220:10018'
os.environ['HTTPS_PROXY'] = 'http://35.243.0.220:10018'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "datasets", "data")
STORAGE_DIR = os.path.join(BASE_DIR, "..", "datasets", "storage")


def ai_helper(question: str):
    # Загружаем ключи из .env
    load_dotenv()

    # Настройки LLM и эмбеддингов
    Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.1, max_tokens=140)
    Settings.embed_model = OpenAIEmbedding(
        model="text-embedding-3-small",
        embed_batch_size=100
    )
    Settings.transformations = [SentenceSplitter(chunk_size=1024)]

    # Загружаем или создаём индекс
    if not os.path.exists(STORAGE_DIR):
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        index = VectorStoreIndex.from_documents(
            documents,
            embed_model=Settings.embed_model,
            transformations=Settings.transformations
        )
        index.storage_context.persist(persist_dir=STORAGE_DIR)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
        index = load_index_from_storage(storage_context)

    # Запрос
    query_engine = index.as_query_engine()
    response = query_engine.query(f"{question}. Ответь на русском языке.")
    return str(response.response)


