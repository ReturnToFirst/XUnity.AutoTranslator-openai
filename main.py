from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
import uvicorn
from prompt import Prompt
from config import Config
from openai_client import LLMClient
from db import DB


proxy_server = FastAPI()
config = Config.from_toml("config.toml")
prompt = Prompt.from_toml("prompt.toml")
client = LLMClient.from_config(config, prompt)
db = DB.from_file(config.database_config.db_file)

@proxy_server.get("/translate", response_class=PlainTextResponse)
async def translation_handler(
    text: str,
    tgt_lang: str = Query(..., alias="to"),
    src_lang: str = Query(..., alias="from")
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
        from (str): The source language code.

    Returns:
        str: The translated text.
    """
    if "" in [client.chat_history.src_lang, client.chat_history.tgt_lang] or client.chat_history.src_lang != src_lang or client.chat_history.tgt_lang != tgt_lang:
        client.reset_history()
        client.set_language_targets(src_lang, tgt_lang)
        if client.config.database_config.use_latest_records:
            translation_records = db.get_latest_translations(src_lang, tgt_lang, client.config.database_config.init_latest_records)
            if translation_records:
                client.apply_latest_translations(translation_records)
                print("Latest translation Applied.")
    client.chat_history.add_user_content(client.prompt.template.get_src_filled_prompt(text))
    if client.config.database_config.use_cached_translation:
        translated_text = db.fetch_translation(src_lang, tgt_lang, text)
        if translated_text:
            print("Got cached translation!")
            completion_res = f"{client.prompt.template.tag.tgt_start}{translated_text}{client.prompt.template.tag.tgt_end}"
        else:
            completion_res = client.request_completion()
    if client.config.history_config.use_history:
        client.chat_history.add_assistant_content(completion_res)
        if client.config.history_config.max_history > -1 :
            if len(client.chat_history.chat_history)-(1+(1 if client.prompt.system_prompt.use_system_prompt else 0)) >= client.config.history_config.max_history:
                if client.config.history_config.use_latest_history:
                    chat_history = client.chat_history.chat_history[2+(1 if client.prompt.system_prompt.use_system_prompt else 0):]
                    client.reset_history()
                    client.set_language_targets(src_lang, tgt_lang)
                    for turn in chat_history:
                        client.chat_history.add_message(turn['role'], turn['content'])
                else:
                    client.chat_history.delete_latest_turns(2)
    else:
        client.set_language_targets("","")
    translated_text = client.prompt.template.get_translated_text(completion_res)
    if client.config.database_config.cache_translation:
        if not db.fetch_translation(src_lang, tgt_lang, text):
            db.save_translation(src_lang, tgt_lang, text, translated_text)
    print(f"Original: {text}\nTranslated: {translated_text}")
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
    client.reset_history()
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