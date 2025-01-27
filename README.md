# Web-operator

A library for automating web tasks

To learn more about the library, check out the [documentation 📕]

## Installation

1. Setup conda enviornment

2. Web-operator and playwright instllation

    ```
    python -m pip install web-operator

    playwright install
    ```

3. Environment Setup

    This guide explains how to set up and manage environment variables for your project using python-dotenv.

    a. Install the python-dotenv library using pip:

    ```
    pip install python-dotenv
    ```
    b. Create a .env file in your project's root directory with the following structure:
    ```
    OPENAI_API_KEY=your_openai_api_key

    # Only add below config if you want to use the GOOGLE services
    GOOGLE_API_CREDS_LOC=your credentials.json file location
    GOOGLE_API_TOKEN_LOC=your token.json file location
    ```

    c. Add .env to your .gitignore file to prevent accidentally committing sensitive information:

    d. code for load environment variables 
    ```
    from dotenv import load_dotenv
    import os
    load_dotenv()
    ```

## Basic Usage 
1. Importing Required Modules
```
from web_operator.supervisor import Supervisor
from dotenv import load_dotenv
```
2. Initializing the Supervisor
The Supervisor class manages different web agents. We need to specify any agents that required tokens. All others are not needed to mention. 
```
load_dotenv()  # Load environment variables
token_required_agents = [] 
supervisor = Supervisor(token_required_agents=token_required_agents)
```
3. Web Search Operation
This example shows how to perform a search on DuckDuckGo:
```
prompt = """
    Go to https://duckduckgo.com, search for insurance usecases in connected vehicles using input box 
    you find from that page, click search button and return the summary of results you get. 
    Use fill tool to fill in fields and print out url at each step.
"""
supervisor.run(query=prompt)
```

## Basic Usage with token required agents like gmail
1. Make sure .env file has the location of the json file for authentication Google APIs (use this document that explain how can you get these files in the first place)
2. Initialize the supervisor and other required librarires
```
from web_operator.supervisor import Supervisor
from dotenv import load_dotenv

load_dotenv()  # Load environment variables
token_required_agents = ['gmail_agent']  # Specify token required agents
supervisor = Supervisor(token_required_agents=token_required_agents)
```
3. Gmail Email Processing
```
prompt = """
    go to gmail and find email with subject 'Open-Source Rival to OpenAI's Reasoning Model'
    We need only the content of the latest email of the above subject and disgard other emails.
    Extract the first URL (link) from the email content.
    Naviagte to the URL and summarise the content and no further navigation is required

    **Constraints:**
    - Only extract the first URL found in the email body.
    - If no URL is found, return "No URL found."
"""

supervisor.run(query=prompt)
```
