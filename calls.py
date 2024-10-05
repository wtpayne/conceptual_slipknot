import json
import textwrap
import os
import dotenv
import mistralai
from requests.exceptions import RequestException
import ssl
import streamlit as st

dotenv.load_dotenv()
THEME_DEFAULT = 'heavy industry'
API_KEY_MISTRAL = os.getenv('API_KEY_MISTRAL')
ID_MODEL_MULTIMODAL = 'pixtral-12b-2409'
ID_MODEL_CHAT = 'mistral-large-latest'
client = mistralai.Mistral(api_key=API_KEY_MISTRAL)

def _generate_poem(concept, theme, url):
    """
    Generate a poem about an image.

    """
    # Combine previous responses to create context, excluding None values
    previous_context = "\n".join(
        filter(None, st.session_state.responses)  # Only include non-None responses
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

def _critique_poem(new_poem, page_index, all_responses):
    """
    Critique the poem using the language model, taking into account all existing poems.
    """
    context = "\n".join([f"Page {i+1} poem: {poem}" if poem else f"Page {i+1} poem: Not generated yet" 
                         for i, poem in enumerate(all_responses)])
    
    prompt = f"""
    Evaluate the following new poem in the context of the existing collection of poems. 
    Respond only with "yes" or "no".

    Current collection state:
    {context}

    New poem for Page {page_index + 1}:
    {new_poem}

    Criteria:
    - The new poem should fit well with the existing collection.
    - Consider the overall flow and coherence of the collection.

    Is this new poem good enough to be added to the collection? (yes/no). Be smart about stuff and do not accept bad poems.

    """
    try:
        output = _generate_text(prompt)  # Use your existing _generate_text function
        return output.strip().lower()  # Normalize the response to lowercase for comparison
    except (ssl.SSLError, RequestException) as e:
        st.error(f"Network error occurred: {str(e)}. Please try again.")
        return None

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