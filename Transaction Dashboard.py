
import time  # to simulate a real time data, time loop
import datetime
from datetime import date
#required for building the interactive dashboard
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st
from streamlit.runtime.state import SessionState  # 🎈 data web app development
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(
    page_title="Real-Time Dashboard",
    page_icon="✅",
    layout="wide"
)



def main_page():
    st.sidebar.markdown("# Main page ")

def page1():
    st.markdown("# Input ")
    st.sidebar.markdown("# Input ")

def page2():
    st.markdown("# Inventory 🎉")
    st.sidebar.markdown("# Inventory 🎉")
    
def page3():
    st.markdown("# Analysis ")
    st.sidebar.markdown("# Analysis ")


page_names_to_funcs = {
    "Main Page": main_page,
    "Page 1": page1,
    "Page 2": page2,
    "Page 3": page3,
}

st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    
    
dataset_url = 'Transactions.csv'

def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url, encoding='utf-8')

df = get_data()

# Convert the "Date" column to a datetime format
df['Trade Date'] = pd.to_datetime(df['Trade Date'], format='mixed', dayfirst=True)
df['Trade Date'] = df['Trade Date'].dt.date

df['Delivery Date'] = pd.to_datetime(df['Delivery Date'], format='mixed', dayfirst=True)

currency = {
    'Exchange': ['EUR:USD', 'CAD/USD', 'GBP/USD'],
    'Values': [1.07, 0.73, 1.26]
}

df_currency = pd.DataFrame(currency)
df_currency.set_index('Exchange', inplace=True)


data_new = []
for year in df['Delivery Date'].dt.year.unique():
    for compliance in df['Compliance Instrument Type'].unique():
        
        temp = df[(((df['Comment'].str.lower().isin([("OTC ClearBlue").lower(), ("OTC ClearBlue BtB").lower()]))) & (df['Delivery Date'].dt.year == year))] 
             
        fee =  np.sum(temp['Fee'] * (
        (temp['Currency'] == 'EUR') * df_currency['Values'][0] +  (temp['Currency'] == 'CAD') * df_currency['Values'][1] + (temp['Currency'] == 'GBP') * df_currency['Values'][2] + (temp['Currency'] == 'USD')*1
        ))
        
        tempPL = df[((df['Compliance Instrument Type'] == compliance) & (df['Comment'].str.lower() == ("OTC ClearBlue").lower()) & (df['Delivery Date'].dt.year == year))]  
    
        PL = np.sum(tempPL['P&L'] * (
        (tempPL['Currency'] == 'EUR') * df_currency['Values'][0] + (tempPL['Currency'] == 'CAD') * df_currency['Values'][1] + (tempPL['Currency'] == 'GBP') * df_currency['Values'][2] + (tempPL['Currency'] == 'USD')*1
        ))
        volume = np.sum((df['Delivery Date'].dt.year == year).astype(int) * (df['Compliance Instrument Type'] == compliance).astype(int) * abs(df['Volume']))
        total = fee + PL
        margin = total/volume
        # Create a dictionary with the values for each column
        data_entry = {
            'Year': year,
            'Compliance Instrument Type': compliance,
            'P&L': PL,  # Placeholder for empty value
            'Fee': fee,    # Placeholder for empty value
            'Volume': volume,
            'Total': total,
            'Margin': margin
        }
        # Append the dictionary to the list of data
        data_new.append(data_entry)
        print(year)
        print(compliance)
        
        
for compliance in df['Compliance Instrument Type'].unique(): 
    
    temp = df[(df['Comment'].str.lower().isin([("OTC ClearBlue").lower(), ("OTC ClearBlue BtB").lower()]))] 
        
    fee =  np.sum(temp['Fee'] * (
    (temp['Currency'] == 'EUR') * df_currency['Values'][0] + (temp['Currency'] == 'CAD') * df_currency['Values'][1] + (temp['Currency'] == 'GBP') * df_currency['Values'][2] + (temp['Currency'] == 'USD')*1
    ))
    
    tempPL = df[((df['Compliance Instrument Type'] == compliance) & (df['Comment'].str.lower() == ("OTC ClearBlue").lower()))]  
    
    PL = np.sum(tempPL['P&L'] * (
    (tempPL['Currency'] == 'EUR') * df_currency['Values'][0] + (tempPL['Currency'] == 'CAD') * df_currency['Values'][1] + (tempPL['Currency'] == 'GBP') * df_currency['Values'][2] + (tempPL['Currency'] == 'USD')*1
    ))
    volume = np.sum((df['Compliance Instrument Type'] == compliance).astype(int) * abs(df['Volume']))
    total = fee + PL
    margin = total/volume
        
    # Create a dictionary with the values for each column
    data_entry = {
        'Year': 'Total',
        'Compliance Instrument Type': compliance,
        'P&L': PL,  # Placeholder for empty value
        'Fee': fee,    # Placeholder for empty value
        'Volume': volume,
        'Total': total,
        'Margin': margin
    }
    # Append the dictionary to the list of data
    data_new.append(data_entry)
    print(year)
    print(compliance)
    
