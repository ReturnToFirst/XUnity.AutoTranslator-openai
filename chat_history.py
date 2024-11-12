from dataclasses import dataclass, field

@dataclass
class ChatHistory:
    """
    A dataclass to store the chat history along with system and task prompts, and source and target languages.
    
    Attributes:
    - chat_history (list): A list of dictionaries where each dictionary represents a message in the chat history.
    - src_lang (str): A string representing the source language.
    - tgt_lang (str): A string representing the target language.
    """

    chat_history: list = field(default_factory=list)
    src_lang: str = field(default='')
    tgt_lang: str = field(default='')

    def reset_history(self):
        self.chat_history = []
    
    def add_message(self, role: str, content: str):
        if self.chat_history:
            latest_message = self.chat_history.pop()
            if latest_message["role"] == role:
                self.chat_history.append({"role": role, "content": f"{latest_message['content']}\n{content}"})
            else:
                self.chat_history.append(latest_message)
                self.chat_history.append({"role": role, "content": content})
        else:
            self.chat_history.append({"role": role, "content": content})
    
    def delete_latest_turn(self):
        self.chat_history.pop()
        
    def set_system_prompt(self, system_prompt: str):
        self.system_prompt = system_prompt

    def set_task_prompt(self, task_prompt: str):
        self.task_prompt = task_prompt
    
    def set_src_lang(self, src_lang: str):
        self.src_lang = src_lang

    def set_tgt_lang(self, tgt_lang: str):
        self.tgt_lang = tgt_lang

    def add_user_content(self, user_content: str):
        self.add_message("user", user_content)

    def add_system_prompt(self, system_prompt: str):
        self.add_message("system", system_prompt)

    def add_assistant_content(self, assistant_content: str):
        self.chat_history.append({"role": "assistant", "content": assistant_content})
