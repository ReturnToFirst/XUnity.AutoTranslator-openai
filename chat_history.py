from dataclasses import dataclass, field

@dataclass
class ChatHistory:
    chat_history: list = field(default_factory=list)
    system_prompt: str = field(default='')
    task_prompt: str = field(default='')
    src_lang: str = field(default='')
    tgt_lang: str = field(default='')

    def reset_history(self, use_system_prompt: bool = True):
        self.chat_history = []
        if use_system_prompt:
            self.add_system_prompt(self.system_prompt)
        self.add_user_content(self.task_prompt)
    
    def add_message(self, role: str, content: str):
        if self.chat_history:
            latest_message = self.chat_history.pop()
            if latest_message["role"] == role:
                self.chat_history.append({"role": role, "content": f"{latest_message['content']}\n\n{content}"})
            else:
                self.chat_history.append(latest_message)
                self.chat_history.append({"role": role, "content": content})
        else:
            self.chat_history.append({"role": role, "content": content})

    def set_system_prompt(self, system_prompt: str):
        self.system_prompt = system_prompt

    def set_task_prompt(self, task_prompt: str):
        self.task_prompt = task_prompt

    def add_user_content(self, user_content: str):
        self.add_message("user", user_content)

    def add_system_prompt(self, system_prompt: str):
        self.add_message("system", system_prompt)

    def add_assistant_content(self, assistant_content: str):
        self.chat_history.append({"role": "assistant", "content": assistant_content})
