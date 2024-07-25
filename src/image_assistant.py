import streamlit as st
from pathlib import Path
from util.custom_logger import CustomLogger
from io import StringIO
import pandas as pd
from src.assistant import Assistant

# set paths
ROOT = Path(__file__).parents[1]
DATA = ROOT / "data"
SRC = ROOT / "src"

st.title('Image Assistant')

backend = Assistant()

# set logger
logger = CustomLogger()

uploaded_file = st.file_uploader("upload excel here:")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_excel(uploaded_file, sheet_name='Voters')
    st.write(dataframe.head())

    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    backend.generate_prompts(uploaded_file)


