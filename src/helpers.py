"""
Helper functions for [Your Project Name].

This module contains reusable functions for data cleaning,
analysis, and visualization.
"""
import pandas as pd

# Exploratory functions

def split_columns(df):
    """
    Split long dataframes into two
    columns for better readability.

    Input: dataframe
    Output: column names and data types in 2 columns

    """

    col_df = pd.DataFrame({
    "Column Names": df.columns,
    "Data Type": df.dtypes,
    })

    # Get halfway point of column names list
    half = (len(col_df) + 1) // 2

    # Index dataframe to split into two columns
    first_rows = col_df.iloc[:half].reset_index(drop=True) # Get first half of rows
    last_rows = col_df.iloc[half:].reset_index(drop=True) # Get rows from halfway onwards

    # Combine the two halves horizontally
    df_two_cols = pd.concat([first_rows, last_rows], axis=1)

    # Rename second set of columns for clarity
    df_two_cols.columns =  ["Column Names", "Data Types", "Column Names (cont.)", "Data Types (cont.)"]

    # Replaced last row with empty string to avoid NaN
    df_two_cols = df_two_cols.fillna("")

    # Dispay results
    return df_two_cols
