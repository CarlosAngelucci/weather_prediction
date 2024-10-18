import yaml

yaml_path = '/Users/kaduangelucci/Documents/Estudos/weather_prediction/src/models/models_config.yaml'

def load_yaml_config(yaml_path=yaml_path):
    """
    Load configuration settings from a YAML file.

    This function reads a specified YAML file and returns its contents as a 
    Python dictionary. It uses the FullLoader to ensure all YAML types are 
    supported during the loading process.

    Args:
        yaml_path (str): The path to the YAML file to be loaded. Defaults to 
                         the variable 'yaml_path'.

    Returns:
        dict: A dictionary containing the configuration settings loaded from 
              the YAML file.
    """
    with open(yaml_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config