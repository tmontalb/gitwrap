"""
YAML Serializer Module
An independent, standard-library alternative to PyYAML.
"""

def to_yaml(data: dict) -> str:
    """
    Converts a flat dictionary containing strings, booleans, and list of strings
    into a clean, valid YAML representation without needing external dependencies.
    """
    lines = []
    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, bool):
            lines.append(f"{key}: {str(value).lower()}")
        elif isinstance(value, list):
            if not value:  # Requirement: omit empty collections
                continue
            lines.append(f"{key}:")
            for item in value:
                # Basic string escaping if it contains special characters
                if any(c in item for c in [":", "#", "[", "]", "{", "}"]):
                    lines.append(f'  - "{item}"')
                else:
                    lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines)