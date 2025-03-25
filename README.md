# OpenAI-Compatiable Translation provider for XUnity.AutoTranslator

A translation Custom provider for [XUnity.AutoTranslator](https://github.com/bbepis/XUnity.AutoTranslator).<br>
This project is compatible with openai API.

## Installation
### Requirements

- [Python](https://www.python.org/downloads/) 3.8 or later

### Dependencies
- [fastapi](https://pypi.org/project/fastapi/)
- [uvicorn](https://pypi.org/project/uvicorn/)
- [openai](https://pypi.org/project/openai/)

You can install the requirements with:
```bash
pip3 install -r requirements.txt
```

## Usage
### Local Usage
1. Install Dependencies
2. Configure the provider in XUnity.AutoTranslator:
    1. Change Provider to 'CustomTranslate' in [Service] section.
        ```
            [Service]
            Endpoint=CustomTranslate
        ```
    2. Set server URL in [Custom] section.
        ```
        [Custom]
        Url=http://<server_url>:<server_port>/translate
        ```
        Turn on server in console:
        ```bash
        python3 main.py
        ```

### Docker Usage
#### docker run
If you want to run it with `docker run`, use command below.

```bash
docker run -d \
  --name xunity \
  -e BASE_URL="https://api.openai.com/v1" \
  -e API_KEY="api_key_here" \
  -e MODEL_NAME="gpt-3.5-turbo" \
  -e SQLITE_DB_PATH="translation.db" \
  -v ./translation.db:/app/translation.db \
  -p 5000:5000 \
  ghcr.io/returntofirst/xunity-autotranslator-openai:latest
```
This command will server on port `5000`.

#### docker compose
If you want to run this container with `docker compose`, use [docker-compose.yaml](docker-compose.yaml) to configure container

#### Kubernetes
If you want to run this container with kubernetes, use [k8s-example.yaml](k8s-example.yaml) to configure container
## Features
### Translation Provider
- CustomTranslate Endpoint: Integrate with XUnity.AutoTranslator using a custom endpoint that leverages OpenAI's translation capabilities.

### Advanced Translation Features
- Translation Caching: Store translated text in a local database to avoid redundant API calls and improve performance.
- Context-Aware Translation: Use previous and latest chat history to provide more contextually accurate translations.
- Configurable Prompts: Customize the system and task prompts used in translation requests via configuration files.
- Supported Languages: Support for multiple source and target languages that LLMs can handle.

### API Endpoints
- Translation: Perform translation using OpenAI's API.
    - Endpoint: /translate
    - Method: GET
    - Parameters: to={tgt_lang}&from={src_lang}&text={src_text}
    - Description: Sends a text translation request to the OpenAI API.

- Reset: Reset the chat history to start fresh.
    - Endpoint: /reset
    - Method: GET
    - Description: Clears the current chat history.

## TODO
- [ ] Docs
    - [ ] Installation
    - [ ] Requirements
    - [ ] Usage
    - [ ] Configuration
- [ ] Refactor
    - [ ] Server
    - [ ] Logger
    - [ ] Error handling
- [ ] UI
    - [ ] WebUI
        - [ ] Control configs
        - [ ] Reset
        - [ ] Custom prompts
        - [ ] System prompt
        - [ ] Task template
        - [ ] Translation history
            - [ ] Pre-translated dictonary
            - [ ] Remove bad translation
- [x] Deployment
    - [x] Github Actions
    - [x] Docker-compose
    - [x] Kubernetes