import openai
import os

# Set up OpenAI API key
api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = api_key

init_message = {"role": "system", "content": "you are a AI helper"}


def gpt_generator(response):
    for chunk in response:
        delta = chunk['choices'][0]['delta']
        if 'content' in delta:
            yield delta['content']


def mock_generator():
    for i in range(10):
        yield str(i)


# Function to send a message to the OpenAI chatbot model and return its response
def invoke_gpt(message_log, use_stream=False):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=1000,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.5,        # The "creativity" of the generated response (higher temperature = more creative)
        stream=use_stream,
        n=1
    )

    if use_stream:
        return gpt_generator(response)
    else:
        return response
    # return mock_generator()


# Function to send a message to the OpenAI chatbot model and return its response
def invoke_gpt3(prompt_value):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.Completion.create(
        model="text-davinci-003",  # The name of the OpenAI chatbot model to use
        prompt=prompt_value,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=200,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.1        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].text
   #  return """
   #  {
   # "searchMarket":
   #      [
   #      {"query": "地产股中表现最好的10支股票"},
   #      {"query": "今年涨幅超过2%的10支基金"}
   #      ]
   # }
   #  """
