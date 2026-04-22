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


# Define outlier function
def outliers(df):
    """
    Function to get outliers from numerical columns

    Parameters: dataframe
    Returns: count and % of outliers for each series containing at least one outlier
    """
    # Initialize empty list to store names of columns with outliers
    outlier_col = {}

    # Loop through columns
    for i in df.columns:
        col = df[i]
        # Check if column is numerical before proceeding
        if col.dtype == 'int64' or col.dtype == 'float64': 
            # Get first and third quartiles
            q1, q3 = col.quantile([0.25, 0.75])
            # Get IQR
            IQR = q3 - q1
            # Get upper and lower limits
            upper_lim = q3 + 1.5 * IQR
            lower_lim = q1 - 1.5 * IQR

            # Count outliers below lower limit
            below = (col < lower_lim).sum()
            # Count outliers above upper limit
            above = (col > upper_lim).sum()
            # Total outliers
            total_outliers = below + above
            # Get percentage of outliers
            percentage = (total_outliers / len(col)) * 100

            # Assign to dictionary if there are outliers
            if total_outliers > 0:
                outlier_col[i] = {'count': total_outliers, 'percentage': percentage}
        # Convert dictionary to dataframe for nicer output
        nicer_output = pd.DataFrame.from_dict(outlier_col)
    return nicer_output


# PLOTTING FUNCTIONS

def donut_permit_types(df):
    """
    Create a donut chart showing the distribution of permit types.
    
    Parameters: df
    
    Returns: None (displays the chart)
    """

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8,6))

    explode = (0.05, 0, 0, 0.1, 0, 0, 0, 0, 0, 0)

    x = df['permit_type'].value_counts()
    x = x[x > 1500]  # only keep permit types with more than 1000 permits
    y = y = x.index

    ax.pie(x, autopct='%1.1f%%', explode=explode, wedgeprops={'width': 0.5}, colors=plt.cm.tab20.colors)

    ax.set_title('Dominance of Permit Types')
    ax.legend(y)
    plt.tight_layout()



def top_neighbourhoods(df, n):

    """
    Create side by side scatterplots for top 'n' neighbourhoods 
    according to number of Housing permits and number
    of Multi-Residential permits

    Parameters:
        df: dataframe
        n: desired number of top neighbourhoods to display
    
    Returns: None (charts)
    """

    import seaborn as sns 
    import matplotlib.pyplot as plt
    import colorcet as cc # To get a larger colour palette than sns and plt offer

    fig, ax = plt.subplots(1, 2, figsize=(20, 6))


    """
    Filter df for Housing and Multi-Residential permits
    """
    # Filter df for only New Construction

    df_new = df[(df['work_type'] == 'Construct New')]

    # Filter df for Housing and Multi-Residential permits
    housing_multi = df[df['permit_type'].isin(['Housing', 'Multi-Residential'])]
    # Count permits per neighbourhood and permit type combination in filtered df
    counts = housing_multi.groupby(['neighbourhood_name',
                                    'permit_type']).size().reset_index(name='count')
    # Pivot so rows are neighbourhood names and columns are permit types fill NaN
    pivotted = counts.pivot(index='neighbourhood_name', 
                            columns='permit_type', values='count').fillna(0)


    """
    Top 10 neighbourhoods by Housing permit count
    """
    # Get top 10 neighbourhoods by housing permit count; set index to names
    top_n_house = pivotted['Housing'].sort_values(ascending=False).head(15).index
    # Filter pivotted df for top_n_house; reset index to use names in scatter plot
    pivot_n_house = pivotted.loc[top_n_house].reset_index()


    """
    Top 10 neighbourhoods by Multiple-Residential permit count
    """

    # Get top 10 neighbourhoods by multi-residential permit count;set index to names
    top_n_mr = pivotted['Multi-Residential'].sort_values(ascending=False).head(n).index
    # Filter pivotted df for top_10 and reset index to a column for scatter plot
    pivot_n_mr = pivotted.loc[top_n_mr].reset_index()


    """
    Create colour map so neighbourhoods that appear in both sets share a colour
    """

    # Converts top_10_house and top_10_mr index to list to concatenate, then to set to remove duplicates
    top_all = list(set(list(top_n_house) + list(top_n_mr)))
    # Set color palette
    colours = sns.color_palette(cc.b_glasbey_bw_minc_20_maxl_70, n_colors=len(top_all))
    # Convert to tuple to pair up neighbourhood_names w/ colours, then to dict to feed to sns
    color_map = dict(zip(top_all, colours))


    """
    Plot both axes
    """
    # Plot Housing
    sns.scatterplot(data=pivot_n_house, x='Housing', y='Multi-Residential', 
                    hue='neighbourhood_name', s=100, ax=ax[0], palette=color_map)
    # Get rightmost and topmost value (max on both axes) to plot diagonal
    max_val2 = max(pivot_n_house['Housing'].max(), pivot_n_mr['Multi-Residential'].max())
    # Plot diagonal line
    ax[0].plot([1, max_val2], [1, max_val2], 'k--', alpha=0.3)

    # Set scales to log to spread out heavily clustered values
    ax[0].set_xscale('log')
    ax[0].set_yscale('log')

    # Set titles
    ax[0].set_title('Top 15 Neighbourhoods by Housing Permits')


    # Plot 'Multi-Residential'
    sns.scatterplot(data=pivot_n_mr, x='Housing', y='Multi-Residential', 
                    hue='neighbourhood_name', s=100, ax=ax[1], palette=color_map)
    # Get rightmost and topmost value (max on both axes) to plot diagonal
    max_val2 = max(pivot_n_mr['Housing'].max(), pivot_n_mr['Multi-Residential'].max())
    # Plot diagonal
    ax[1].plot([1, max_val2], [1, max_val2], 'k--', alpha=0.3)

    # Set scales to log to spread out heavily clustered values
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')

    # Set titles
    ax[1].set_title(f'Top {n} Neighbourhoods by Multi-Residential Permits')

    # Set figure title
    fig.suptitle('Data Shows Winnipeg Builds Out, Not Up', fontsize=16)



def building_up_out(df):
    """
    Create a scatter plot of all neighbourhoods 
    by number of Housing permits and number
    of Multi-Residential permits w/ diagonal axline
    dividing the plot into 'buiding up' or 'building out' zones

    Parameter: dataframe
    Returns: None (chart)
    
    """


    import seaborn as sns 
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))

    # Filter df for Housing and Multi-Residential permits
    housing_multi = df[df['permit_type'].isin(['Housing', 'Multi-Residential'])]

    # Count permits per neighbourhood and permit type combination
    counts = housing_multi.groupby(['neighbourhood_name', 'permit_type']).size().reset_index(name='count')
    # Pivot so rows are individual neighbourhoods and columns are permit types and fill NaN values w/ 0 (need to be numerical)
    pivotted = counts.pivot(index='neighbourhood_name', columns='permit_type', values='count').fillna(0)


    # Plot graph w/ all neighbourhoods
    sns.scatterplot(data=pivotted, x='Housing', y='Multi-Residential', ax=ax)
    # Find the max value across both axes to stretch diagonal line far enough
    max_val = max(pivotted['Housing'].max(), pivotted['Multi-Residential'].max())
    # Plot diagonal from 0 to max_val
    ax.plot([1, max_val], [1, max_val], 'k--', alpha=0.3)

    # Set scales to log to spread out heavily clustered values
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Set titles
    ax.set_title('Data Shows That Most Winnipeg Neighbourhoods Build Out, Not Up')
