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
import partialjson
import streamlit


dotenv.load_dotenv()
THEME_DEFAULT       = 'heavy industry'
URL_DEFAULT         = 'https://i.etsystatic.com/7450813/r/il/bbdfb2/1138370933/il_570xN.1138370933_b4pi.jpg'
API_KEY_MISTRAL     = os.getenv('API_KEY_MISTRAL')
ID_MODEL_MULTIMODAL = 'pixtral-12b-2409'
ID_MODEL_CHAT       = 'mistral-large-latest'


# -----------------------------------------------------------------------------
def main(argv: list[str] | None = None):
    """
    Main function.

    """

    if argv is None:
        argv = sys.argv

    engine = ConceptEngine()

    str_url = streamlit.text_input(
        'Enter the URL of the image',
        value = URL_DEFAULT)
    if not str_url:
        streamlit.stop()
    streamlit.image(str_url)

    count_iter = streamlit.number_input(
        'Enter the number of iterations',
        min_value = 1,
        max_value = 30,
        value     = 3)



    if streamlit.button('Generate poem'):

        concept = engine.seed()

        for iter in range(count_iter):

            streamlit.write(f'Iteration: {iter}')

            if iter >= 1:
                method = engine.plan(concept)
                streamlit.write(f'Method: {method}')
                concept = engine.step(concept, method)

            streamlit.write(f'Concept: {concept}')
            theme = random.choice(engine.theme(concept, url = str_url))
            streamlit.write(f'Theme: {theme["name"]}')
            streamlit.write(f'Significance: {theme["significance"]}')
            poem = engine.poem(concept, theme, url = str_url)
            streamlit.write(f'Poem: {poem}')
            streamlit.divider()



# =============================================================================
class ConceptEngine:
    """
    Concept engine.

    """

    # -------------------------------------------------------------------------
    def __init__(
            self,
            client: mistralai.Mistral | None = None,
            parser: partialjson.json_parser.JSONParser | None = None):
        """
        Return a ConceptEngine instance.

        """

        if client is None:
            client = mistralai.Mistral(api_key = API_KEY_MISTRAL)
        if parser is None:
            parser = partialjson.json_parser.JSONParser()

        self.client = client
        self.parser = parser

    # -------------------------------------------------------------------------
    def seed(self):
        """
        Return a random seed concept.

        """
        return self._textual(
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
            json = True).get('concept', None)

    # -------------------------------------------------------------------------
    def plan(self, concept):
        """
        Generate a plan.

        """

        return self._textual(
            f"""
            Select one of the following methods to explore <concept> further.
            
            * Concept Expansion
            * Metaphorical Reframing
            * Context Switching
            * Contrastive Prompts
            * Boundary Testing
            * Blending

            <concept>
            {concept}
            <concept>

            example output format:
            {{
                "method": "Concept Expansion"
            }}
            """,
            json = True).get('method', None)
        
    # -----------------------------------------------------------------------------
    def step(self, concept, method):
        """
        Take the next step in the plan.

        """

        return self._textual(
            f"""
            Starting with <concept>, apply <method> to generate a new concept.

            <concept>
            {concept}
            <concept>

            <method>
            {method}
            <method>
            
            example output format:
            {{
                "concept": "stillness"
            }}
            """,
            json = True).get('concept', None)

    # -------------------------------------------------------------------------
    def theme(self, concept, url):
        """
        Return a list of themes common to image and concept.

        """

        return self._multimodal(
            f"""
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
            json = True).get('themes', None)

    # -----------------------------------------------------------------------------
    def poem(self, concept, theme, url):
        """
        Generate poem from concept, theme and image.

        """
        return self._multimodal(
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
            url  = url,
            json = False)

    # -------------------------------------------------------------------------
    def _textual(self, prompt: str, json: bool = False) -> str | dict:
        """
        Generate from text.

        """

        prompt = textwrap.dedent(prompt)
        kwargs = dict(
            model    = ID_MODEL_CHAT,
            messages = [{'role': 'user', 'content': prompt }])
        if json:
            kwargs['response_format'] = { 'type': 'json_object' }

        return self._parse(
            self.client.chat.complete(**kwargs).choices[0].message.content)

    # -------------------------------------------------------------------------
    def _multimodal(self, prompt: str, url: str, json: bool = False) -> str:
        """
        Generate from multimodal input.

        """

        prompt = textwrap.dedent(prompt)
        kwargs = dict(
            model    = ID_MODEL_MULTIMODAL,
            messages = [{'role':    'user',
                        'content': [{ 'type': 'text',      'text': prompt },
                                    { 'type': 'image_url', 'image_url': url }]}])
        if json:
            kwargs['response_format'] = { 'type': 'json_object' }

        return self._parse(
            self.client.chat.complete(**kwargs).choices[0].message.content)

    # -------------------------------------------------------------------------
    def _parse(self, text: str) -> dict | list | str:
        """
        Parse text which may or may not be JSON.

        """

        try:
            return self.parser.parse(text)
        except:
            return text




















# -----------------------------------------------------------------------------
if __name__ == '__main__':
    sys.exit(main())
