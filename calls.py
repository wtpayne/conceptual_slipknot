import json
import textwrap
import os
import dotenv
import mistralai
import random
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
        """
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
    result = json.loads(output)
    return result['concept']

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
    result = json.loads(json_themes)
    return result['themes']

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
    output = _generate_text(prompt)
    return output.strip().lower()

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

def generate_poem_workflow(page_index, img_base64):
    """
    Handle the poem generation workflow, including generating a concept, theme, and attempting
    multiple poem generations with critique.
    """
    concept = _random_concept()
    st.write(f'Concept: {concept}')

    theme = random.choice(_common_themes(concept, url=img_base64))
    st.write(f'Theme: {theme["name"]}')
    st.write(f'Significance: {theme["significance"]}')

    generation, max_generations = 1, 10
    found_yes, poem = False, None

    while generation <= max_generations and not found_yes:
        poem = _generate_poem(concept, theme, url=img_base64)

        if st.session_state.is_first_global_generation:
            critique_result = "yes"
            st.write(f"Decision for generation {generation}: yes, no critique for the first generation!")
            st.session_state.is_first_global_generation = False
        else:
            critique_result = _critique_poem(poem, page_index, st.session_state.responses)

        if critique_result == "yes":
            found_yes = True
            st.session_state.responses[page_index] = poem
            st.write("Final poem:")
            st.write(poem)
        else:
            generation += 1

    if not found_yes and poem:
        st.write("Reached maximum generations without a satisfactory poem.")
        st.write("Last generated poem:")
        st.write(poem)