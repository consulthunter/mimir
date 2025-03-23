from typing import TypedDict, List

# Define the structure for each language's configuration
class LanguageConfig(TypedDict):
    name: str  # Language name
    extensions: list[str]

class ConfigSchema(TypedDict):
    max_concurrency: int
    log_dir: str
    temp_dir: str
    output_dir: str
    target: str
    languages: list[LanguageConfig]
    # Add more fields as needed
