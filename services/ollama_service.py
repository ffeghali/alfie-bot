import functools
import typing
import asyncio
import ollama

def to_thread(func: typing.Callable) -> typing.Coroutine:
    """Decorator to run a blocking function in a separate thread."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

@to_thread
def get_response(system_content, user_content):
    """Fetches a response from the Ollama model."""
    response = ollama.chat(model='llama3.2', messages=[
        {
            'role' : 'system',
            'content' : system_content
        },
        {
            'role': 'user',
            'content': user_content,
        },
    ])
    return response['message']['content'] 


@to_thread
def ollama_classify(system_content, input_text, categories):
    """
        Classifies input text based on provided categories.
        TODO fix this method, there is no way to classify with the chat api atm
    """
    response = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'system', 
            'content': system_content},
        {
            'role': 'user', 
            'messages': [{'type': 'input', 'text': input_text}], 
        }
    ])
    return response['message']['content'] 