import pandas as pd
import streamlit as st
from util.custom_logger import CustomLogger
import time

st.title('Image Generation')


# set logger
logger = CustomLogger()

# save state
if 'prompts' in st.session_state:
    with st.container(height=200):
        prompt = st.radio(
        ":stuck_out_tongue: Choose a prompt :point_down:",
        [f":thought_balloon: :rainbow[{p}]" for p in st.session_state.prompts])

    st.divider()

    if prompt:
        with st.spinner('generating images...'):
            idx = st.session_state.prompts.index(prompt[27:-1])
            with st.container(height=250):
                st.write(":eyes: Discover the stunning images brought to life by AI :point_down:")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.image(st.session_state['images'].get(idx)[0])
                    st.write(f":mag_right: [fullscreen]({st.session_state['images'].get(idx)[0]})")

                with col2:
                    st.image(st.session_state['images'].get(idx)[1])
                    st.write(f":mag_right: [fullscreen]({st.session_state['images'].get(idx)[1]})")
                    
                with col3:
                    st.image(st.session_state['images'].get(idx)[2])
                    st.write(f":mag_right: [fullscreen]({st.session_state['images'].get(idx)[2]})")

                with col4:
                    st.image(st.session_state['images'].get(idx)[3])
                    st.write(f":mag_right: [fullscreen]({st.session_state['images'].get(idx)[3]})")

else:
    st.write("please go to main page and upload your file first")