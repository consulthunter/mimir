import os
import json
from mimir.services.configuration.config_schema import ConfigSchema
from mimir.services.logger.logger import Logger

class Configuration:

    default_config = {
        "max_concurrency": 5,
        "log_dir": "logs",
        "temp_dir": "temp",
        "output_dir": "output",
        "target": os.path.join("examples", "java_example.txt"),
        "languages": [
            {
                "name": "java",
                "extensions": [
                    ".java"
                ],
            }
        ],
    }

    def __init__(self, config_file: str, logger: Logger):
        self.config_file = config_file
        self.logger = logger
        self.config: ConfigSchema = self.load_config()

        # attributes
        self.max_concurrency = self.config["max_concurrency"]
        self.log_dir = self.config["log_dir"]
        self.temp_dir = self.config["temp_dir"]
        self.output_dir = self.config["output_dir"]
        self.target = self.config["target"]
        self.languages = self.config["languages"]

    def load_config(self) -> ConfigSchema:
        if not os.path.exists(self.config_file):
            self.logger.log_error(f"Config file {self.config_file} does not exist")
            raise FileNotFoundError(f"Config file {self.config_file} does not exist")
        else:
            with open(self.config_file) as config_file:
                data = json.load(config_file)

            self.validate_config(data)

            return data

    def validate_config(self, data: dict):
        if data.keys() != self.default_config.keys():
            self.logger.log_error(f"Invalid configuration: invalid or missing configuration options.")
            raise KeyError(
                "Invalid configuration: invalid or missing configuration options."
            )

    @classmethod
    def create_default_config(cls, file_path: str, logger: Logger) -> None:
        cls.ensure_directory_exists(os.path.dirname(file_path), logger)

        with open(file_path, "w") as config_file:
            json.dump(cls.default_config, config_file, indent=4)
        logger.log_info(f"Default configuration file created at {file_path}")

    @staticmethod
    def ensure_directory_exists(directory_path: str, logger: Logger) -> None:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
            logger.log_info(f"Directory created at {directory_path}")
