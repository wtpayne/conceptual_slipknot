import base64
import json
import textwrap
import os
import dotenv
import mistralai
import streamlit


def _load_image_as_base64(file_path):
    """
    Convert local image to base64 string.

    """
    with open(file_path, "rb") as image_file:
        return f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"

# -----------------------------------------------------------------------------
def _generate_poem(concept, theme, url):
    """
    Generate a poem about an image.

    """
    # Combine previous responses to create context, excluding None values
    previous_context = "\n".join(
        filter(None, streamlit.session_state.responses)  # Only include non-None responses
    )
    return _caption_image(
        f"""
        Write a haiku about this image using the
        <concept> and common <theme> below. Do NOT use
        explicit words related to the <theme>.

        Previous context:
        {previous_context}

        <concept>
        {concept}
        <concept>

        <theme>
        {theme['name']}: {theme['significance']}
        <theme>
        """,
        url=url,
        json=False)

# -----------------------------------------------------------------------------
def _random_concept():
    """
    Return a randomly generated concept.

    """
    output = _generate_text(
        f"""
        Generate a random 1-word concept. First, think
        step by step using a random wikipedia article.
        Then, extract a concept from that article. Return
        the result as a JSON object.

        Example output format:
        {{
          "reasoning": "A spring is a natural exit point at which groundwater emerges from the aquifer and flows onto the top of the Earth's crust (pedosphere) to become surface water. "
          "concept":  "crust"
        }}
        """,
        json=True)
    try:
        result = json.loads(output)
        return result['concept']
    except:
        return None

# -----------------------------------------------------------------------------
def _common_themes(concept, url):
    """
    Get the common themes of an image.

    """
    json_themes = _caption_image(
        prompt=f"""
            Extract 5 common themes that link the image with <concept>. 
            Return the result as a JSON object.

            <concept>
            {concept}
            </concept>

            Example output format:
            {{
                "themes": [
                    {{
                        "name": "stillness",
                        "significance": "the stillness of a winter scene"
                    }}
                ]
            }}

            """,
        url=url,
        json=True)
    try:
        result = json.loads(json_themes)
        return result['themes']
    except:
        return None

# -----------------------------------------------------------------------------
def _generate_text(prompt: str, json: bool = False) -> str:
    """
    Generate text from a prompt.

    """
    prompt = textwrap.dedent(prompt)
    kwargs = dict(
        model=ID_MODEL_CHAT,
        messages=[{'role': 'user', 'content': prompt}])
    if json:
        kwargs['response_format'] = {'type': 'json_object'}
    return client.chat.complete(**kwargs).choices[0].message.content

# -----------------------------------------------------------------------------
def _caption_image(prompt: str, url: str, json: bool = False) -> str:
    """
    Caption an image.

    """
    prompt = textwrap.dedent(prompt)
    kwargs = dict(
        model=ID_MODEL_MULTIMODAL,
        messages=[{'role': 'user',
                   'content': [{'type': 'text', 'text': prompt},
                               {'type': 'image_url', 'image_url': url}]}])
    if json:
        kwargs['response_format'] = {'type': 'json_object'}
    return client.chat.complete(**kwargs).choices[0].message.content

# -----------------------------------------------------------------------------

dotenv.load_dotenv()
THEME_DEFAULT = 'heavy industry'
API_KEY_MISTRAL = os.getenv('API_KEY_MISTRAL')
ID_MODEL_MULTIMODAL = 'pixtral-12b-2409'
ID_MODEL_CHAT = 'mistral-large-latest'
client = mistralai.Mistral(api_key=API_KEY_MISTRAL)

URLS = [
    '/Users/ssk/Downloads/conceptual_slipknot/images/frog.jpeg',
    '/Users/ssk/Downloads/conceptual_slipknot/images/lion.jpeg',  # Replace with your second image URL
    '/Users/ssk/Downloads/conceptual_slipknot/images/zebra.jpeg'  # Replace with your third image URL
]

# Initialize session state for responses if it doesn't exist
if 'responses' not in streamlit.session_state:
    streamlit.session_state.responses = [None] * len(URLS)  # Initialize with None for each page