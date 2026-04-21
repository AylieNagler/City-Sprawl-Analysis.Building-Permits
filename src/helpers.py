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

    Parameters: dataframe
    Returns: column names and data types in 2 columns

    """

    # Get column names and data types in a new dataframe
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



def nan_count(df):
    """
    Count the number of NaN values in each column of a 
    dataframe and returns in 2 columns

    Parameters: dataframe
    Returns: dataframe with column names and NaN counts

    """

    # Get column names and NaN counts in a new dataframe
    nan_counts = pd.DataFrame({
        "Column Names": df.columns,
        "NaN Count": df.isna().sum()
    })

    # Get halfway point of column names list
    half = (len(nan_counts) + 1) // 2

    # Index dataframe to split into two columns

    # Get first half of rows
    first_rows = nan_counts.iloc[:half].reset_index(drop=True)
    # Get rows from halfway onwards
    last_rows = nan_counts.iloc[half:].reset_index(drop=True)

    # Combine the two halves horizontally
    df_two_cols = pd.concat([first_rows, last_rows], axis=1)

    # Rename second set of columns for clarity
    df_two_cols.columns =  ["Column Names", "NaN Count",
                             "Column Names (cont.)", "NaN Count (cont.)"]

    # Replaced last row with empty string to avoid NaN
    df_two_cols = df_two_cols.fillna("")

    # Return results
    return df_two_cols


def extract_coords(df):
    """
    Geocode missing coordinates using the Google Maps API with the address column.

    Parameters: 
        dataframe containing coordinate columns w/ missing values
    returns:
        dataframe with coordinates filled in, list of addresses that failed to geocode

    """

    import googlemaps
    gmaps = googlemaps.Client(key='AIzaSyDPg-7ZNC4wmhVnNKMNQ6_NTPkI-tUkWOQ')

    # Initialize empty lists to append coordinates and fails to
    longitude = []
    latitude = []
    fails = []

    # Define df containing only rows where coordinates are missing
    missing_df = df[df['x_coordinate_nad83'].isna()].copy()


    for row in missing_df['address']:
        result = gmaps.geocode(row + ", Winnipeg, MB, Canada")
        # Check if geocode was successful
        if result:
            # Append long/lat from best result to lists
            latitude.append(result[0]['geometry']['location']['lat']) 
            longitude.append(result[0]['geometry']['location']['lng'])
        # Append to 'fail' list if geocode unsuccessful
        else:
            fails.append(row)
            latitude.append(None)
            longitude.append(None)

    # Add coords to missing_df
    missing_df['latitude'] = latitude
    missing_df['longitude'] = longitude

    # Index missing df to slot lat/long back in 
    df.loc[missing_df.index, 'x_coordinate_nad83'] = missing_df['latitude']
    df.loc[missing_df.index, 'y_coordinate_nad83'] = missing_df['longitude']

    return df, fails

def remove_time(column):
    """
    Remove Time from a column w/ 'YYYY-MM-DDT00:00:000' format

    Parameters:
        series: A pandas Series w/ datetime data
    Returns:
        values w/ time stripped
    """

    clean_column = pd.to_datetime(column)

    return clean_column


def get_suffix(column):
    """
    Get only characteres after the last space from a series

    Parameters: Pandas series with at least one space in its values
    Returns: suffix of rows in a pandas series
    """

    # Convert series to list to split suffix    
    column_values = column.tolist()

    # Initializes empty list to append suffixes to 
    suffixes = []

    # Loop through rows and split suffixes
    for row in column_values:
        suffixes.append(row.split()[-1])

    # Convert list to a set to remove duplicates (mimicking .unique())
    return(set(suffixes))
