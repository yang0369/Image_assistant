import pandas as pd
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page
from util.custom_logger import CustomLogger

st.title('Prompt Generation')

# set logger
logger = CustomLogger()

def display_generations() -> None:
    with st.container(height=500):
        if st.session_state['code']:
            st.markdown(f'<p class="sub_header"> <b>Code Interpreter:</b> </p>', unsafe_allow_html=True)
            with st.container(height=200, border=True):
                st.code(st.session_state['code'], language='python', line_numbers=True)

        if st.session_state['proposal']:
            st.markdown(f'<p class="sub_header"> <b>Proposal:</b> </p>', unsafe_allow_html=True)
            with st.container(height=200, border=True):
                paragraphs = st.session_state['proposal'].split('\n\n')
                for p in paragraphs:
                    st.markdown(f'<p class="custom-text"> {p} </p>', unsafe_allow_html=True)

# save state
if 'prompts' in st.session_state:
    display_generations()
    time.sleep(20)
    switch_page("image_generation")
else:
    st.warning("Please upload your file first", icon="⚠️")
    time.sleep(3)
    switch_page("home")