for year in df['Delivery Date'].dt.year.unique(): 
    temp = df[(df['Delivery Date'].dt.year == year)] 
    fee =  np.sum(temp['Fee'] * (
        (temp['Currency'] == 'EUR') * df_currency['Values'][0] + (temp['Currency'] == 'CAD') * df_currency['Values'][1] + (temp['Currency'] == 'GBP') * df_currency['Values'][2] + (temp['Currency'] == 'USD')*1
        ))
    
    tempPL = df[((df['Delivery Date'].dt.year == year) & (df['Comment'].str.lower().isin([("OTC ClearBlue").lower(), ("OTC ClearBlue BtB").lower()])))] 
    tempPL = tempPL.replace(np.nan, 0)
    PL = np.sum(tempPL['P&L'] * (
        (tempPL['Currency'] == 'EUR') * df_currency['Values'][0] + (tempPL['Currency'] == 'CAD') * df_currency['Values'][1] + (tempPL['Currency'] == 'GBP') * df_currency['Values'][2] + (tempPL['Currency'] == 'USD')*1
        ))
    
    volume = np.sum((df['Delivery Date'].dt.year == year).astype(int) * abs(df['Volume']))
    total = fee + PL
    margin = total/volume
    # Create a dictionary with the values for each column
    data_entry = {
        'Year': year,
        'Compliance Instrument Type': 'Total',
        'P&L': PL,  # Placeholder for empty value
        'Fee': fee,    # Placeholder for empty value
        'Volume': volume,
        'Total': total,
        'Margin': margin
    }
    # Append the dictionary to the list of data
    data_new.append(data_entry)
    print(year)
    print(compliance)

fee =  np.sum(df['Fee'] * (
    (df['Currency'] == 'EUR') * df_currency['Values'][0] + (df['Currency'] == 'CAD') * df_currency['Values'][1] + (df['Currency'] == 'GBP') * df_currency['Values'][2] + (df['Currency'] == 'USD')*1
    ))
PL = np.sum( (df['Comment'] == "OTC ClearBlue").astype(int) * df['P&L'] * (
    (df['Currency'] == 'EUR') * df_currency['Values'][0] + (df['Currency'] == 'CAD') * df_currency['Values'][1] + (df['Currency'] == 'GBP') * df_currency['Values'][2] + (df['Currency'] == 'USD')*1
    ))
volume = np.sum(abs(df['Volume']))
total = fee + PL
margin = total/volume
data_entry = {
        'Year': 'Total',
        'Compliance Instrument Type': 'Total',
        'P&L': PL,  # Placeholder for empty value
        'Fee': fee,    # Placeholder for empty value
        'Volume': volume,
        'Total': total,
        'Margin': margin
    }

data_new.append(data_entry)
   
df_new = pd.DataFrame(data_new)
df_new = df_new.round(2)
df_new['Volume'] = df_new['Volume'].astype(int)

df['Delivery Date'] = df['Delivery Date'].dt.date
# Data from the table
data_out = {
    'Year' : ['Total'],
    'Compliance Instrument Type' : ['Total'],
    'P&L' : [None], 
    'Fee' : [None],
    'Volume' : [None],
    'Total' : [None],
    'Margin' : [None],
}
# Create the DataFrame
df_out = pd.DataFrame(data_out)

# dashboard title
st.title("Transaction dashboard")
years = [2023, 2022,2021,2020,2019,2018,2017,'Total']
comp_ins_type = pd.unique(df_new['Compliance Instrument Type'])
comp_ins_type = comp_ins_type[::-1]

# top-level filters
year_filter, compliance_type = st.columns(2)
with year_filter:
    year_filt = st.selectbox("Year", years)
