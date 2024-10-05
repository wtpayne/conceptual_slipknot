import os
from mistralai import Mistral

# Retrieve the API key from environment variables
api_key = "8QNoSTjzgWWqnx1MgehPI7NUSwDLNHGq"

# Specify model
model = "pixtral-12b-2409"

# Initialize the Mistral client
client = Mistral(api_key=api_key)

# Define the messages for the chat
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": """Analyze this image and provide a structured output. Include a description of the scene and a list of all visible objects. Return the result as a JSON object.

Example output format:
{
  "description": "nice photo",
  "important_objects": [
    {
      "name": "Rock",
      "significance": "It is fancy"
    }
  ]
}"""
            },
            {
                "type": "image_url",
                "image_url": "https://tripfixers.com/wp-content/uploads/2019/11/eiffel-tower-with-snow.jpeg"
            }
        ]
    }
]

# Get the chat response
chat_response = client.chat.complete(
    model=model,
    messages=messages,
    response_format={
        "type": "json_object"
    }
)

# Print the content of the response
print(chat_response.choices[0].message.content)
