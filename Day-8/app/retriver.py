from dotenv import load_dotenv
from langchain.messages import ToolMessage
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGEngine, PGVectorStore

load_dotenv()

def init_db():
    embeddingEngine = OpenAIEmbeddings(model="text-embedding-3-small",chunk_size=50,retry_min_seconds=10)
    dbEngine = PGEngine.from_connection_string(url="postgresql+psycopg://postgres:password@localhost:5432/vectordb")
    vector_store = PGVectorStore.create_sync(engine=dbEngine,embedding_service=embeddingEngine,table_name="my_vector_collection_v3")
    return vector_store 

store = init_db()

def pushArtifactsToDownstreamService(artifacts):
    print("***"*15)
    print("Starting to log sources ............")
    print("***"*15)
    sources = "\n\n".join([document.metadata['source'] for document in artifacts])
    with open("sources.txt","w") as f:
        f.write(sources)
        
    print("***"*15)
    print("Logged Sources Successfully!!!!")
    print("***"*15)


@tool(response_format="content_and_artifact")
def search_for_documentations(query:str):
    """
    This is a tool to queries for text documentations indexed in vector database which can return context for passed query
    
    Args:
        query (str): The search query/sentence you want to search for.
    """
    results  = store.as_retriever(search_kwargs={"k": 4}).invoke(input=query)
    strutured_docs = "".join((f"source:{res.metadata['source']}\n\n"+res.page_content for res in results))
    
    return strutured_docs,results

def run_llm(Question:str):

    system_template = SystemMessagePromptTemplate.from_template("""You are a helpfull assisitant how has access to knowledge base of langchain 
                                                                documentations, You have the tools provided to search for the documentations user
                                                                asked and set you context first and the answer the user question in the requested style below
                                                                style -> {style}""")
    
    human_template = HumanMessagePromptTemplate.from_template("My questions is : {query}")
    final_template = ChatPromptTemplate.from_messages([system_template,human_template])
    
    final_prompt = final_template.invoke({"style":"concise bullet list","query":Question})

    agent = create_agent(model="gpt-5",tools=[search_for_documentations])    

    result = agent.invoke(final_prompt)
    print("====="*15)
    print(result['messages'][-1].content)
    print("====="*15)

    for mesType in result['messages']:
        if isinstance(mesType,ToolMessage):
            pushArtifactsToDownstreamService(mesType.artifact)

run_llm("What are deep agents in langchain ? ")