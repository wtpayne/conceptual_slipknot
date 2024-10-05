import base64
import streamlit as st

def _load_image_as_base64(file_path):
    """
    Convert local image to base64 string.

    """
    with open(file_path, "rb") as image_file:
        return f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"

def display_image(page_index):
    """
    Load and display the image for the current page index.
    """
    img_base64 = _load_image_as_base64(URLS[page_index])
    st.image(img_base64, use_column_width=True, output_format='auto')
    return img_base64

def replace_current_url():
    """
    Replace the current URL with a new one provided by the user.
    """
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
    '/Users/ssk/Downloads/conceptual_slipknot/images/lion.jpeg',  # Replace with your second image URL
    '/Users/ssk/Downloads/conceptual_slipknot/images/zebra.jpeg'  # Replace with your third image URL
]
# /Users/ssk/Downloads/conceptual_slipknot/images/cheetah.jpeg

# Initialize session state for responses if it doesn't exist
if 'responses' not in st.session_state:
    st.session_state.responses = [None] * len(URLS)  # Initialize with None for each page