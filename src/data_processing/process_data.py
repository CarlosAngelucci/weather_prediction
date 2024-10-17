import pandas as pd
import os
import json


def consolidate_weather_data(data_folder='data'):
    # Get all files in data folder
    files = os.listdir(data_folder)
    # Create an empty list to store the dataframes
    dfs = []
    # Loop through the files
    for file in files:
        # Check if the file is a csv file
        if file.endswith('.csv'):
            # Read the csv file
            df = pd.read_csv(os.path.join(data_folder, file))
            # Append the dataframe to the list
            dfs.append(df)
    # Concatenate all dataframes in the list
    df = pd.concat(dfs)
    # Return the concatenated dataframe
    return df

