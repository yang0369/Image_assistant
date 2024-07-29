"""
This script is to experiment with OpenAI APIs
"""
import os
import re
import time
import yaml
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.beta.thread import Thread as ThreadType
from openai.types.beta.threads.run import Run as RunType
from pathlib import Path

from util.custom_logger import CustomLogger

"""
1. Project Setup
"""
# set paths
ROOT = Path(__file__).parents[1]
DATA = ROOT / "data"
SRC = ROOT / "src"

# set logger
logger = CustomLogger()

# load OpenAI credentials
load_dotenv()

if os.getenv("OPENAI_KEY", default="False"):
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    logger.info("successfully loaded OpenAI key")
else:
    raise ValueError("no OpenAI key found")

# get system prompt
with open(SRC / "util" / 'template.yml', 'r') as file:
   template = yaml.safe_load(file)

PROMPT = template["PROMPT"]

"""
2. set up OpenAI client
"""
logger.info("creating AI assistant")

# create client
client = OpenAI(
   default_headers={"OpenAI-Beta": "assistants=v2"},
   max_retries=1,
   api_key=OPENAI_KEY,
)

# prepare input file
file = client.files.create(
  file=open(DATA / "sample.xlsx", "rb"),
  purpose='assistants'
)

# create assistant
assistant = client.beta.assistants.create(
  name="Feedback Analysis Assistant ",
  instructions=PROMPT,
  model="gpt-4o",
  temperature=0.01,
  top_p=0.1,
  tools=[{"type": "code_interpreter"}],
  tool_resources={
    "code_interpreter": {
      "file_ids": [file.id]
    }
  }
)

"""
3. start a thread to prompt LLM
"""
logger.info("starting thread")
# create thread
thread = client.beta.threads.create()

# add message to thread
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="start",
)

# create a run 
run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
)


"""
4. get response
"""
logger.info("parsing the response")

def wait_on_run(
        run: RunType, 
        thread: ThreadType) -> RunType:
    """ wait for all polling to be completed """
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


run = wait_on_run(run, thread)

# parse code logs
run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread.id,
  run_id=run.id
)

code_snippet = []
for itm in run_steps.data[::-1]:
    sd = itm.step_details
    if sd.type == "tool_calls":
        tool_call_detail = sd.tool_calls        
        code_snippet.append(tool_call_detail[0].code_interpreter.input) # Algoritm
        if len(tool_call_detail[0].code_interpreter.outputs) > 0:
            code_snippet.append(tool_call_detail[0].code_interpreter.outputs[0].logs) # Output

code_snippet = "\n".join(code_snippet)
logger.info("code interpreter >>>")
logger.info(code_snippet)

# parse the messages
text = []
messages = client.beta.threads.messages.list(thread_id=thread.id)

for m in messages:
    text.append(m.content[0].text.value)

text = "\n".join(text)
logger.info("proposal >>>")
logger.info(text)

"""
5. parse response for image generation prompt
"""

# Regex pattern to extract text between "/imagine" and "—ar 16:9"
pattern = r"/imagine\s*(.*?)\s*—ar 16:9"

# Finding all matches
matches = re.findall(pattern, text)
logger.info("image prompts >>>")
logger.info(matches)




"""
references:
- create AI assistant: https://cookbook.openai.com/examples/assistants_api_overview_python
"""