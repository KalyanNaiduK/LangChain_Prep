from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVectorStore,PGEngine
from dotenv import load_dotenv
load_dotenv()

def retrive(query:str):
    db_engine = PGEngine.from_connection_string(url="postgresql+psycopg://postgres:password@localhost:5432/vectordb")
    vector_store = PGVectorStore.create_sync(engine=db_engine,embedding_service=OpenAIEmbeddings(),table_name="my_vector_collection",
    schema_name="public")
    retrived_documents  =  vector_store.similarity_search_with_score("what back-end frameworks sai know ?")
    i=0
    for document, score in retrived_documents:
        print(document.page_content)
        print("Score:", score)
        i+=1
        print(i)
        print("-----------------"*25)