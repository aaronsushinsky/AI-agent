Gemini-based AI agent that can read and print file size and contents.
It can also review/edit/run python code, but only in the permitted directory. 
Agent is rate limited to 20 answers to prevent excess looping.
Agent saves its own previous responses to build on top of that logic/use history to determine next steps.
A basic calculator app in included as the code the agent is tested on.

Agent is just a project/prototype and IS NOT safe for public use.
With an API key connected, all that is needed from the user is to run `uv run main.py "<commands or requests>"`
