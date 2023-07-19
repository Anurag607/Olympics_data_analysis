import pandas as pd
def mf_medal_tally(df,country):
    data = df[df['region'] == country]
    pivot_data = data.pivot_table(index='Medal', columns='Sex', values='ID', aggfunc='count', fill_value=0)
    
    # Ensure that both 'F' and 'M' columns are present with default value of 0
    if 'F' not in pivot_data.columns:
        pivot_data['F'] = 0
    if 'M' not in pivot_data.columns:
        pivot_data['M'] = 0
    
    # Convert values to integers
    pivot_data = pivot_data.astype(int)

    # Add a Total column
    new_row=pd.DataFrame({'F':pivot_data['F'].sum(),'M':pivot_data['M'].sum()},index=['Total'])
    pivot_data= pd.concat([new_row,pivot_data.loc[:]])

    # Reindexing the columns
    desired_order = ['Gold', 'Silver', 'Bronze', 'Total']
    pivot_data=pivot_data.reindex(desired_order, axis=0)

    # Fill NaN values with 0
    pivot_data = pivot_data.fillna(0)

    #Creating new dataframe for plotting
    data={
    'Medal':['Gold','Gold','Silver','Silver','Bronze','Bronze','Total','Total'],
    'Gender':['Male','Female','Male','Female','Male','Female','Male','Female'],
    'count':[pivot_data['M']['Gold'],pivot_data['F']['Gold'],pivot_data['M']['Silver'],pivot_data['F']['Silver'],pivot_data['M']['Bronze'],pivot_data['F']['Bronze'],pivot_data['M']['Total'],pivot_data['F']['Total']],
    }
    data=pd.DataFrame(data)

    return data

def mf_medal_pivot_data(df,country):
    data = df[df['region'] == country]
    pivot_data = data.pivot_table(index='Medal', columns='Sex', values='ID', aggfunc='count', fill_value=0)
    
    # Ensure that both 'F' and 'M' columns are present with default value of 0
    if 'F' not in pivot_data.columns:
        pivot_data['F'] = 0
    if 'M' not in pivot_data.columns:
        pivot_data['M'] = 0
    
    # Convert values to integers
    pivot_data = pivot_data.astype(int)

    # Add a Total column
    new_row=pd.DataFrame({'F':pivot_data['F'].sum(),'M':pivot_data['M'].sum()},index=['Total'])
    pivot_data= pd.concat([new_row,pivot_data.loc[:]])

    # Reindexing the columns
    desired_order = ['Gold', 'Silver', 'Bronze', 'Total']
    pivot_data=pivot_data.reindex(desired_order, axis=0)

    # Fill NaN values with 0
    pivot_data = pivot_data.fillna(0)

    return pivot_data
