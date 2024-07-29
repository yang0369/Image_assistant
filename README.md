# Imagine_assistant

## About this App
This app utilizes OpenAI GPT-4 and Midjourney APIs, combining LLM and image generation to bring your ideas to life. Just launch this Streamlit app and see your concepts transformed into stunning images.

## How to run
- set up environment
```
# set up environment, e.g. on linux
curl -sSL https://install.python-poetry.org | python3 -

poetry init

poetry install
```
 - run App on local server
```
cd Image_assistant
python -m streamlit run src/🏠home.py
```

## Project Structure

```
📦src
 ┣ 📂pages
 ┃ ┣ 📜1_🗒️prompt_generation.py
 ┃ ┗ 📜2_🖼️image_generation.py
 ┣ 📂util
 ┃ ┣ 📜custom_logger.py
 ┃ ┗ 📜template.yml
 ┣ 📜assistant.py
 ┗ 📜🏠home.py
```
where
 - home.py and pages/ form the streamlit frontend
 - assistant.py is the backend, including how the APIs being called.