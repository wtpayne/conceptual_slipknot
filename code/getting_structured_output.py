import json
from mistralai import Mistral

api_key = "pqmKVrIjJjkKQMhvRslPapP7QzNV2A1I"
model = "pixtral-12b-2409"
client = Mistral(api_key=api_key)

# Step 1: Image analysis
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

chat_response = client.chat.complete(
    model=model,
    messages=messages,
    response_format={"type": "json_object"}
)

response_json = json.loads(chat_response.choices[0].message.content)
print('Raw response content:', json.dumps(response_json, indent=2))

# Step 2: Generate correlations
new_object = 'apple'
existing_objects = response_json['important_objects']
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

correlation_response = client.chat.complete(
    model=model,
    messages=correlation_prompt,
    response_format={"type": "json_object"}
)

correlation_json = json.loads(correlation_response.choices[0].message.content)
print('\nCorrelated Response:', json.dumps(correlation_json, indent=2))

# Step 3: Generate haikus
haikus = []

for i in range(3):
    existing_object = correlation_json['correlations'][i]['existing_object']
    correlation_reason = correlation_json['correlations'][i]['correlation_reason']
    
    if i == 0:
        haiku_prompt = [
            {
                "role": "user",
                "content": f"""Write a haiku inspired by the correlation between an {new_object} and the {existing_object}, 
in the context of this image description: "{response_json['description']}".
The haiku should reflect this idea: {correlation_reason}.
Before the haiku, mention 'Haiku 1:' on a separate line."""
            }
        ]
    else:
        haiku_prompt = [
            {
                "role": "user",
                "content": f"""Continue the story from the previous haiku:
{haikus[-1]}

Write the next haiku building upon this theme, incorporating the {new_object} and the {existing_object} from the image.
The haiku should reflect this idea: {correlation_reason}.
Before the haiku, mention 'Haiku {i+1}:' on a separate line."""
            }
        ]

    haiku_response = client.chat.complete(
        model=model,
        messages=haiku_prompt,
        response_format={"type": "text"}
    )

    haikus.append(haiku_response.choices[0].message.content)

print('\nGenerated Haikus:')
for i, haiku in enumerate(haikus):
    print(f"Significant object for Haiku {i+1}: {correlation_json['correlations'][i]['existing_object']}")
    print(haiku)
    print()

# Step 4: Explain the connection between haikus
connection_prompt = [
    {
        "role": "user",
        "content": f"""Given these three haikus:

{haikus[0]}

{haikus[1]}

{haikus[2]}

Explain how these haikus are connected to each other while maintaining the central theme of the {new_object} in relation to the image of {response_json['description']}. 
Provide a brief analysis of the narrative flow and thematic consistency across the three haikus."""
    }
]

connection_response = client.chat.complete(
    model=model,
    messages=connection_prompt,
    response_format={"type": "text"}
)

print('\nConnection between the haikus:')
print(connection_response.choices[0].message.content)
