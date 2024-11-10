# OpenAI-Compatiable Translation provider for XUnity.AutoTranslator

A translation Custom provider for [XUnity.AutoTranslator](https://github.com/bbepis/XUnity.AutoTranslator).
This project is compatible with openai API.

## Installation
### Requirements

- [Python](https://www.python.org/downloads/) 3.8 or later

### Dependencies
- [aiohttp](https://pypi.org/project/aiohttp/)
- [openai](https://pypi.org/project/openai/)

You can install requirement with
```bash
pip3 install -r requirements.txt
```

## Usage
1. Install Depandencies
2. Configure the provider in XUnity.AutoTranslator
    1. Changer Provider to 'CustomTranslate' in [Service] section.
    ```toml
    [Service]
    Endpoint=CustomTranslate
    ```
    2. Set server url in [Custom] section.
    ```toml
    [Custom]
    Url=http://<server_url>:<server_port>/translate
    ```

3. Turn on server in console
    ```bash
    python3 main.py
    ```

## TODO
- [ ] Separate config file
    - [ ] Prompt
    - [ ] Server
    - [ ] Model
- [ ] Docs
    - [ ] Installation
    - [ ] Usage
    - [ ] Configuration
- [ ] refactor