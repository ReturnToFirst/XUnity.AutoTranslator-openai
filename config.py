from dataclasses import dataclass
import toml


@dataclass
class OpenAIConfig:
    base_url: str
    api_key: str
    model_name: str
    
    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(**config_dict)
@dataclass
class ModelConfig:
    temperature: float
    max_tokens: int
    frequency_penalty: float
    presence_penalty: float

    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(**config_dict)
@dataclass
class ServerConfig:
    host: str
    port: str

    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(**config_dict)
@dataclass
class DatabaseConfig:
    db_file: str
    
    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(**config_dict)


@dataclass
class LoggingConfig:
    log_file: str
    log_level: str

    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(**config_dict)


@dataclass
class Config:
    openai_config: OpenAIConfig
    model_config: ModelConfig
    server_config: ServerConfig
    database_config: DatabaseConfig
    logging_config: LoggingConfig

    @classmethod
    def from_toml(cls, config_file: str = "config.toml"):
        try:
            config_dict = toml.load(config_file)
        except Exception as e:
            print(f"Error loading config file: {e}")
            raise
        print(config_dict)
        return cls(
            openai_config=OpenAIConfig.from_dict(config_dict['openai']),
            model_config=ModelConfig.from_dict(config_dict['model']),
            server_config=ServerConfig.from_dict(config_dict['server']),
            database_config=DatabaseConfig.from_dict(config_dict['database']),
            logging_config=LoggingConfig.from_dict(config_dict['logging']),
        )
