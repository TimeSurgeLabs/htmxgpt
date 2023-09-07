# htmxgpt

ChatGPT clone in htmx, Python, and SQLite

# Stack
* HTMX + Tailwind
  + LangUI
* Python
* ChatGPT API
* SQLite
# Goal
* Create a ChatGPT like chat interface using HTMX and Tailwind
* Use Python to interact with the ChatGPT API
* Use SQLite to store the chat history
* Be able to view and select from multiple chat histories
* ~~Minimize the amount of JavaScript used~~ NO JAVASCRIPT. Use [Hyperscript](https://hyperscript.org/).

# To Do
* [Disable button and input](https://hyperscript.org/cookbook/#40-disable-btn-during-request) when waiting for response from API
* prevent HTML from being rendered if returned by the LLM
* Add loading display when waiting for response from API
* Add ability to use multiple LLMs
* Dockerize the application

# Possible Future Goals
* User accounts & authentication
* Move to a more robust database
* Chat history search via vectors
