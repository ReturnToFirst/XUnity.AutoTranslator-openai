from openai import OpenAI
from config import Config
from prompt import Prompt
from chat_history import ChatHistory
from dataclasses import dataclass, field

@dataclass
class LLMClient:
    """
    A class representing a client for interacting with a language model via OpenAI API.

    Args:
        config (Config): Configuration settings for the client including OpenAI API and model configurations.
        prompt (Prompt): The prompt to be used for interactions with the language model.
        chat_history (ChatHistory): The history of the chat between the user and the language model. Defaults to an empty ChatHistory.
    """
    config: Config
    client: OpenAI = field(init=False)
    prompt: Prompt
    chat_history: ChatHistory = field(default_factory=ChatHistory)

    @classmethod
    def from_config(cls, config: Config, prompt: Prompt):
        """
        Factory method to create an LLMClient from a Config and Prompt instance.

        Args:
            config (Config): Configuration settings for the client including OpenAI API and model configurations.
            prompt (Prompt): The prompt to be used for interactions with the language model.

        Returns:
            LLMClient: An instance of LLMClient.
        """
        return cls(config=config, prompt=prompt)
    
    def __post_init__(self):
        """
        Initializes the OpenAI client and sets up the system and task prompts in the chat history.
        """
        self.client = OpenAI(base_url=self.config.openai_config.base_url,
                             api_key=self.config.openai_config.api_key)
        self.chat_history.set_system_prompt(self.prompt.system_prompt.system_prompt)
        self.chat_history.set_task_prompt(self.prompt.template.task_template)

    def request_completion(self):
        """
        Requests a completion from the language model based on the chat history.

        Returns:
            str: The content of the response message from the language model.
            Exception: An exception if an error occurs during the API call.
        """
        try:
            completion = self.client.chat.completions.create(
                        model=self.config.openai_config.model_name,
                        messages=self.chat_history.chat_history,
                        temperature=self.config.model_config.temperature,
                        frequency_penalty=self.config.model_config.frequency_penalty,
                        presence_penalty=self.config.model_config.presence_penalty
                        )
        except Exception as e:
            print(f"Error in OpenAI completion. Error: {e}")
            return e
        return completion.choices[0].message.content

    def reset_history(self):
        """
        Resets the chat history.
        """
        self.chat_history.reset_history()
        if self.prompt.system_prompt.use_system_prompt:
            self.chat_history.add_system_prompt(self.prompt.system_prompt)
        self.chat_history.add_user_content(self.prompt.template.task_template)
        self.chat_history.src_lang = ""
        self.chat_history.tgt_lang = ""

@dataclass
class Prompt:
    system_prompt: str
    task_prompt: str