from typing import Any

import yaml
from pydantic import BaseModel


def create_yaml_object(  # type: ignore[misc]
    yaml_file: str,
    yaml_object_type: type[BaseModel],
) -> Any:
    with open(yaml_file, "r") as yaml_file_io:
        yaml_data = yaml.safe_load(yaml_file_io)
        return yaml_object_type.model_validate(yaml_data)
