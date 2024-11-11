from dataclasses import dataclass
import toml

@dataclass
class Config:
    """
    Represents the configuration settings for the application.
    
    Attributes:
        OpenAIConfig (OpenAIConfig): Configuration for the OpenAI API.
        ModelConfig (ModelConfig): Configuration for the language model.
        ServerConfig (ServerConfig): Configuration for the server.
        DatabaseConfig (DatabaseConfig): Configuration for the database.
        LoggingConfig (LoggingConfig): Configuration for logging.
        
    Methods:
        load_config(str): Loads the configuration settings from a TOML file.
    """
    
    OpenAIConfig = None
    ModelConfig = None
    ServerConfig = None
    DatabaseConfig = None
    LoggingConfig = None
    def __init__(self, config_file:str):
        """
        Loads the configuration settings from a TOML file.

        Args:
            config_file (str): The path to the TOML configuration file.

        Raises:
            Exception: If there is an error loading the config file.
        """

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

        self.OpenAIConfig = OpenAIConfig(openai_config['url'], openai_config['api_key'], openai_config['model'])
        self.ModelConfig = ModelConfig(model_config['temperature'], model_config['max_tokens'], model_config['frequency_penalty'], model_config['presence_penalty'])
        self.ServerConfig = ServerConfig(server_config['host'], server_config['port'])
        self.DatabaseConfig = DatabaseConfig(database_config['db_file'])
        self.LoggingConfig = LoggingConfig(logging_config['log_file'], logging_config['log_level'])

@dataclass
class OpenAIConfig:
    """
    Represents the configuration for the OpenAI API.

    Attributes:
        url (str): The URL for the OpenAI API.
        api_key (str): The API key for accessing the OpenAI API.
        model_name (str): The name of the language model to be used with the OpenAI API.
    """

    def __init__(self, url:str, api_key:str, model:str):
        self.url = url
        self.api_key = api_key
        self.model = model

@dataclass
class ModelConfig:
    """
    Represents the configuration for the language model.

    Attributes:
        temperature (float): The temperature value for controlling randomness in the generated text.
        max_tokens (int): The maximum number of tokens to generate in the response.
        frequency_penalty (float): Penalty for repeated tokens based on their frequency.
        presence_penalty (float): Penalty for repeated tokens based on their presence in the model.
    """

    def __init__(self, temperature:float, max_tokens:int, frequency_penalty:float, presence_penalty:float):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

@dataclass
class ServerConfig:
    """
    Represents the configuration for the server.

    Attributes:
        host (str): The host address for the server.
        port (int): The port number for the server.
    """

    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port


@dataclass
class DatabaseConfig:
    """
    Represents the configuration for the database.

    Attributes:
        db_filename (str): The filename of the database file.
    """

    def __init__(self, db_file:str):
        self.db_file = db_file


@dataclass
class LoggingConfig:
    """
    Represents the configuration for logging.
    
    Attributes:
        log_filename (str): The filename for the log file.
        log_level (str): The logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
    """

    def __init__(self, log_file:str, log_level:str):
        self.log_file = log_file
        self.log_level = log_level