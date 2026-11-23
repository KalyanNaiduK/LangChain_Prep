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


async def init_db():
    embeddingEngine = OpenAIEmbeddings(model="text-embedding-3-small",show_progress_bar=True,chunk_size=50,retry_min_seconds=10)
    dbEngine = PGEngine.from_connection_string(url="postgresql+psycopg://postgres:password@localhost:5432/vectordb")
    await dbEngine.ainit_vectorstore_table(
        table_name="my_vector_collection_v3",
        vector_size=1536,
        schema_name="public")
    vector_store = PGVectorStore.create_sync(engine=dbEngine,embedding_service=embeddingEngine,table_name="my_vector_collection_v3")
    return vector_store

tavily_extact = TavilyExtract()
tavily_map = TavilyMap(max_depth=1,max_breadth=0,max_pages = 1000)
tavily_crawl = TavilyCrawl()

async def index_split_documents(split_documents:List[Document],batchsize:int = 500):
    
    vs = await init_db()
    
    batches = [split_documents[i:i+batchsize] for i in range(0,len(split_documents),batchsize)]
    log_info(f"Created {len(batches)} batches with each batch average size is : {len(batches[0])}",Colors.UNDERLINE)
    async def add_batch(batch:List[Document],batchNumber):
        try:
            await vs.aadd_documents(batch)
            log_success(f"Vector Store indexing: Successfully indexed batch {batchNumber}/{len(batches)} {len(batch)} documents")
        except Exception as e:
            log_error(f"Vector Store indexing: Failed to index batch {batchNumber} - {e}")
            return False
        return True
    
    log_info("Processing Batches")
    # tasks = [add_batch(batch,i+1) for i,batch in enumerate(batches)] #list of add_batch functions concurrent processing of batches
    # below is the code for sequentially processing the batches due to ratelimiting issue 
    results = []
    for batchNumber,batch in enumerate(batches,start=1):
        result = await add_batch(batch,batchNumber)
        results.append(result)
        
        if batchNumber<len(batches):
            await asyncio.sleep(90)
    
    successfull = sum(1 for result in results if result is True)
    
    if successfull==len(batches):
        log_info("Vector Store indexing: Document indexing Successfull to vector DB")
    else:
        log_warning("Vector Store indexing: Document indexing Partially failed......")
    
async def main():
    log_header("DOCUMEMTATION INGESTION PIPELINE")
    log_info("Starting to Crawl documetation from https://docs.langchain.com/oss/python/langchain/overview ")
    
    
    res = tavily_crawl.invoke({"url":"https://docs.langchain.com/oss/python/langchain/overview",
                                    "max_depth":2,
                                    "extract_depth":"advanced"})
    
    all_docs = [Document(page_content=str(result['raw_content']),metadata={"source":result['url']}) for result in res['results']]
    log_success(f"Tavily Crawlling Success : total number of documents crawled = {len(all_docs)}")

    log_header("DOCUMENT CHUNKING PHRASE")
    log_info(f"Starting Chunking process of all the scraped {len(all_docs)} documents")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000,chunk_overlap=200)
    splitted_documents = text_splitter.split_documents(all_docs)
    log_success(f"Text Splitter Created {len(splitted_documents)} chunks from {len(all_docs)} documents")
    
    log_header("DOCUMENT INDEXING PHRASE")
    
    await index_split_documents(splitted_documents,500)
    
    
    log_header("PIPELINE COMPLETE")
    
if __name__ == "__main__":
    asyncio.run(main())