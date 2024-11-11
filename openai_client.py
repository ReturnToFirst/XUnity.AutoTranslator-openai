from openai import OpenAI
from config import Config
from prompt import Prompt
from chat_history import ChatHistory
from dataclasses import dataclass, field

@dataclass
class LLMClient:
    config: Config
    client: OpenAI = field(init=False)
    prompt: Prompt
    chat_history: ChatHistory = field(default_factory=ChatHistory)
    prompt: Prompt
    @classmethod
    def from_config(cls, config: Config, prompt: Prompt):
       return cls(config=config, prompt=prompt)
    
    def __post_init__(self):
        self.client = OpenAI(base_url=self.config.openai_config.base_url,
                             api_key=self.config.openai_config.api_key)
        self.chat_history.set_system_prompt(self.prompt.system_prompt.system_prompt)
        self.chat_history.set_task_prompt(self.prompt.template.task_template)

    @dataclass
    class Prompt:
        system_prompt: str = field(init=False)
        task_prompt: str = field(init=False)

    def request_completion(self):
        try:
            completion = self.client.chat.completions.create(
                        model=self.config.openai_config.model_name,
                        messages=self.chat_history.chat_history,
                        temperature=self.config.model_config.temperature,
                        frequency_penalty=self.config.model_config.frequency_penalty,
                        presence_penalty=self.config.model_config.presence_penalty
                        )

        except Exception as e:
            print(f"Error in OpenAI completion. Error : {e}")
            return e
        return completion.choices[0].message.content

    def reset_history(self):
        self.chat_history.reset_history()