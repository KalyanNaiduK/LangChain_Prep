import requests
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from response_format.Country import NamePredictionResults
from dotenv import load_dotenv
from response_format.classifier import Classifier,get_name_map
load_dotenv()

@tool
def name_nationality_api(specified_name: str):
    """
    description: This function makes a GET request to the name nationality API "http://127.0.0.1:8000/items/{specified_name}" and returns the JSON response.

    Args:
        specified_name (str): The name to query for nationality information.

    Returns:
        dict: The JSON response from the API.
    """
    url = f"http://127.0.0.1:8000/items/{specified_name}"
    response = requests.get(url)
    return response.json()

messages = [{"role": "system", "content": """You are a helpful assistant. 
             You have access to a tool that can find nationality information based on a specified name."""},
            {"role": "user", "content": "{user_message}"}]

nationality_agent_prompt_template = ChatPromptTemplate.from_messages(messages)

user_msg = "tell me about the nationality of the names below: 'smith', 'dubois' ,'okafor', 'garcia', 'kim'"
final_prompt = nationality_agent_prompt_template.invoke({"user_message": user_msg})

nationality_agent = create_agent(model="gpt-5", tools=[name_nationality_api],response_format=NamePredictionResults)

nationality_agent_response = nationality_agent.invoke(final_prompt)

# print("Nationality Agent Response:", nationality_agent_response['structured_response'])
down_response = nationality_agent_response['structured_response']

Classifier(down_response)

print("Name Map:",get_name_map())