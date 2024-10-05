#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Conceptual Slipknot demo.

"""

import json
import os
import sys
import textwrap
import random

import dotenv
import mistralai
import streamlit


dotenv.load_dotenv()
THEME_DEFAULT       = 'heavy industry'
URL_DEFAULT         = 'https://i.etsystatic.com/7450813/r/il/bbdfb2/1138370933/il_570xN.1138370933_b4pi.jpg'
API_KEY_MISTRAL     = os.getenv('API_KEY_MISTRAL')
ID_MODEL_MULTIMODAL = 'pixtral-12b-2409'
ID_MODEL_CHAT       = 'mistral-large-latest'
client              = mistralai.Mistral(api_key = API_KEY_MISTRAL)


# -----------------------------------------------------------------------------
def main(argv: list[str] | None = None):
    """
    Main function.

    """

    if argv is None:
        argv = sys.argv

    str_url = streamlit.text_input(
        'Enter the URL of the image',
        value = URL_DEFAULT)
    if not str_url:
        streamlit.stop()
    streamlit.image(str_url)

    # str_theme = streamlit.text_input(
    #     'Enter the theme',
    #     value = THEME_DEFAULT)

    if streamlit.button('Generate poem'):
        str_poem = generate_poem(url = str_url)
        streamlit.write(str_poem)

# -----------------------------------------------------------------------------
def generate_poem(url):
    """
    Generate a poem about an image.

    """
 
    concept    = _random_concept()
    list_theme = _common_themes(concept, url)
    theme      = random.choice(list_theme)
    
    return _caption_image(
        f"""
        Write a 5-line poem about this image using the
        <concept> and common <theme> below. Do NOT use
        explicit words related to the <theme>.

        <concept>
        {concept}
        <concept>

        <theme>
        {theme['name']}: {theme['significance']}
        <theme>
        """,
        url = url)


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
        json = True)
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
    json_themes =  _caption_image(
        prompt = f"""
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
        url  = url,
        json = True)
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
        model    = ID_MODEL_CHAT,
        messages = [{'role': 'user', 'content': prompt }])
    if json:
        kwargs['response_format'] = { 'type': 'json_object' }
    return client.chat.complete(**kwargs).choices[0].message.content


# -----------------------------------------------------------------------------
def _caption_image(prompt: str, url: str, json: bool = False) -> str:
    """
    Caption an image.

    """

    prompt = textwrap.dedent(prompt)
    kwargs = dict(
        model    = ID_MODEL_MULTIMODAL,
        messages = [{'role':    'user',
                     'content': [{ 'type': 'text',      'text': prompt },
                                 { 'type': 'image_url', 'image_url': url }]}])
    if json:
        kwargs['response_format'] = { 'type': 'json_object' }
    return client.chat.complete(**kwargs).choices[0].message.content


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    sys.exit(main())
