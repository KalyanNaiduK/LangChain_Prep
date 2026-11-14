from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVectorStore,PGEngine
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-5")
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
        
def format_docs(question):
    
    db_engine = PGEngine.from_connection_string(url="postgresql+psycopg://postgres:password@localhost:5432/vectordb")
    vector_store = PGVectorStore.create_sync(engine=db_engine,embedding_service=OpenAIEmbeddings(),table_name="my_vector_collection_v2")
    
    retiver = vector_store.as_retriever(search_kwargs={"k": 6})
    docs = retiver.invoke(question)
    
    final_docs=""
    for doc in docs:
        final_docs+=doc.page_content
        
    return final_docs


def retriver_with_out_lecl(user_question:str):

    template = [{"role":"system","content":"you are a help full assistant"},{"role":"user","content": "question:{user_query} Docs: {information}"}]
    prompt_template = ChatPromptTemplate.from_messages(template)
    
    documents_info = format_docs(user_question)
    
    final_prompt = prompt_template.invoke({"user_query":user_question,"information":documents_info})
    
    response = llm.invoke(final_prompt)
    
    print("Final Reposnse \n")
    print("======="*10)
    print((response.content))
    
retriver_with_out_lecl("Tell me about Sai in 50 words , how much do you rate him for a Software engineering position.")