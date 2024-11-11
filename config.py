from dataclasses import dataclass
import toml

@dataclass
class OpenAIConfig:
    def __init__(self, url:str, api_key:str, model:str):
        self.url = url
        self.api_key = api_key
        self.model = model

@dataclass
class ModelConfig:
    def __init__(self, temperature:float, max_tokens:int, frequency_penalty:float, presence_penalty:float):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

@dataclass
class ServerConfig:
    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port


@dataclass
class DatabaseConfig:
    def __init__(self, db_file:str):
        self.db_file = db_file


@dataclass
class LoggingConfig:
    def __init__(self, log_file:str, log_level:str):
        self.log_file = log_file
        self.log_level = log_level

@dataclass
class Config:
    def __init__(self, openai_config:OpenAIConfig, model_config:ModelConfig, server_config:ServerConfig, database_config:DatabaseConfig, logging_config:LoggingConfig):
        self.OpenAIConfig = openai_config
        self.ModelConfig = model_config
        self.ServerConfig = server_config
        self.DatabaseConfig = database_config
        self.LoggingConfig = logging_config

    @classmethod
    def from_toml(cls, config_file:str=r"config.toml"):
        try:
            config_dict = toml.load(config_file)
        except Exception as e:
            print(f"Error loading config file: {e}")
            raise e
        
        openai_config = config_dict['openai']
        model_config = config_dict['model']
        server_config = config_dict['server']
        database_config = config_dict['database']
        logging_config = config_dict['logging']
        
        return cls(OpenAIConfig(openai_config['url'], openai_config['api_key'], openai_config['model']),
                   ModelConfig(model_config['temperature'], model_config['max_tokens'], model_config['frequency_penalty'], model_config['presence_penalty']),
                   ServerConfig(server_config['host'], server_config['port']),
                   DatabaseConfig(database_config['db_file']),
                   LoggingConfig(logging_config['log_file'], logging_config['log_level']))