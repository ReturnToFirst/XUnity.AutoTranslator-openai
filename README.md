# OpenAI-Compatiable Translation provider for XUnity.AutoTranslator

A translation Custom provider for [XUnity.AutoTranslator](https://github.com/bbepis/XUnity.AutoTranslator).
This project is compatible with openai API.

## Installation
### Requirements

- [Python](https://www.python.org/downloads/) 3.8 or later

### Dependencies
- [fastapi](https://pypi.org/project/fastapi/)
- [uvicorn](https://pypi.org/project/uvicorn/)
- [openai](https://pypi.org/project/openai/)

You can install requirement with
```
pip3 install -r requirements.txt
```

## Usage
1. Install Depandencies
2. Configure the provider in XUnity.AutoTranslator
    1. Changer Provider to 'CustomTranslate' in [Service] section.
    ```
    [Service]
    Endpoint=CustomTranslate
    ```
    2. Set server url in [Custom] section.
    ```
    [Custom]
    Url=http://<server_url>:<server_port>/translate
    ```

3. Turn on server in console
    ```
    python3 main.py
    ```

## TODO
- [x] Separate config file
    - [x] Prompt
    - [x] Server
    - [x] Model
- [ ] Docs
    - [ ] Installation
    - [ ] Requirements
    - [ ] Usage
    - [ ] Configuration
- [ ] refactor
    - [x] History
    - [x] Template
    - [x] Completion request
    - [x] Config
    - [x] Main
    - [ ] Server
    - [ ] Logger
    - [ ] Error handling
- [ ] Config
    - [x] Custom url
    - [x] Disable system template
    - [x] Disable specifying language
    - [ ] Disable history

- [ ] Database
    - [ ] Translation history
- [ ] API
    - [ ] Translation
    - [ ] Reset
- [ ] UI
    - [ ] WebUI
        - [ ] Control configs
        - [ ] Reset
        - [ ] Custom prompts
            - [ ] System prompt
            - [ ] Task template
        - [ ] Translation history