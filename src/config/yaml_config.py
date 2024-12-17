import yaml


class YamlObject:
    @classmethod
    def from_yaml(cls, yaml_file):
        with open(yaml_file, "r") as yaml_config_file:
            yaml_data = yaml.safe_load(yaml_config_file)
        return cls.create_instance(yaml_data)  # type: ignore [no-untyped-call]

    @classmethod
    def create_instance(cls, input_data):
        if isinstance(input_data, dict):
            return cls(
                **{
                    config_key: cls.create_instance(config_value)  # type: ignore [no-untyped-call]
                    for config_key, config_value in input_data.items()
                },
            )
        elif isinstance(input_data, list):
            return [cls.create_instance(config_item) for config_item in input_data]  # type: ignore [no-untyped-call]

        return input_data
