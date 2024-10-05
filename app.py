import streamlit as st

from utils import display_image, replace_current_url, navigation_controls, display_responses
from utils import apply_styles, initialize_state
from calls import generate_poem_workflow

def main():

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