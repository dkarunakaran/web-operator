from openai import OpenAI
from web_operator.nodes.computer_use_node import ComputerUseNode
from transformers import AutoTokenizer, AutoModelForCausalLM
from web_operator.nodes import router_node
import os
from dotenv import load_dotenv


load_dotenv()  

if not os.environ.get("OPENAI_API_KEY"):
    raise KeyError("OPENAI API token is missing, please provide it .env file.") 


computerUseNode = ComputerUseNode()

query1 = "Open a web browser and naviagate to scholar.google.com"
query2 = "Search for 'OpenAI' in the search bar"
query3 = "go to gmail using google API and read the email titles 'test'"
query4 = "Open the settings in the os and set volume to zero"
query5 = "Open a firefox web browser and  go to sportsbet.com"
user_query = query5

#tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")
#model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")
"""
client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)
"""

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

completion = client.chat.completions.create(
    #model="llama3.1:latest",
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": """
         You are a supervisor and tasked to select the right node for further automation. 
         You have two nodes: computer_use_node and api_operation_node.
         Given, the user prompt select the right node. 
         If there is no right match, then don't return any node.
         """
        },
        {
            "role": "user", "content": [
            {"type":"text", "text":user_query},
            ]
        }
    ],
    tools = router_node.tools
)

node_selected = completion.choices[0].message.tool_calls
print(node_selected)
if node_selected:
    node_name = node_selected[0].function.name
    if node_name == 'computer_use_node':
        # Example usage
        computerUseNode.run(user_query=user_query)
else:
    print("No tools are selected")


