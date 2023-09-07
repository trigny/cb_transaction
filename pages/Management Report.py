
import time  # to simulate a real time data, time loop
import datetime
#required for building the interactive dashboard
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
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
    return pd.read_csv(dataset_url)

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

# dashboard title
st.title("Management Report")

years = [2023, 2022,2021,2020,2019,2018,2017]

# top-level filters
year_filt = st.selectbox("Year", years)

st.markdown("#### Per Trader")

# rows = ['AA', 'AD', 'FG', 'GP', 'HN', 'JG', 'NVB', 'AT', 'Total']
# columns = ['BCO', 'CCA', 'CCA NS', 'CCO', 'CCO0', 'CCO8', 'GCCO', 'CEE', 'CER', 'EUA', 'GOO', 'RECs', 'SC', 'VER', 'Total']

# table = [
#     ['-', 'BCO', 'CCA', 'CCA NS', 'CCO', 'CCO0', 'CCO8', 'GCCO', 'CEE', 'CER', 'EUA', 'GOO', 'RECs', 'SC', 'VER', '-'],
#     ['AA', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
#     ['AD', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
#     ['FG', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
#     ['GP', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
#     ['HN', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
#     ['JG', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
#     ['NVB', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
#     ['AT', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
#     ['Total', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
# ]

# for row in table:
#     print('\t'.join(row))
    
    
    
result = pd.DataFrame()  
data_new = []
contactCBM = df['Contact CBM'].unique()
contactCBM = contactCBM[~pd.isnull(contactCBM)]
for contact in contactCBM:

    temp = df[(df['Delivery Date'].dt.year == year_filt)]
    
    temp = temp[['P&L', 'Fee', 'Currency', 'Contact CBM', 'Compliance Instrument Type']]
    
    PL =  ((temp['Contact CBM'] == contact)) * temp['P&L'] * ((temp['Currency'] == 'EUR') * df_currency['Values'][0] + (temp['Currency'] == 'CAD') * df_currency['Values'][1] + (temp['Currency'] == 'GBP') * df_currency['Values'][2] + (temp['Currency'] == 'USD')*1
    )
    Fee = ((temp['Contact CBM'] == contact)) * temp['Fee'] * ((temp['Currency'] == 'EUR') * df_currency['Values'][0] + (temp['Currency'] == 'CAD') * df_currency['Values'][1] + (temp['Currency'] == 'GBP') * df_currency['Values'][2] + (temp['Currency'] == 'USD')*1
    )
    
    PL = PL.replace(np.nan, 0)
    Fee = Fee.replace(np.nan, 0)
    
    total = PL + Fee

    # result = pd.DataFrame()   
    # result = result.assign(contact = total)
    # result['Compliance Instrument Type'] = temp['Compliance Instrument Type']
        
    # result.groupby(['Compliance Instrument Type']).sum()
    
    print(contact)
    # Append the dictionary to the list of data
    data_new.append(total)
    result[contact] = total

result['Compliance Instrument Type'] = df[(df['Delivery Date'].dt.year == year_filt)]['Compliance Instrument Type']
result = result.groupby(['Compliance Instrument Type']).sum()
# Calculate the totals for each column
column_totals = result.sum()

# Create a new DataFrame for the totals row
totals_df = pd.DataFrame([column_totals.tolist()], columns=result.columns)

# Concatenate the original DataFrame with the totals DataFrame
result = pd.concat([result, totals_df])
as_list = result.index.tolist()
idx = as_list.index(0)
as_list[idx] = 'Total'
result.index = as_list
result = result.astype(int)
result['Total'] = result.sum(axis=1)
def highlight_last_row(s):
    return ['background-color: yellow' if i == len(s) - 1 else '' for i, _ in enumerate(s)]


st.dataframe(result.style.apply(highlight_last_row, axis=0), use_container_width = True)


st.markdown("#### Per Team")

result = pd.DataFrame()  
data_new = []
Teams = df['Client Type'].unique()
Teams = Teams[~pd.isnull(Teams)]

for team in Teams:

    temp = df[(df['Delivery Date'].dt.year == year_filt)]
    
    temp = temp[['P&L', 'Fee', 'Currency', 'Client Type', 'Compliance Instrument Type']]
    
    PL =  ((temp['Client Type'] == team)) * temp['P&L'] * ((temp['Currency'] == 'EUR') * df_currency['Values'][0] + (temp['Currency'] == 'CAD') * df_currency['Values'][1] + (temp['Currency'] == 'GBP') * df_currency['Values'][2] + (temp['Currency'] == 'USD')*1
    )
    Fee = ((temp['Client Type'] == team)) * temp['Fee'] * ((temp['Currency'] == 'EUR') * df_currency['Values'][0] + (temp['Currency'] == 'CAD') * df_currency['Values'][1] + (temp['Currency'] == 'GBP') * df_currency['Values'][2] + (temp['Currency'] == 'USD')*1
    )
    
    PL = PL.replace(np.nan, 0)
    Fee = Fee.replace(np.nan, 0)
    
    total = PL + Fee
    
    print(team)
    # Append the dictionary to the list of data
    data_new.append(total)
    result[team] = total

result['Compliance Instrument Type'] = df[(df['Delivery Date'].dt.year == year_filt)]['Compliance Instrument Type']
result = result.groupby(['Compliance Instrument Type']).sum()
# Calculate the totals for each column
column_totals = result.sum()

# Create a new DataFrame for the totals row
totals_df = pd.DataFrame([column_totals.tolist()], columns=result.columns)

# Concatenate the original DataFrame with the totals DataFrame
result = pd.concat([result, totals_df])
as_list = result.index.tolist()
idx = as_list.index(0)
as_list[idx] = 'Total'
result.index = as_list
result = result.astype(int)
result['Total'] = result.sum(axis=1)
def highlight_last_row(s):
    return ['background-color: yellow' if i == len(s) - 1 else '' for i, _ in enumerate(s)]


st.dataframe(result.style.apply(highlight_last_row, axis=0), use_container_width = True)
