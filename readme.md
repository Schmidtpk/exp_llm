# Readme

## Using llms

To use llms in coding we need to

- make API key available

- connect to openrouter API

- send prompts, receive llm answer

## Implementing experiments

- code single run
  - contains prompt
  - shares prompt
  - receives answer
  - saves all important data
  - look at result

- code treatment variations of single run
  - all of the above with variations
  - look at results (variation?)

- run treatment variations (potentially multiple times)
  - best wrap single run in function
  
- analyse data
  - compare treatment and control
  
- extend to more complex ideas


## Software stack

- Language: R or python

- Location: cloud or local
  - Local Rstudio
  - cloud Rstudio server
  - local Posit (R & Python)
  - local VSCode (Python & R)
  - cloud Colab (python & R)

- AI tools
  - chats (copy paste)
  - cloud native tools
    - gemini in colab (R performance disappointing)
    - codex of OpenAI (free tier?)
  - agentic tools local 
    - Cursor (free for students?)
    - Claude Code (best, but 20USD / month)
    - gemini cli (free tier, but helpful?)
    - VS Code with Copilot (free for students via github)
  - text complete
    - Rstudio (Github copilot, free for students via github)
    
- always:
  - provide context
    - your details on the project
    - your specific demands and preferences
    - slides, projectplan, etc.
    - scientific papers/books
    - previous ideas/plans
  - use context as resource to be saved and cherished
    - models come and go, some context stays relevant


## Repository

llmexp/
├── examples/             # examples
│   ├── setup.R           # Setup llm (R Code)
│   ├── setup.py          # Setup llm (python Code)
│   ├── expectations.R    # simple experiment with expectations
│   └── expectations.py   # simple experiment with expectations


