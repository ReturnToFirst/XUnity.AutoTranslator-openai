from dataclasses import dataclass
import toml

class Template:
    def __init__(self, init_template:str, specify_language:bool, language_template:str):
        self.src_prompt = ""
        self.tgt_regex = ""

        self.init_template = init_template
        self.specify_language = specify_language
        self.language_template = language_template

    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(
            init_template=config_dict['init_template'],
            specify_language=config_dict['specify_language'],
            language_template=config_dict['language_template']
        )

class SystemPrompt:
    def __init__(self, use_system_prompt:bool, system_prompt:str):
        self.use_system_prompt = use_system_prompt
        self.system_prompt = system_prompt

    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(
            use_system_prompt=config_dict['use_system_prompt'],
            system_prompt=config_dict['system_prompt']
        )

class Tag:
    def __init__(self, src_start:str, src_end:str, tgt_start:str, tgt_end:str):
        self.src_start = src_start
        self.src_end = src_end
        self.tgt_start = tgt_start
        self.tgt_end = tgt_end
    
    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(
            src_start=config_dict['src_start'],
            src_end=config_dict['src_end'],
            tgt_start=config_dict['tgt_start'],
            tgt_end=config_dict['tgt_end'],
        )

@dataclass
class Prompt:
    def __init__(self, system_prompt:SystemPrompt, template:Template, tag:Tag):
        self.template = template
        self.system_prompt = system_prompt
        self.tag = tag
        self.template.src_prompt = f"{self.tag.src_start} {{tgt_text}} {self.tag.src_end}"
        self.template.tgt_regex = f"{self.tag.tgt_start}\\s*(.*?)\\s*{self.tag.tgt_end}"
        
    @classmethod
    def from_toml(cls, prompt_file:str=r"prompt.toml"):
        try:
            config_dict = toml.load(prompt_file)
        except Exception as e:
            print(f"Error loading config file: {e}")
            raise e
        
        system_prompt = config_dict['system_prompt']
        template = config_dict['template']
        tag = config_dict['tag']

        return cls(SystemPrompt.from_dict(system_prompt),
                   Template.from_dict(template),
                   Tag.from_dict(tag))