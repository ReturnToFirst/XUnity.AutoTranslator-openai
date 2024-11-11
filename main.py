from fastapi import FastAPI, Query
import uvicorn
from prompt import Prompt
from config import Config
from openai_client import LLMClient


proxy_server = FastAPI()
config = Config.from_toml("config.toml")
prompt = Prompt.from_toml("prompt.toml")

@proxy_server.get("/translate")
async def translation_handler(to:str, text:str, from_lang: str = Query(..., alias="from")):
    if "" in [client.chat_history.src_lang, client.chat_history.tgt_lang] or client.chat_history.src_lang != from_lang or client.chat_history.tgt_lang != to:
        client.chat_history.src_lang = from_lang
        client.chat_history.tgt_lang = to
        client.chat_history.reset_history(prompt.system_prompt.use_system_prompt)
        client.chat_history.add_user_content(client.prompt.template.get_language_target_prompt(from_lang, to))
    client.chat_history.add_user_content(client.prompt.template.get_src_filled_prompt(text))
    completion_res = client.request_completion()
    translated_text = client.prompt.template.get_translated_text(completion_res)
    return translated_text

@proxy_server.get("/reset")
async def reset_handler():
    return "Reset successful"

@proxy_server.get("/status")
async def status_handler():
    return "Server is running"

if __name__ == "__main__":
    client = LLMClient.from_config(config, prompt)
    uvicorn.run(proxy_server)