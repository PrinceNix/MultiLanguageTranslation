# src/utils/config_reader.py
import yaml
from src.utils.logger import setup_logger

logger = setup_logger("config_reader")

def load_config(config_path):
    """Load configuration from a YAML file."""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Configuration loaded from {config_path}")
            return config
    except Exception as e:
        logger.error(f"Failed to load config: {str(e)}")
        raise