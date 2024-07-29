import io
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from src.assistant import Assistant
from util.custom_logger import CustomLogger

# set logger
logger = CustomLogger()

backend = Assistant()

st.set_page_config(
    page_title="Image Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject custom CSS
st.markdown(
    """
    <style>
    .custom-text {
        font-size: 15px;  /* Change the font size */
    }
    .description {
        font-size: 15px;  /* Change the font size */
    }
    .caveat {
        font-size: 15px;  /* Change the font size */
        color: #FF0000;
    }
    .sub_header {
        font-size: 20px;  /* Change the font size */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def display_data() -> None:
    st.header("Data Sample")
    with st.container(height=300, border=True):
        st.write(st.session_state['demo'])


def run():
    st.title("Image Assistant :robot_face:")
    
    txt = "Created using the cutting-edge technology of OpenAI and ImagineAPI, our app transforms your creative ideas into stunning images. Simply describe your vision, and watch as our app brings it to life with unparalleled detail and artistry. Perfect for artists, designers, and anyone looking to visualize their creativity, our app makes the impossible possible—one image at a time. Dive into a world where imagination knows no bounds!"
    st.markdown(
        f"""
        <p class="description"><i>{txt}</i></p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    uploaded_file = st.file_uploader("upload your :page_with_curl: here :point_down:")
    st.markdown('<p class="caveat"> <i>*currently supports excel only</i> </p>', unsafe_allow_html=True)

    # if there is new file uploaded
    if uploaded_file is not None:
        with st.spinner(':rocket: generating images...'):
            # Can be used wherever a "file-like" object is accepted:
            dataframe = pd.read_excel(uploaded_file, sheet_name='Voters')

            st.session_state['demo'] = dataframe.head(5)
            display_data()
            
            # generate prompts
            st.session_state['code'], st.session_state['proposal'], st.session_state['prompts'] = \
            backend.generate_prompts(uploaded_file)

            # generate images
            if "prompts" not in st.session_state:
                st.warning('no prompt generated, please check the format of your document', icon="⚠️")
            else:
                images = dict()
                for idx, p in enumerate(st.session_state['prompts']):
                    images[idx] = backend.generate_image(p)   

                st.session_state['images'] = images 

                # force switch to next page
                switch_page("prompt_generation")
    
    else:  # if no file being uploaded
        if 'demo' in st.session_state:
            display_data()

if __name__ == "__main__":
    run()