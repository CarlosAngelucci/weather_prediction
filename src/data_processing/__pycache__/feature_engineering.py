# %%
import pandas as pd
import os
import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.load_yaml_config import load_yaml_config
# %%
def create_lag_features(df, lags=range(1, 4)):
    """
    Create lagged features for the specified columns in the DataFrame.

    This function takes a DataFrame and a range of lag values, then 
    creates new columns in the DataFrame that represent lagged versions 
    of the specified features. The lagged features are generated by shifting 
    the original features by the specified lag periods.

    Args:
        df (pd.DataFrame): The input DataFrame containing the original features.
        lags (iterable, optional): A range of integers representing the lag periods 
                                   to create. Defaults to range(1, 4), which 
                                   generates lagged features for 1, 2, and 3 hours.

    Returns:
        pd.DataFrame: A DataFrame containing the original features along with the 
                       newly created lagged features.

    Raises:
        KeyError: If specified features in the YAML configuration are not present 
                  in the DataFrame.
    """
    yaml_config = load_yaml_config()
    features = yaml_config['features'][1:]

    for feature in features:
        for lag in lags:
            df[f'{feature}_lag_{lag}'] = df[feature].shift(lag)
        
    df.dropna(inplace=True)

    df_final = df[features + [f'{feature}_lag_{lag}' for feature in features for lag in lags]]
    return df_final
# %%
def feature_engineering(df):
    df_engineered = create_lag_features(df)
    return df_engineered