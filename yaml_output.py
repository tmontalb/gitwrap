"""
YAML Output Module
Serializes Python dictionaries into clean, machine-readable YAML.
"""

import yaml


def to_yaml(data: dict) -> str:
    """
    Converts a Python dictionary into YAML.

    Removes keys whose values are:
      - None
      - Empty lists

    Returns a YAML string.
    """

    cleaned = {}

    for key, value in data.items():

        if value is None:
            continue

        if isinstance(value, list) and not value:
            continue

        cleaned[key] = value

    return yaml.safe_dump(
        cleaned,
        sort_keys=False,
        default_flow_style=False
    ).rstrip()