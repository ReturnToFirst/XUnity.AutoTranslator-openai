from dataclasses import dataclass
import toml


@dataclass
class OpenAIConfig:
    """
    A dataclass to represent the configuration for OpenAI API requests.
    
    Attributes:
        base_url (str): The base URL for the OpenAI API.
        api_key (str): The API key for authentication with the OpenAI API.
        model_name (str): The name of the OpenAI model to be used for requests.
    """
    
    base_url: str
    api_key: str
    model_name: str
    
    @classmethod
    def from_dict(cls, config_dict: dict):
        """
        Create an OpenAIConfig instance from a dictionary.
        
        Args:
            config_dict (dict): A dictionary containing the configuration for the OpenAI API.
        """
        return cls(**config_dict)

@dataclass
class ModelConfig:
    """
    Configuration for the OpenAI model parameters.

    Attributes:
        temperature (float): Controls the randomness of predictions. Lower values make the model more deterministic.
        max_tokens (int): The maximum number of tokens to generate in the completion.
        frequency_penalty (float): Penalizes new tokens based on their frequency in the text so far.
        presence_penalty (float): Penalizes new tokens based on whether they appear in the text so far.
    """
    temperature: float
    max_tokens: int
    frequency_penalty: float
    presence_penalty: float

    @classmethod
    def from_dict(cls, config_dict: dict):
        """
        Create a ModelConfig instance from a dictionary.

        Args:
            config_dict (dict): A dictionary containing the configuration parameters.

        Returns:
            ModelConfig: An instance of ModelConfig initialized with the values from the dictionary.
        """
        return cls(**config_dict)
@dataclass
class ServerConfig:
    """
    Configuration for the server.
    
    Attributes:
        host: The server's host address.
        port: The port on which the server will listen.
    """
    host: str
    port: str

    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(**config_dict)
@dataclass
class DatabaseConfig:
    """Dataclass to store the configuration for the database, including the file path."""
    db_file: str
    cache_translation: bool
    use_cached_translation: bool
    
    @classmethod
    def from_dict(cls, config_dict: dict):
        """Create a DatabaseConfig instance from dictionary.

        Args:
            config_dict (dict): Dictionary containing the database configuration.

        Returns:
            DatabaseConfig: Instance of DatabaseConfig with provided configuration.
        """
        return cls(**config_dict)

@dataclass
class HistoryConfig:
    use_history: bool
    max_history: int
    use_latest_history: bool

    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(**config_dict)
@dataclass
class LoggingConfig:
    """
    Configuration settings for logging.
    
    Attributes:
        log_file (str): The path to the log file where logs will be written.
        log_level (str): The level of logging (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
    """
    log_file: str
    log_level: str

    @classmethod
    def from_dict(cls, config_dict: dict):
        return cls(**config_dict)


@dataclass
class Config:
    """
    Configuration class for the application, aggregating various configurations.
    
    Attributes:
        openai_config: Configuration related to the OpenAI API.
        model_config: Configuration for the model parameters.
        server_config: Configuration for the server settings.
        database_config: Configuration for the database.
        logging_config: Configuration for logging settings.
    """
    openai_config: OpenAIConfig
    model_config: ModelConfig
    server_config: ServerConfig
    history_config: HistoryConfig
    database_config: DatabaseConfig
    logging_config: LoggingConfig

    @classmethod
    def from_toml(cls, config_file: str = "config.toml"):
        """
        Load configuration from a TOML file and create a Config instance.

        Args:
            config_file: Path to the TOML configuration file.

        Returns:
            Config: An instance of Config with configuration loaded from the file.

        Raises:
            Exception: If there is an error loading the configuration file.
        """
        try:
            config_dict = toml.load(config_file)
        except Exception as e:
            print(f"Error loading config file: {e}")
            raise
        return cls(
            openai_config=OpenAIConfig.from_dict(config_dict['openai']),
            model_config=ModelConfig.from_dict(config_dict['model']),
            server_config=ServerConfig.from_dict(config_dict['server']),
            history_config=HistoryConfig.from_dict(config_dict['history']),
            database_config=DatabaseConfig.from_dict(config_dict['database']),
            logging_config=LoggingConfig.from_dict(config_dict['logging']),
        )
