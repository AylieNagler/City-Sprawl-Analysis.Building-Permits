# COMP2040-Assignment3

Data URL (shortened with bitly):
https://bit.ly/41NYUwK

### Dataset description
This dataset was sourced from The Winnipeg Open Data portal. It contains building permit data for the city of Winnipeg from January 4, 2010 to March 31, 2026. It was chosen for its analytical potential and relevancy for businesses in Winnipeg looking towards expansion. Through the analysis of this dataset one thing should become clear: the City of Winnipeg is expanding outwards, instead of upwards, which can have costly impacts on its infrastrucutre, quality of life, and the environment.

### Analytical questions
The analytical questions this project addresses are as follows:
1. Are Winnipeg Neighbourhoods growing up or out?
2. Are there any patterns indicating the geographical direction of growth in the city?
3. How have the types of permits changed over time?

### Helper script functions:
1. split_columns()
    - Displays dataframe column names in 2 columns w/ data type
2. nan_count()
    - Displays dataframe column names in 2 columns w/ NaN counts
3. split_dates()
    - Splits datetime columns from a dataframe into year, month, and day series
4. remove_time()
    - Removes time from datetime columns in a dataframe
5. get_suffix()
    - Splits series and pulls out the group of characters after the last space
6. outliers()
    - Gets count and percentage of outliers in all series containing at least one outlier
7. donut_permit_types()
    - Creates a donut chart showing the distribution of permit types.
8. top_neighbourhoods()
    - Creates side by side scatterplots for top 'n' neighbourhoods 
    according to number of Housing permits and number
    of Multi-Residential permits
9. building_up_out()
   - Creates a scatter plot of all neighbourhoods 
    by number of Housing permits and number
    of Multi-Residential permits w/ diagonal axline (1:1)
10. line_charts()
    - Creates overlaid line charts showing permit trends over time 
    for the top 5 permit types
11. rf()
    - Splits a dataframe into 60% train and 40% test, train a Random Forest 
    according to the parameters chosen by the user and return results in
    lists
12. stacked_bar()
    - Creates a stacked bar chart showing train and test accuracy
    of models
13. rf_model()
    - Trains a random forest model and returns just the model
14. show_tree()
    - Displays top nodes of first decision tree in a random forest


### How to run this analysis:
1. Clone the repository
2. Install required libararies (pandas, matplotlib, seaborn, sckikit-learn, and colorcet)
4. run the notebooks in order
    - `notebooks/analysis.ipynb`
    - `notebooks/cleaning.ipynb`
    - `notebooks/visual_analysis.ipynb`
  
