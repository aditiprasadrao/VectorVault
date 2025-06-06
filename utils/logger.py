from loguru import logger
import sys
import yaml

def setup_logger(config_path: str = "config.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    log_config = config["logging"]
    logger.remove()  # Remove default logger
    logger.add(sys.stdout, level=log_config.get("level", "INFO"))

    if log_config.get("log_to_file"):
        logger.add(log_config["file_path"], level=log_config.get("level", "INFO"))

    return logger
