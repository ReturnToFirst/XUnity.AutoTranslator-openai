from dataclasses import dataclass

@dataclass
class Setting:
    def __init__(self):
        self.OpenAISetting = OpenAISetting()
        self.ModelSetting = ModelSetting()
        self.ServerSetting = ServerSetting()
        self.DatabaseSetting = DatabaseSetting()
        self.LoggingSetting = LoggingSetting()

@dataclass
class OpenAISetting:
    def __init__(self, url:str, api_key:str, model_name:str):
        self.url = url
        self.api_key = api_key
        self.model_name = model_name

@dataclass
class ModelSetting:
    def __init__(self, temperature:float, max_tokens:int, frequency_penalty:float, presence_penalty:float):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

@dataclass
class ServerSetting:
    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port


@dataclass
class DatabaseSetting:
    def __init__(self, db_filename:str):
        self.db_filename = db_filename


@dataclass
class LoggingSetting:
    def __init__(self, log_filename:str, log_level:str):
        self.log_filename = log_filename
        self.log_level = log_level
