from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_postgres import PGEngine,PGVectorStore
from dotenv import load_dotenv

load_dotenv()
template = [{"role":"system","content":"you are a help full assistant, answer the following question based on the context only"},
            {"role":"user","content": "question:{user_query} Docs: {information}"}]
prompt_template = ChatPromptTemplate.from_messages(template)

llm = ChatOpenAI(model="gpt-5")

embeddingEngine  = OpenAIEmbeddings()
dbEngine = PGEngine.from_connection_string(url="postgresql+psycopg://postgres:password@localhost:5432/vectordb")
vector_store = PGVectorStore.create_sync(engine=dbEngine,embedding_service=embeddingEngine,table_name="my_vector_collection_v2")

retriver = vector_store.as_retriever(search_kwargs={"k":3})

def fomat_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def create_retriveal_chain_with_lecl():
    
    
    info_chain = RunnablePassthrough.assign(
                        information = itemgetter("user_query")| retriver | fomat_docs
                        )
    # print(info_chain)
    retirval_chain = (info_chain | prompt_template | llm | StrOutputParser())
    
    return retirval_chain


retriver_chain = create_retriveal_chain_with_lecl()
response = retriver_chain.invoke({"user_query":"Tell me about Sai in 50 words , how much do you rate him for a Software engineering position."})
print(response)