from dataclasses import dataclass
import toml

class Template:
    def __init__(self, init_template:str, specify_language:bool, language_template:str):
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

class Pattern:
    def __init__(self, src_tag_start:str, src_tag_end:str, tgt_tag_start:str, tgt_tag_end:str, regex_pattern:str):
        self.regex_pattern= regex_pattern
        self.src_tag_start = src_tag_start
        self.src_tag_end = src_tag_end
        self.tgt_tag_start = tgt_tag_start
        self.tgt_tag_end = tgt_tag_end
    
    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(
            src_tag_start=config_dict['src_tag_start'],
            src_tag_end=config_dict['src_tag_end'],
            tgt_tag_start=config_dict['tgt_tag_start'],
            tgt_tag_end=config_dict['tgt_tag_end'],
            regex_pattern=config_dict['regex_pattern']
        )

@dataclass
class Prompt:
    def __init__(self, system_prompt:SystemPrompt, template:Template, pattern:Pattern):
        self.template = template
        self.system_prompt = system_prompt
        self.pattern = pattern
        
    @classmethod
    def from_toml(cls, prompt_file:str=r"prompt.toml"):
        try:
            config_dict = toml.load(prompt_file)
        except Exception as e:
            print(f"Error loading config file: {e}")
            raise e
        
        system_prompt = config_dict['system_prompt']
        template = config_dict['template']
        pattern = config_dict['pattern']

        return cls(SystemPrompt.from_dict(system_prompt),
                   Template.from_dict(template),
                   Pattern.from_dict(pattern))
