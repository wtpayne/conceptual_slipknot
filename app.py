import random
import streamlit as st

from utils import _load_image_as_base64
from utils import _generate_poem
from utils import _random_concept
from utils import _common_themes
from utils import URLS

def main():
    """
    Main function.
    """
    # Apply centering CSS and hide overflow
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
            max-height: 30vh; /* Limit the height of images to 30% of viewport height */
            width: auto;  /* Maintain aspect ratio */
        }
        .stButton > button {
            display: inline-block;
        }
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state for responses if not already present
    if 'responses' not in st.session_state:
        st.session_state.responses = [None] * len(URLS)

    page_index = st.session_state.get('page_index', 0)

    str_url = URLS[page_index]
    img_base64 = _load_image_as_base64(str_url)

    # Center the image using the class defined in the CSS
    st.image(img_base64, use_column_width=True, output_format='auto')

    if st.button('Generate poem'):
        concept = _random_concept()
        st.write(f'Concept: {concept}')

        theme = random.choice(_common_themes(concept, url=img_base64))
        st.write(f'Theme: {theme["name"]}')
        st.write(f'Significance: {theme["significance"]}')

        # Generate poem and replace the existing response for the current page
        poem = _generate_poem(concept, theme, url=img_base64)
        st.session_state.responses[page_index] = poem  # Store the poem in session state
        st.write(poem)

    # Display response for all pages
    with st.expander("Responses for all pages"):
        for i, response in enumerate(st.session_state.responses):
            if response is not None:
                st.write(f"Page {i + 1}: {response}")
            else:
                st.write(f"Page {i + 1}: No response generated yet.")

    # Navigation buttons
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

if __name__ == '__main__':
    main()