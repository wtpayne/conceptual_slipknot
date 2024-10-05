import random
import streamlit as st
import ssl
from requests.exceptions import RequestException

from utils import display_image, replace_current_url
from utils import URLS
from calls import _random_concept, _common_themes, _generate_poem, _critique_poem

def apply_styles():
    """
    Apply custom CSS styles to center elements and control image overflow.
    """
    st.markdown(
        """
        <style>
        html, body, [class*="css"] {
            margin: 0;
            padding: 0;
            overflow-y: hidden !important;
        }
        .stApp {
            max-width: 400px;
            margin: 0 auto;
            text-align: center;
        }
        .stImage {
            display: block;
            margin-left: auto;
            margin-right: auto;
            max-height: 30vh;
            width: auto;
        }
        .stButton > button {
            display: inline-block;
        }
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True
    )

def initialize_state():
    """
    Initialize session state variables for responses and global first-generation flag.
    """
    if 'responses' not in st.session_state:
        st.session_state.responses = [None] * len(URLS)
    if 'is_first_global_generation' not in st.session_state:
        st.session_state.is_first_global_generation = True

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
        try:
            poem = _generate_poem(concept, theme, url=img_base64)

            if st.session_state.is_first_global_generation:
                critique_result = "yes"
                st.write(f"Decision for generation {generation}: yes, no critique for the first generation!")
                st.session_state.is_first_global_generation = False
            else:
                critique_result = _critique_poem(poem, page_index, st.session_state.responses)
                if critique_result is None:
                    st.error("Network error occurred during critique. Please try again.")
                    break

            if critique_result == "yes":
                found_yes = True
                st.session_state.responses[page_index] = poem
                st.write("Final poem:")
                st.write(poem)
            else:
                generation += 1

        except (ssl.SSLError, RequestException) as e:
            st.error(f"Network error occurred: {str(e)}. Please try again.")
            break

    if not found_yes and poem:
        st.write("Reached maximum generations without a satisfactory poem.")
        st.write("Last generated poem:")
        st.write(poem)

def display_responses():
    """
    Display responses for all pages.
    """
    with st.expander("Responses for all pages"):
        for i, response in enumerate(st.session_state.responses):
            st.write(f"Page {i + 1}: {response if response else 'No response generated yet.'}")

def navigation_controls(page_index):
    """
    Display navigation controls for navigating between pages.
    """
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button('Previous') and page_index > 0:
            st.session_state.page_index = page_index - 1
            st.rerun()
    with col2:
        st.write(f'Page {page_index + 1} of {len(URLS)}')
    with col3:
        if st.button('Next') and page_index < len(URLS) - 1:
            st.session_state.page_index = page_index + 1
            st.rerun()

def main():
    """
    Main function to run the Streamlit app.
    """
    apply_styles()
    initialize_state()

    page_index = st.session_state.get('page_index', 0)

    # Move the Replace URL button and functionality to the top
    replace_current_url()

    img_base64 = display_image(page_index)

    if st.button('Generate poem', key="generate_poem_button"):
        generate_poem_workflow(page_index, img_base64)

    display_responses()
    navigation_controls(page_index)

if __name__ == '__main__':
    main()