import os
from dotenv import load_dotenv
# import google.generativeai as genai
import json
import pprint as pprint
from langchain_community.agent_toolkits.json.base import create_json_agent
from langchain_community.agent_toolkits.json.toolkit import JsonToolkit
from langchain_community.tools.json.tool import JsonSpec
from langchain_google_genai import ChatGoogleGenerativeAI


# Step 1: Load environment variables
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash",api_key=os.getenv("Google_API_KEY"))


# Load the JSON data
# file = "students_details.json"
file = "data.json"

with open(file, "r") as f1:
    data = json.load(f1)

# pprint(data)

# Create JSON spec and toolkit
spec = JsonSpec(dict_=data, max_value_length=500)

toolkit = JsonToolkit(spec=spec)

# Create the JSON agent with the Gemini LLM
# agent = create_json_agent(llm=model, toolkit=toolkit, max_iterations=1000, verbose=True)
agent = create_json_agent(llm=model, toolkit=toolkit, verbose=True,max_iterations=2000, max_execution_time=300,handle_parsing_errors=True,input_variables=['data'])

'''nested_keys: Specifying that students is a nested key.
keys_to_ignore:

Type: list[str]
Description: A list of keys in the JSON data that should be ignored by the agent or tools. This is useful if there are certain parts of the JSON that are irrelevant or should be excluded from processing.

keys_to_include:

Type: list[str]
Description: A list of keys that should be specifically included for processing. This attribute allows you to focus on only the relevant parts of the JSON data.
'''

# Run the agent with a query
# print(agent.run("how many students are there?"))
while (True):
    try:
        user_prompt = input("Ask something: ")
        if user_prompt.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        print(agent.run(user_prompt))

    except Exception as e:
        print(f"An error occurred: {e}")