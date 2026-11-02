# Agent with custom tool implementation with @tool decorator from langchain.agents import tool
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient
load_dotenv()

tavily = TavilyClient(api_key="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")
tavilyresults=[]
@tool
def find_user_info(user_id: str) -> dict:
    """
    Custom tool to find user information based on user ID.
    
    Args:
        user_id (str): The ID of the user to look up.
        
    Returns:
        dict: A dictionary containing user information.
    """
    # Simulated database of users
    user_database = {
        "1": {"name": "Alice", "age": 30, "email": "alice@example.com"},
        "2": {"name": "Bob", "age": 25, "email": "bob@example.com"},
        "3": {"name": "Charlie", "age": 35, "email": "charlie@example.com"},
        "4": {"name": "David", "age": 40, "email": "david@example.com"},
        "5": {"name": "Eve", "age": 28, "email": "eve@example.com"}
    }
    return user_database.get(user_id, {"error": "User not found"})

@tool
def search_internet(search_query: str) -> dict:
    """
    Custom tool to gives access to search functionality for the internet and find any topics or information.
    
    Args:
        search_query (str): The query string you want to pass to search to look up any information on internet.
        
    Returns:
        dict: A dictionary containing search results.
    """
    print(search_query + "\n")
    tavily_response = tavily.search(query=search_query)
    tavilyresults.append(tavily_response)
    return tavily_response




Agent = create_agent(model = "gpt-5",tools = [find_user_info, search_internet])

messages = [{"role":"system","content":"""You are a helpful assistant. 
             You have access to a tool that can find user information based on user ID,You have access to a tool that can search the internet for other information."""},
            {"role":"user","content":"{user_message}"}
]

prompt_template = ChatPromptTemplate.from_messages(messages)

user_input = "tell me about the user with ID 5 and also tell me about the latest news on AI technology in 50 words"
final_prompt = prompt_template.invoke({"user_message": user_input})
agent_response = Agent.invoke(final_prompt)
print(agent_response.get("messages")[-1].content)