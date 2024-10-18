import yaml
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(f)
    return config

def get_model(config):
    model_type = config['model_type']
    params = config['params']

    if model_type == 'RandomForest':
        model = RandomForestRegressor(**params)
    elif model_type == 'XGBoost':
        model = xgb.XGBRegressor(**params)
    else:
        raise ValueError(f"Model type {model_type} not supported")
    return model