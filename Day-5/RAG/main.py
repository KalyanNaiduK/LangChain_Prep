from langchain_openai import OpenAIEmbeddings
# from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_postgres import PGVectorStore,PGEngine
from dotenv import load_dotenv
load_dotenv()

def load_document(filename:str):
    print("Starting Ingestion .....")
    
    with open(file=filename,mode="r",encoding="utf-8") as f:
        file_content = f.read()
        
    document = Document(page_content=file_content,metadata={"source":filename})
    
    print("Spliting Document ......")
    
    text_spliter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=0)
    
    texts = text_spliter.split_documents([document])
    
    print("Embeddings ......")
    embeddings = OpenAIEmbeddings()
    # resultant_embeddings = embeddings.embed_documents([text.page_content for text in texts[0:5]])
    print("Storing in Db......")
    db_engine = PGEngine.from_connection_string(url="postgresql+psycopg://postgres:password@localhost:6024/vectordb")
    PGVectorStore.afrom_documents(documents=texts,embedding=embeddings,engine=db_engine,table_name="my_vector_collection")
    print("Ready ........")
load_document("Day-5/RAG/docs/apple.txt")