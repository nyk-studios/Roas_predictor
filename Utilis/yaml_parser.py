import yaml
from collections import defaultdict


def read_and_create_objects_from_yaml(yaml_path):
    # Load the YAML file
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    # Dictionary to hold the created objects
    objects = defaultdict(list)

    # Assuming your YAML structure and processing accordingly
    components = config.get('components', {})
    return components

