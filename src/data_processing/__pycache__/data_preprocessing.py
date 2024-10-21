
# %%
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import sys

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CODE_DIR))

from utils.load_yaml_config import load_yaml_config

# %%
path_config = load_yaml_config()
processed_data_path = path_config['paths']['processed_path_data']    
consolidate_data  = pd.read_csv(processed_data_path)

# %%
def preprocess_data(df):
    yaml_config = load_yaml_config()

    date_col = df['Date']

    target = yaml_config['target']
    X = df.drop(columns=[target, 'Date'], axis=1)
    y = df[target]

    #  dividindo os dados sem embaralhar, respeitando a ordem temporal
    split_index = int(len(X) * 0.8) # Ponto de corte (80% para treino e 20% para teste)
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #  dividindo as datas também
    date_col_train, date_col_test = date_col[:split_index], date_col[split_index:]
    # date_col_train, date_col_test = train_test_split(date_col, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test, date_col_test

