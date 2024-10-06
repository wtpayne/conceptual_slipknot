import streamlit as st

from utils import URLS

def apply_styles():
    st.markdown(
        """
        <style>
        html, body, [class*="css"] {
            margin: 0;
            padding: 0;
            overflow-y: hidden !important;
        }
        .stApp {
            max-width: 350px;
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
            margin: 0 15px;  /* Add some margin between buttons */
        }
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        /* Style for the dropdown */
        .stSelectbox {
            max-width: 200px;
            margin: 0 auto 10px;
        }
        /* Container for buttons */
        .button-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 10px;
        }
        /* Style for the heading */
        .heading {
            font-size: 24px;
            font-weight: bold;
            color: #4A4A4A;
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True
    )

def navigation_controls(page_index):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button('Back') and page_index > 0:
            st.session_state.page_index = page_index - 1
            st.rerun()
    with col2:
        st.write(f'Page {page_index + 1} of {len(URLS)}')
    with col3:
        if st.button('Next') and page_index < len(URLS) - 1:
            st.session_state.page_index = page_index + 1
            st.rerun()