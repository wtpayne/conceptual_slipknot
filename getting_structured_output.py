import json
from mistralai import Mistral

# Retrieve the API key from environment variables
api_key = "8QNoSTjzgWWqnx1MgehPI7NUSwDLNHGq"

# Specify model
model = "pixtral-12b-2409"

# Initialize the Mistral client
client = Mistral(api_key=api_key)

# Step 1: Image analysis to get existing objects
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

print('#############')
print('Chat Response')
print('#############')
print()

# Get the chat response for the first message (image analysis)
chat_response = client.chat.complete(
    model=model,
    messages=messages,
    response_format={
        "type": "json_object"
    }
)

# Parse the response to extract important objects
response_json = json.loads(chat_response.choices[0].message.content)
print('Raw response content:', json.dumps(response_json, indent=2))

# Step 2: Generate correlations between the new object and existing objects
new_object = 'apple'
existing_objects = response_json['important_objects']

# Prepare a prompt for generating correlations
existing_object_names = ', '.join([obj['name'] for obj in existing_objects])

correlation_prompt = [
    {
        "role": "user",
        "content": f"""Given the following objects from the image: {existing_object_names}, 
and a new object: {new_object}, generate correlations between the new object and each of the existing objects. 
Please provide a reason for each correlation in JSON format.

Example format:
{{
  "new_object": "apple",
  "correlations": [
    {{
      "existing_object": "Snow",
      "correlation_reason": "Both are associated with winter."
    }},
    {{
      "existing_object": "Eiffel Tower",
      "correlation_reason": "The apple and Eiffel Tower are both iconic in their fields."
    }}
  ]
}}"""
    }
]

# Get the chat response for the second prompt (generating correlations)
correlation_response = client.chat.complete(
    model=model,
    messages=correlation_prompt,
    response_format={
        "type": "json_object"
    }
)

# Parse the response to extract correlations
correlation_json = json.loads(correlation_response.choices[0].message.content)

print()
print('####################')
print('Correlated Response:')
print('####################')
print()

print(json.dumps(correlation_json, indent=2))

# Step 3: Prepare a prompt to generate a metaphorical haiku based on the correlation
# Assuming the best correlation is with the Eiffel Tower
best_correlation = correlation_json['correlations'][1]  # You can change the index if needed

# Extracting existing_object and correlation_reason from best_correlation
existing_object = best_correlation['existing_object']
correlation_reason = best_correlation['correlation_reason']

haiku_prompt = [
    {
        "role": "user",
        "content": f"""Write a haiku inspired by the correlation between an {new_object} and the {existing_object}. 
The haiku should reflect the idea that both are iconic in their fields, one in nature and the other in architecture. 
Here's the correlation reason for inspiration: {correlation_reason}."""
    }
]

# Get the chat response for generating the haiku
haiku_response = client.chat.complete(
    model=model,
    messages=haiku_prompt,
    response_format={
        "type": "text"
    }
)

# Print the generated haiku
print()
print('###############')
print('Generated Haiku:')
print('###############')
print()

print(haiku_response.choices[0].message.content)
