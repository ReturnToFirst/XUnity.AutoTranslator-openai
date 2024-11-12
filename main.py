from fastapi import FastAPI, Query
import uvicorn
from prompt import Prompt
from config import Config
from openai_client import LLMClient


proxy_server = FastAPI()
config = Config.from_toml("config.toml")
prompt = Prompt.from_toml("prompt.toml")
client = LLMClient.from_config(config, prompt)

@proxy_server.get("/translate")
async def translation_handler(
    to: str,
    text: str,
    from_lang: str = Query(..., alias="from")
):
    """
    Handle translation requests between specified languages.

    This function translates a piece of text from a source language to a target language.
    It checks if the current chat history's source and target languages differ from the provided
    ones and updates them if necessary. Then, it sends a completion request to the language model
    client and returns the translated text.

    Args:
        to (str): The target language code.
        text (str): The text to be translated.
        from_lang (str): The source language code.

    Returns:
        str: The translated text.
    """
    if "" in [client.chat_history.src_lang, client.chat_history.tgt_lang] or client.chat_history.src_lang != from_lang or client.chat_history.tgt_lang != to:
        client.chat_history.src_lang = from_lang
        client.chat_history.tgt_lang = to
        client.chat_history.reset_history(prompt.system_prompt.use_system_prompt)
        if client.prompt.template.specify_language:
            client.chat_history.add_user_content(client.prompt.template.get_language_target_prompt(from_lang, to))
    client.chat_history.add_user_content(client.prompt.template.get_src_filled_prompt(text))
    completion_res = client.request_completion()
    client.chat_history.add_assistant_content(completion_res)
    translated_text = client.prompt.template.get_translated_text(completion_res)
    return translated_text


@proxy_server.get("/reset")
async def reset_handler():
    """
    Reset the chat history.

    This function resets the chat history to its initial state, optionally using the system prompt
    based on the configuration.

    Returns:
        str: A success message indicating that the reset was successful.
    """
    client.chat_history.reset_history(prompt.system_prompt.use_system_prompt)
    return "Reset successful"


@proxy_server.get("/status")
async def status_handler():
    """
    Get the status of the server.

    This function returns a message indicating that the server is running.

    Returns:
        str: A message indicating the server's status.
    """
    return "Server is running"


if __name__ == "__main__":
    uvicorn.run(proxy_server)