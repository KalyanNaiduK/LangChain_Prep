from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage,HumanMessage,ToolMessage
from langchain.tools import tool
from dotenv import load_dotenv
load_dotenv()

@tool
def get_product_price(product_name:str) -> float:
    """
    Fetches the price of a product given its name.

    Args:
        product_name (str): The name of the product.

    Returns:
        float: The price of the product.
    """
    mock_prices = {
        "laptop": 2000.00,
        "mouse": 30.00,
        "keyboard": 40.00,
        "monitor": 190.00,
    }
    print("Running get_product_price tool")
    print("="*50)
    return mock_prices.get(product_name.lower(), 0.0)

@tool
def get_discounted_price(product_cost:float,discount_tier:str) -> float:
    """
    Calculates the discounted price of a product based on the discount tier.

    Args:
        product_cost (float): The original cost of the product.
        discount_tier (str): The discount tier (e.g., "silver", "gold", "platinum").

    Returns:
        float: The discounted price of the product.
    """
    discount_rates = {
        "silver": 0.05,  # 5% discount
        "gold": 0.10,    # 10% discount
        "platinum": 0.15 # 15% discount
    }
    
    discount_rate = discount_rates.get(discount_tier.lower(), 0.0)
    discounted_price = product_cost * (1 - discount_rate)
    
    print("Running get_discounted_price tool")
    print("="*50)
    return discounted_price


tools = [get_product_price, get_discounted_price]

tools_dict = {tool.name: tool for tool in tools}

model = "gpt-5"
MAX_ITERATIONS = 10

chat_model = init_chat_model(model=f"openai:{model}")
chat_model_with_tools = chat_model.bind_tools(tools)



def run_query(user_query: str):
    messages = [SystemMessage(content="""You are a helpful assistant that can fetch product prices and
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
                          """)]
    print(f"User Query: {user_query}")
    messages.append(HumanMessage(content=user_query))
    
    for iteration in range(1, MAX_ITERATIONS + 1):
    
        print(f"\nPreforming Iteration {iteration}:")
    
        ai_message = chat_model_with_tools.invoke(messages)
        
        if not ai_message.tool_calls:
            print("="*50)
            response = ai_message.content
            print(f"\n Final Response: {response}")
            return response
                    
        tool_call = ai_message.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args_dict = tool_call["args"]
        tool_func = tools_dict.get(tool_name)
        tool_response = tool_func.invoke(tool_args_dict)
        tool_id = tool_call["id"]
        messages.append(ai_message)
        messages.append(ToolMessage(content=str(tool_response),tool_call_id=tool_id))
        
    else:
        print("Max iterations reached without a final response.")
        return "Unable to provide a final response after maximum iterations."


if __name__ == "__main__":
    print("Running the layer 1 ReAct agent\n")
    print("="*50)
    final_response = run_query("What is the price of a keyboard with a platinum membership?")
    