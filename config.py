from dataclasses import dataclass
import toml

@dataclass
class OpenAIConfig:
    base_url: str
    api_key: str
    model_name: str
    
    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(base_url=config_dict['base_url'],
                   api_key=config_dict['api_key'],
                   model_name=config_dict['model_name'])

@dataclass
class ModelConfig:
    temperature: float
    max_tokens: int
    frequency_penalty: float
    presence_penalty: float

    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(temperature=config_dict['temperature'],
                   max_tokens=config_dict['max_tokens'],
                   frequency_penalty=config_dict['frequency_penalty'],
                   presence_penalty=config_dict['presence_penalty'])

@dataclass
class ServerConfig:
    host: str
    port: str

    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(host=config_dict['host'],
                   port=config_dict['port'])


@dataclass
class DatabaseConfig:
    db_file: str
    
    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(db_file=config_dict['db_file'])


@dataclass
class LoggingConfig:
    log_file: str
    log_level: str

    @classmethod
    def from_dict(cls, config_dict:dict):
        return cls(log_file=config_dict['log_file'],
                   log_level=config_dict['log_level'])

@dataclass
class Config:
    openai_config: OpenAIConfig
    model_config: ModelConfig
    server_config: ServerConfig
    database_config: DatabaseConfig
    logging_config: LoggingConfig

    @classmethod
    def from_toml(cls, config_file:str=r"config.toml"):
        try:
            config_dict = toml.load(config_file)
        except Exception as e:
            print(f"Error loading config file: {e}")
            raise e
        
        return cls(OpenAIConfig.from_dict(config_dict['openai']),
                   ModelConfig.from_dict(config_dict['model']),
                   ServerConfig.from_dict(config_dict['server']),
                   DatabaseConfig.from_dict(config_dict['database']),
                   LoggingConfig.from_dict(config_dict['logging']))