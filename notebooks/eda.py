# %% 
import pandas as pd
import sys
import os 

from pathlib import Path

code_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(code_dir))

from src.utils.load_yaml_config import load_yaml_config
from src.data_processing.__pycache__.feature_engineering import feature_engineering
from src.data_processing.__pycache__.data_preprocessing import preprocess_data


# %%
configs = load_yaml_config()
consoldiated_data_path = configs['paths']['processed_path_data']
features = configs['features']
features
# %%
df = pd.read_csv(consoldiated_data_path)
df.sort_values('Date', inplace=True)
df = df[features]
df
# %%
features_to_lag = features[1:]

for feature in features_to_lag:
    for lag in range(1, 4):
        df[f'{feature}_lag_{lag}'] = df[feature].shift(lag)
    
df.dropna(inplace=True)

df_final = df[features + [f'{feature}_lag_{lag}' for feature in features_to_lag for lag in range(1, 4)]]

df_final

# %%
X_train, X_test, y_tran, y_test, date_col_test = preprocess_data(df_final)
print('Shape of X_train:', X_train.shape)
print('Shape of X_test:', X_test.shape)
print('Shape of y_train:', y_tran.shape)
print('Shape of y_test:', y_test.shape)

# %%
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor

#  Create a dictionary with the hyperparameters of random forest
rf_params = {
    'n_estimators': [100, 200, 300, 500, 700, 1000],
    'max_depth': [None, 5, 10, 15, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Create a random forest regressor
rf = RandomForestRegressor()

# Create a grid search with the random forest regressor and the hyperparameters
rf_grid = GridSearchCV(rf, rf_params, cv=5, n_jobs=-1, verbose=2)

# Fit the grid search to the training data
rf_grid.fit(X_train, y_tran)

# Get the best hyperparameters
best_params = rf_grid.best_params_
best_params

# %%
# Create a random forest regressor with the best hyperparameters
rf_best = RandomForestRegressor(**best_params)

# Fit the random forest regressor to the training data
rf_best.fit(X_train, y_tran)

# %%
# Make predictions with the random forest regressor
y_pred = rf_best.predict(X_test)

# %%
from sklearn.metrics import mean_squared_error

# Calculate the mean squared error of the random forest regressor
mse = mean_squared_error(y_test, y_pred)
mse


# %%
# hyperparameters for a XGBoost regressor model
from xgboost import XGBRegressor
xgb_params = {
    'n_estimators': [100, 200, 300, 500, 700, 1000],
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.1, 0.3],
    'subsample': [0.5, 0.7, 1],
    'colsample_bytree': [0.5, 0.7, 1]
}

# Create a XGBoost regressor
xgb = XGBRegressor()

# Create a grid search with the XGBoost regressor and the hyperparameters
xgb_grid = GridSearchCV(xgb, xgb_params, cv=5, n_jobs=-1, verbose=2)

# Fit the grid search to the training data
xgb_grid.fit(X_train, y_tran)

# Get the best hyperparameters
best_params_xgb = xgb_grid.best_params_
best_params_xgb


# %%
# Create a XGBoost regressor with the best hyperparameters
xgb_best = XGBRegressor(**best_params_xgb)

# Fit the XGBoost regressor to the training data
xgb_best.fit(X_train, y_tran)

# Make predictions with the XGBoost regressor
y_pred_xgb = xgb_best.predict(X_test)

# Calculate the mean squared error of the XGBoost regressor
mse_xgb = mean_squared_error(y_test, y_pred_xgb)
mse_xgb

# %%
#  create a dataframw with the date, real and predicted value
df_final = pd.DataFrame({'Date': date_col_test, 
                         'Real': y_test, 
                         'Predicted - Random Forest': y_pred, 
                         'Predicted - XGBoost': y_pred_xgb})
# reset index
df_final.reset_index(drop=True, inplace=True)
df_final

# sort_values
df_final.sort_values('Date', inplace=True)
df_final
# %%
# plotar o df
import matplotlib.pyplot as plt

plt.figure(figsize=(20, 10))
plt.plot(df_final['Date'], df_final['Real'], label='Real')
plt.plot(df_final['Date'], df_final['Predicted - Random Forest'], label='Predicted - Random Forest')
plt.plot(df_final['Date'], df_final['Predicted - XGBoost'], label='Predicted - XGBoost')
plt.legend()
plt.show()

