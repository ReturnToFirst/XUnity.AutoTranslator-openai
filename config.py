from dataclasses import dataclass
import toml
import argparse


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
    use_latest_records: bool
    init_latest_records: int

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

    @classmethod
    def from_args(cls, args):
        """
        Create a Config instance from command-line arguments.

        Args:
            args: Parsed command-line arguments.

        Returns:
            Config: An instance of Config with values from the provided arguments.
        """
        return cls(
            openai_config=OpenAIConfig.from_dict({
                "base_url": args.base_url,
                "api_key": args.api_key,
                "model_name": args.model_name
            }),
            model_config=ModelConfig.from_dict({
                "temperature": args.temperature,
                "max_tokens": args.max_tokens,
                "frequency_penalty": args.frequency_penalty,
                "presence_penalty": args.presence_penalty
            }),
            server_config=ServerConfig.from_dict({
                "host": args.host,
                "port": args.port
            }),
            history_config=HistoryConfig.from_dict({
                "use_history": args.use_history,
                "max_history": args.max_history,
                "use_latest_history": args.use_latest_history
            }),
            database_config=DatabaseConfig.from_dict({
                "db_file": args.db_file,
                "cache_translation": args.cache_translation,
                "use_cached_translation": args.use_cached_translation,
                "use_latest_records": args.use_latest_records,
                "init_latest_records": args.init_latest_records
            }),
            logging_config=LoggingConfig.from_dict({
                "log_file": args.log_file,
                "log_level": args.log_level
            })
        )
    
def parse_args():
    parser = argparse.ArgumentParser(description="Application Configuration CLI")
    
    # OpenAI Config
    parser.add_argument("--base_url", type=str, default="https://api.openai.com/v1", help="Base URL for OpenAI API")
    parser.add_argument("--api_key", type=str, required=True, help="openai")
    parser.add_argument("--model_name", type=str, default="gpt-3.5-turbo", help="OpenAI model name")
    
    # Model Config
    parser.add_argument("--temperature", type=float, default=0.0, help="Model temperature (randomness control)")
    parser.add_argument("--max_tokens", type=int, default=2048, help="Maximum number of tokens to generate")
    parser.add_argument("--frequency_penalty", type=float, default=0.0, help="Penalty for repeated tokens")
    parser.add_argument("--presence_penalty", type=float, default=0.0, help="Penalty for new tokens")
    
    # Server Config
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Server host address")
    parser.add_argument("--port", type=int, default=5000, help="Server port")
    
    # History Config
    parser.add_argument("--use_history", action="store_true", help="Enable history usage")
    parser.add_argument("--max_history", type=int, default=30, help="Maximum number of history records")
    parser.add_argument("--use_latest_history", action="store_true", help="Use latest history records")
    
    # Database Config
    parser.add_argument("--db_file", type=str, default="translated_texts.db", help="Path to the database file")
    parser.add_argument("--cache_translation", action="store_true",  help="Enable translation caching")
    parser.add_argument("--use_cached_translation", action="store_true", help="Use cached translations if available")
    parser.add_argument("--use_latest_records", action="store_true", help="Use latest database records")
    parser.add_argument("--init_latest_records", type=int, default=30, help="Number of initial latest records")
    
    # Logging Config
    parser.add_argument("--log_file", type=str, default="", help="Log file path")
    parser.add_argument("--log_level", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO", help="Logging level")
    
    return parser.parse_args()