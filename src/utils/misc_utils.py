import os
import json
import logging.config
from datetime import datetime

def load_json(file_path: str):
    """
    Loads a JSON file.

    Args:
    -------
    file_path: str
        Path to the JSON file.
    
    Returns:
    -------
    generator
    """
    for l in open(file_path, "r"):
        yield json.loads(l)


def setup_logger(log_dir: str):
    """
    Sets up a logger.

    Args:
    -------
    log_dir: str
        Path to the directory where the log file will be saved.
    
    Returns:
    -------
    None
        The logger configuration is changed to our preferred settings.
    """
    now = datetime.now()
    filename = f"{now.year}-{now.month}-{now.day}.log"
    logging.basicConfig(
        filename=os.path.join(log_dir, filename),
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d | %(levelname)-8s | %(module)-18s | %(funcName)-20s: %(lineno)-4d | %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return