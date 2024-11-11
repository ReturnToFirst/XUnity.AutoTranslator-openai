from dataclasses import dataclass
import toml

@dataclass
class OpenAIConfig:
    def __init__(self, url:str, api_key:str, model:str):
        self.url = url
        self.api_key = api_key
        self.model = model
    
    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(url=config_dict['url'],
                   api_key=config_dict['api_key'],
                   model=config_dict['model'])

@dataclass
class ModelConfig:
    def __init__(self, temperature:float, max_tokens:int, frequency_penalty:float, presence_penalty:float):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(temperature=config_dict['temperature'],
                   max_tokens=config_dict['max_tokens'],
                   frequency_penalty=config_dict['frequency_penalty'],
                   presence_penalty=config_dict['presence_penalty'])

@dataclass
class ServerConfig:
    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
    
    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(host=config_dict['host'],
                   port=config_dict['port'])


@dataclass
class DatabaseConfig:
    def __init__(self, db_file:str):
        self.db_file = db_file
    
    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(db_file=config_dict['db_file'])


@dataclass
class LoggingConfig:
    def __init__(self, log_file:str, log_level:str):
        self.log_file = log_file
        self.log_level = log_level

    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(log_file=config_dict['log_file'],
                   log_level=config_dict['log_level'])

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
        
        return cls(OpenAIConfig.from_dict(openai_config),
                   ModelConfig.from_dict(model_config),
                   ServerConfig.from_dict(server_config),
                   DatabaseConfig.from_dict(database_config),
                   LoggingConfig.from_dict(logging_config))