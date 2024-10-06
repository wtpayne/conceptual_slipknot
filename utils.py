import base64
import streamlit as st

def display_responses():
    with st.expander("Responses for all pages"):
        for i, response in enumerate(st.session_state.responses):
            st.write(f"Page {i + 1}: {response if response else 'No response generated yet.'}")

def initialize_state():
    if 'responses' not in st.session_state:
        st.session_state.responses = [None] * len(URLS)
    if 'is_first_global_generation' not in st.session_state:
        st.session_state.is_first_global_generation = True

def _load_image_as_base64(file_path):
    with open(file_path, "rb") as image_file:
        return f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"

def display_image(page_index):
    img_base64 = _load_image_as_base64(URLS[page_index])
    st.image(img_base64, use_column_width=True, output_format='auto')
    return img_base64

def replace_current_url():
    if 'show_url_input' not in st.session_state:
        st.session_state.show_url_input = False

    if st.button("Replace URL", key="replace_url_button"):
        st.session_state.show_url_input = not st.session_state.show_url_input

    if st.session_state.show_url_input:
        new_url = st.text_input("Enter a new URL:", key="new_url_input")
        if st.button("Confirm", key="confirm_url_button"):
            if new_url:
                page_index = st.session_state.get('page_index', 0)
                URLS[page_index] = new_url
                st.success(f"URL for page {page_index + 1} has been updated.")
                st.session_state.show_url_input = False
                st.rerun()
            else:
                st.warning("Please enter a valid URL.")

URLS = [
    '/Users/ssk/Downloads/conceptual_slipknot/images/frog.jpeg',
    '/Users/ssk/Downloads/conceptual_slipknot/images/lion.jpeg',
    '/Users/ssk/Downloads/conceptual_slipknot/images/zebra.jpeg'
    # '/Users/ssk/Downloads/conceptual_slipknot/images/cheetah.jpeg'
]

if 'responses' not in st.session_state:
    st.session_state.responses = [None] * len(URLS)