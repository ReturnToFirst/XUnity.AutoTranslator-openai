from dataclasses import dataclass, field
import re

@dataclass
class Tag:
    """
    Represents the start and end tags for source and target in a translation task.

    Attributes:
        src_start (str): Start tag for the source language.
        src_end (str): End tag for the source language.
        tgt_start (str): Start tag for the target language.
        tgt_end (str): End tag for the target language.
    """
    src_start: str
    src_end: str
    tgt_start: str
    tgt_end: str

    @classmethod
    def from_dict(cls, config_dict: dict):
        """
        Creates an instance of Tag from a dictionary.

        Args:
            config_dict (dict): A dictionary containing 'src_start', 'src_end', 'tgt_start', 'tgt_end'.

        Returns:
            Tag: An instance of the Tag class with attributes set from the dictionary.
        """
        return cls(src_start=config_dict['src_start'],
                   src_end=config_dict['src_end'],
                   tgt_start=config_dict['tgt_start'],
                   tgt_end=config_dict['tgt_end'])

@dataclass
class Template:
    """
    Represents a translation task template, including start and end tags for source and target, and optional language specification.

    Attributes:
        task_template (str): The template for the translation task.
        specify_language (bool): Indicates whether language specification is required.
        language_template (str): The template for specifying the source and target languages.
        tag (Tag): An instance of the Tag class containing start and end tags.
        src_prompt (str): The formatted source prompt using the source tags.
        tgt_regex (re.Pattern): A regular expression pattern to extract the target text using the target tags.
    """
    task_template: str
    specify_language: bool
    language_template: str
    tag: Tag
    src_prompt: str = field(init=False)
    tgt_regex: re.Pattern = field(init=False)

    def __post_init__(self):
        """
        Initializes the src_prompt and tgt_regex attributes based on the tag and task_template attributes.
        """
        self.src_prompt = f"{self.tag.src_start}{{src_text}}{self.tag.src_end}"
        self.tgt_regex = re.compile(f"{self.tag.tgt_start}\\s*(.*?)\\s*{self.tag.tgt_end}", re.DOTALL)
        self.task_template = self.task_template.format(src_start=self.tag.src_start,
                                                      src_end=self.tag.src_end,
                                                      tgt_start=self.tag.tgt_start,
                                                      tgt_end=self.tag.tgt_end)

    @classmethod
    def from_dict(cls, config_dict: dict):
        """
        Creates an instance of Template from a dictionary.

        Args:
            config_dict (dict): A dictionary containing 'task_template', 'specify_language', 'language_template' and 'tag'.

        Returns:
            Template: An instance of the Template class with attributes set from the dictionary.
        """
        return cls(task_template=config_dict['task_template'],
                   specify_language=config_dict['specify_language'],
                   language_template=config_dict['language_template'],
                   tag=Tag.from_dict(config_dict['tag']))
    
    def get_src_filled_prompt(self, src_text: str) -> str:
        """
        Returns the source prompt filled with the provided source text.

        Args:
            src_text (str): The source text to be included in the prompt.

        Returns:
            str: The formatted source prompt.
        """
        return self.src_prompt.format(src_text=src_text)

    def get_translated_text(self, tgt_text: str) -> str:
        """
        Extracts and returns the translated text from the provided target text using the tgt_regex.

        Args:
            tgt_text (str): The target text to be searched for the translated text.

        Returns:
            str: The extracted translated text.
        """
        print(tgt_text)
        match = self.tgt_regex.search(tgt_text)
        return match.group(1) if match else ""

    def get_language_target_prompt(self, src_lang: str, tgt_lang: str) -> str:
        """
        Returns the language target prompt filled with the provided source and target languages.

        Args:
            src_lang (str): The source language.
            tgt_lang (str): The target language.

        Returns:
            str: The formatted language target prompt.
        """
        return self.language_template.format(src_lang=src_lang, tgt_lang=tgt_lang)

@dataclass
class SystemPrompt:
    """
    Represents a system prompt configuration with an optional system prompt.

    Attributes:
        use_system_prompt (bool): Indicates whether a system prompt should be used.
        system_prompt (str): The system prompt to be used.
    """
    use_system_prompt: bool
    system_prompt: str

    @classmethod
    def from_dict(cls, config_dict: dict):
        """
        Creates an instance of SystemPrompt from a dictionary.

        Args:
            config_dict (dict): A dictionary containing 'use_system_prompt' and 'system_prompt'.

        Returns:
            SystemPrompt: An instance of the SystemPrompt class with attributes set from the dictionary.
        """
        return cls(use_system_prompt=config_dict['use_system_prompt'],
                   system_prompt=config_dict['system_prompt'])

@dataclass
class Prompt:
    """
    Represents a prompt configuration for a translation task, including a template and an optional system prompt.

    Attributes:
        template (Template): An instance of the Template class containing the translation task template.
        system_prompt (SystemPrompt): An instance of the SystemPrompt class containing the system prompt configuration.
    """
    template: Template
    system_prompt: SystemPrompt

    @classmethod
    def from_dict(cls, config_dict: dict):
        """
        Creates an instance of SystemPrompt from a dictionary.

        Args:
            config_dict (dict): A dictionary containing 'use_system_prompt' and 'system_prompt'.

        Returns:
            SystemPrompt: An instance of the SystemPrompt class with attributes set from the dictionary.
        """
        return cls(template=Template.from_dict(config_dict['template']),
                   system_prompt=SystemPrompt.from_dict(config_dict['system_prompt']))