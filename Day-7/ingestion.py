import asyncio
import os
import ssl
from typing import Any,Dict,List

import certifi
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_tavily import TavilyCrawl,TavilyExtract,TavilyMap
from langchain_postgres import PGVectorStore,PGEngine
from logger import *

load_dotenv()


#ssl configuration
ssl_context = ssl.create_default_context(cafile=certifi.where())
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUEST_C_BUNDLE"] = certifi.where()


embeddingEngine = OpenAIEmbeddings(show_progress_bar=True,chunk_size=50,retry_min_seconds=10)
# dbEngine = PGEngine.from_connection_string(url="postgresql+psycopg://postgres:password@localhost:5432/vectordb")
# vector_store = PGVectorStore.create_sync(engine=dbEngine,embedding_service=embeddingEngine,table_name="my_vector_collection_v3")

tavily_extact = TavilyExtract()
tavily_map = TavilyMap(max_depth=5,max_breadth=20,max_pages = 1000)
tavily_crawl = TavilyCrawl()


async def main():
    log_header("DOCUMEMTATION INGESTION PIPELINE")
    log_info("Starting to Crawl documetation from https://docs.langchain.com/oss/python/langchain/overview ",Colors.PURPLE)
    
    
    res = tavily_crawl.invoke({"url":"https://docs.langchain.com/oss/python/langchain/overview",
                                    "max_depth":2,
                                    "extract_depth":"advanced"})
    print("")
if __name__ == "__main__":
    asyncio.run(main())