with compliance_type:
    comp_type = st.selectbox("Compliance Instrument Type", comp_ins_type)
    
# creating a single-element container
placeholder = st.empty()

df_new = df_new.replace(np.NaN, 0)
condition = (df_new['Year'] == year_filt) & (df_new['Compliance Instrument Type'] == comp_type)
df_out['P&L'][0] = df_new.loc[condition, 'P&L'].values[0]
df_out['Fee'][0] = df_new.loc[condition, 'Fee'].values[0]
df_out['Volume'][0] = df_new.loc[condition, 'Volume'].values[0]

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

# Function to save changes to the CSV file
def save_changes(data):
    # Replace 'your_updated_data.csv' with your desired output CSV file
    data.to_csv('book1.csv', index=False)

# Function to update the initial DataFrame
def update_initial_df(df, edited_df):
    # Replace the rows in the initial DataFrame with the edited rows
    df.loc[df.index.max() + 1] = edited_df.loc[edited_df.index.max()].values
    return df

def delete_row(df):
     # Replace the rows in the initial DataFrame with the edited rows
    df = df.drop(df.index[-1])
    return df

with placeholder.container():
    
    kpi2, kpi1, kpi4, kpi3, kpi5 = st.columns(5)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="P&L💸",
        value=f"$ {df_out['P&L'][0]:,}"
    )

    kpi2.metric(
        label="Fee 💲",
        value=f"$ {df_out['Fee'][0]:,}"
    )

    kpi3.metric(
        label="Volume 📶",
        value=f"{df_out['Volume'][0]:,} ",
    )

    kpi4.metric(
        label="Total 🟰",
        value=f"$ {(df_out['Fee'][0] + df_out['P&L'][0]).round(2):,} "
    )

    kpi5.metric(
        label="Margin 📝",
        value=f"{(((df_out['Fee'][0] + df_out['P&L'][0])/df_out['Volume'][0])).round(2)} "
    )
    

    # VER_table = df[(df['Compliance Instrument Type'] == 'VER') & (df['Comment'] == 'OTC ClearBlue')].set_index(['Protocol'])
    # pivot_table = df[(df['Compliance Instrument Type'] == 'VER') & (df['Comment'] == 'OTC ClearBlue')].pivot_table(
    #     values = 'Volume',
    #     index=['Protocol', 'Vintage End'],
    # )
    
    # with st.sidebar:
    #     pivot_table
    

    # create two columns for charts
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.markdown("#### Transaction P&L")
        fig = st.bar_chart(
            df_new[(df_new['Compliance Instrument Type'] == 'Total') & (df_new['Year'] !='Total') &  (df_new['Year'] !=2016)], 
            y=["P&L", "Fee"],
            x="Year"
        )
    
    with fig_col2:
        st.markdown("#### Margin")
        fig2 = st.bar_chart(df_new[(df_new['Compliance Instrument Type'] == 'Total') & (df_new['Year'] != 'Total') & (df_new['Year'] !=2016)], 
                            x="Year", 
                            y="Margin")
        
        
    st.markdown("### Detailed Data View")
    
    # Get today's date
    today = date.today()
    edited_df = st.data_editor(
        df.tail(),
        column_config={
            "Compliance Instrument Type": st.column_config.SelectboxColumn(
                options=df['Compliance Instrument Type'].unique(),
                required=True,
            )
        },
        hide_index=True,
        num_rows="dynamic"
    )
    
    # Submit button to save changes
    if st.button('Submit Changes'):
        try:
                # Update the initial DataFrame with the edited values
            df = update_initial_df(df, edited_df)
            # Save the updated initial DataFrame as a CSV file
            df.to_csv('Transactions.csv', index=False)
            # Display a success message
            st.success('Changes saved to CSV file.')
        except Exception as e:
            # Display an error message if something goes wrong
            st.error(f'Error while saving changes: {str(e)}')
    
        # Submit button to save changes
    if st.button('Delete Row'):
        try:
                # Update the initial DataFrame with the edited values
            df = delete_row(df)
            # Save the updated initial DataFrame as a CSV file
            df.to_csv('Transactions.csv', index=False)
            # Display a success message
            st.success('Changes saved to CSV file.')
            st.experimental_rerun()
        except Exception as e:
            # Display an error message if something goes wrong
            st.error(f'Error while saving changes: {str(e)}')
        
    @st.cache_data
    def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        label="Download",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )