import random
import streamlit as st
import ssl
from requests.exceptions import RequestException

from utils import _load_image_as_base64
from utils import _generate_poem
from utils import _random_concept
from utils import _common_themes
from utils import _critique_poem
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

    # Initialize session state for responses and global first generation if not already present
    if 'responses' not in st.session_state:
        st.session_state.responses = [None] * len(URLS)
    if 'is_first_global_generation' not in st.session_state:
        st.session_state.is_first_global_generation = True

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

        generation = 1
        max_generations = 10
        poem = None
        critique_result = None
        found_yes = False

        while generation <= max_generations and not found_yes:
            try:
                poem = _generate_poem(concept, theme, url=img_base64)

                if st.session_state.is_first_global_generation:
                    critique_result = "yes"
                    st.write(f"Decision for generation {generation}: yes, no critic for the first generation!")
                    st.session_state.is_first_global_generation = False
                else:
                    critique_result = _critique_poem(poem, page_index, st.session_state.responses)
                    if critique_result is None:
                        st.error("Network error occurred during critique. Please try again.")
                        break
                
                st.write(f"Decision for generation {generation}: {critique_result}")

                if critique_result == "yes" or critique_result == '""yes""' or critique_result == "'yes'" or critique_result == 'yes.':
                    found_yes = True
                    st.session_state.responses[page_index] = poem
                    st.write("Final poem:")
                    st.write(poem)
                else:
                    generation += 1

            except (ssl.SSLError, RequestException) as e:
                st.error(f"Network error occurred: {str(e)}. Please try again.")
                break

        # This block will only execute if we've gone through all generations without a "yes"
        if not found_yes:
            if poem:
                st.write("Reached maximum generations without a satisfactory poem.")
                st.write("Last generated poem:")
                st.write(poem)
            else:
                st.error("Failed to generate a poem due to network errors. Please try again.")

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