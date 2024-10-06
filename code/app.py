import streamlit as st

from utils import display_image, replace_current_url, initialize_state, display_responses
from front import apply_styles, navigation_controls
from calls import generate_poem_workflow

def main():
    apply_styles()
    initialize_state()

    page_index = st.session_state.get('page_index', 0)

    # Initialize heading_shown in session state if not present
    if 'heading_shown' not in st.session_state:
        st.session_state.heading_shown = False

    # Display heading only on the first page and if it hasn't been shown yet
    if page_index == 0 and not st.session_state.heading_shown:
        st.markdown("<strong>Co-author:</strong> A multi-modal copilot for authors", unsafe_allow_html=True)
        st.session_state.heading_shown = True

    # Move the Replace URL button and functionality to the top
    replace_current_url()

    img_base64 = display_image(page_index)

    if st.button('Generate poem', key="generate_poem_button"):
        generate_poem_workflow(page_index, img_base64)

    display_responses()
    navigation_controls(page_index)

    # Add a refresh button to reset the heading
    if st.button('Refresh'):
        st.session_state.heading_shown = False
        st.session_state.page_index = 0
        st.rerun()

if __name__ == '__main__':
    main()