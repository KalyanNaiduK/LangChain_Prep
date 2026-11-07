from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

def get_product_price(product_name:str) -> float:
    mock_prices = {
        "laptop": 2000.00,
        "mouse": 30.00,
        "keyboard": 40.00,
        "monitor": 190.00,
    }
    print("Running get_product_price tool")
    print("="*50+"\n")
    price = mock_prices.get(product_name.lower(), 0.0)
    print("Exiting get_product_price tool")
    print("="*50+"\n")
    return price

def get_discounted_price(product_cost:float,discount_tier:str) -> float:
    discount_rates = {
        "silver": 0.05,  # 5% discount
        "gold": 0.10,    # 10% discount
        "platinum": 0.15 # 15% discount
    }
    
    print("Running get_discounted_price tool")
    print("="*50+"\n")
    discount_rate = discount_rates.get(discount_tier.lower(), 0.0)
    discounted_price = product_cost * (1 - discount_rate)
    print("Exiting get_discounted_price tool")
    print("="*50+"\n")
    return discounted_price


tool_definitions = [
    {
        "type": "function",
        "name": "get_product_price",
        "strict": True,
        "description": "Fetches the price of a product given its name.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The name of the product."
                }
            },
            "required": ["product_name"],
            "additionalProperties":False
        }
    },
    {
        "type": "function",
        "name": "get_discounted_price",
        "strict":True,
        "description": "Calculates the discounted price of a product based on the discount tier.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_cost": {
                    "type": "number",
                    "description": "The original cost of the product."
                },
                "discount_tier": {
                    "type": "string",
                    "description": "The discount tier (e.g., 'silver', 'gold', 'platinum')."
                }
            },
            "required": ["product_cost", "discount_tier"],
            "additionalProperties":False
        }
    }
]

openAI_client = OpenAI()
MAX_ITERATIONS = 4

def run_query(user_query: str):
    input_messages = [{ "role": "system", "content": """You are a helpful assistant that can fetch product prices and
                          calculate discounted prices based on membership tiers.
                          You have access to the following tools:
                          1. get_product_price(product_name:str) -> float: Fetches the price of
                          a product given its name.
                          2. get_discounted_price(product_cost:float,discount_tier:str) ->
                          float: Calculates the discounted price of a product based on the discount tier.
                           Rules to follow:
                          - Donot assume the price of any product or the discount rates. Always use the tools to get accurate information.
                          - Always provide the final answer in a concise manner without any additional commentary.
                          - Always ask for the product name and discount tier if not provided in the user query.
                          """}]
    print(f"User Query: {user_query}")
    input_messages.append({"role": "user", "content": user_query})
    
    # for iteration in range(1, MAX_ITERATIONS + 1):
    # print(f"\nPreforming Iteration {iteration}:")
    
    for i in range(1,MAX_ITERATIONS+1):
        print(f"Running iteration {i}\n")
        print(f"="*50+"\n")
        ai_message = openAI_client.responses.create(
            model="gpt-5",
            input=input_messages,
            tools=tool_definitions)
        
        input_messages+=ai_message.output
        for item in ai_message.output:
            if item.type == "function_call":
                if item.name == "get_product_price":
                    product_name = json.loads(item.arguments)["product_name"]
                    tool_reponse = str(get_product_price(product_name))
                    
                    input_messages.append({
                        "type":"function_call_output",
                        "call_id":item.call_id,
                        "output":tool_reponse
                    })
                if item.name == "get_discounted_price":
                    product_cost = json.loads(item.arguments)["product_cost"]
                    discount_teir = json.loads(item.arguments)["discount_tier"]
                    tool_reponse = str(get_discounted_price(product_cost,discount_teir))
                    
                    input_messages.append({
                        "type":"function_call_output",
                        "call_id":item.call_id,
                        "output":tool_reponse
                    })
            if item.type=="message":
                final_response = ai_message.output_text
                print(f"Final Reponse :  {final_response}")
                return final_response
    print("Ending___")
    return "Max Itterations Limit Reached !!!"
        
if __name__ == "__main__":
    run_query("What is the price of a laptop with a gold membership?")