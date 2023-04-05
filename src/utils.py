import os
import json


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