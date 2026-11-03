from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()
model = ChatOpenAI(model_name="gpt-5")
system_message = "You are a helpful assistant that translates natural language into SQL queries."
user_message_template = "Information: {information}\n\n" + "Please provide the SQL query based on the above information."

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_message),
        ("user", user_message_template)
    ]
)

chain = prompt_template | model

def r_info(filename)->str:
    with open(filename, "r") as file:
        return file.read()

reterived_infromation = r_info(filename="Day-1/queries/query.md")

result = chain.invoke(input={"information": reterived_infromation})

print(result.content)
