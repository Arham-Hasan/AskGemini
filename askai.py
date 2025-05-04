import google.generativeai as genai
import yaml

# Read config file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

MESSAGE_SYSTEM_CONTENT = """You are a customer service agent that helps a customer with answering questions. 
Please answer the question based on the provided context below. 
Make sure not to make any changes to the context, if possible, when preparing answers to provide accurate responses. 
If the answer cannot be found in context, just politely say that you do not know, do not try to make up an answer."""

# Configure the Gemini API key
genai.configure(api_key=config['API_KEY'])

model = genai.GenerativeModel("gemini-2.0-flash-lite")

def get_response_with_cached_context(question: str, context: str):
    # Convert context to string if it's a list/dict
    if isinstance(context, (list, dict)):
        context = str(context)
    
    # Create chat with system message and context
    chat = model.start_chat()
    chat.send_message(MESSAGE_SYSTEM_CONTENT)
    chat.send_message(f"Context: {context}")
    response = chat.send_message(question)
    return response.text