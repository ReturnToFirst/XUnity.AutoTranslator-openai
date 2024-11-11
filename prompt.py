from dataclasses import dataclass, field
import toml
import re

@dataclass
class Tag:
    src_start: str
    src_end: str
    tgt_start: str
    tgt_end: str

    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(src_start=config_dict['src_start'],
                   src_end=config_dict['src_end'],
                   tgt_start=config_dict['tgt_start'],
                   tgt_end=config_dict['tgt_end'])

@dataclass
class Template:
    task_template: str
    specify_language: bool
    language_template: str
    tag: Tag
    src_prompt: str = field(init=False)
    tgt_regex: re.Pattern = field(init=False)

    def __post_init__(self):
        self.src_prompt = f"{self.tag.src_start}{{src_text}}{self.tag.src_end}"
        self.tgt_regex = re.compile(f"{self.tag.tgt_start}\\s*(.*?)\\s*{self.tag.tgt_end}", re.DOTALL)
        self.task_template = self.task_template.format(src_start=self.tag.src_start,
                                                      src_end=self.tag.src_end,
                                                      tgt_start=self.tag.tgt_start,
                                                      tgt_end=self.tag.tgt_end)

    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(task_template=config_dict['task_template'],
                   specify_language=config_dict['specify_language'],
                   language_template=config_dict['language_template'],
                   tag=Tag.from_dict(config_dict['tag']))
    
    def get_src_filled_prompt(self, src_text:str):
        return self.src_prompt.format(src_text=src_text)

    def get_translated_text(self, tgt_text:str):
        match = self.tgt_regex.search(tgt_text)
        if match:
            translated_text = match.group(1)
        else:
            translated_text = ""
        return translated_text

@dataclass
class SystemPrompt:
    use_system_prompt: bool
    system_prompt: str

    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(use_system_prompt=config_dict['use_system_prompt'],
                   system_prompt=config_dict['system_prompt'])

@dataclass
class Prompt:
    template: Template
    system_prompt: SystemPrompt

    @classmethod
    def from_toml(cls, prompt_file: str = r"prompt.toml"):
        try:
            config_dict = toml.load(prompt_file)
        except Exception as e:
            print(f"Error loading config file: {e}")
            raise e

        return cls(template=Template.from_dict(config_dict['template']),
                   system_prompt=SystemPrompt.from_dict(config_dict['system_prompt']))