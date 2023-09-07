
import time  # to simulate a real time data, time loop
import datetime
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

st.title("Invenvtory")

dataset_url = 'Transactions.csv'
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

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

# Data from the table
data_inv = {
    'Inventory': ['Spot', 'Value USD'],
    'VER': [27120, 244080],
    'CER': [0, 0],
    'EUA': [0, 0],
    'CCA': [56, 1792],
    'CCO': [0, 0]
}

# Create the DataFrame
df_inv = pd.DataFrame(data_inv)
df_inv.set_index('Inventory', inplace=True)
df_inv = df_inv.astype('int')



result = pd.DataFrame()  
data_new = []



temp = df[['Volume', 'Compliance Instrument Type', 'Comment']]
result = pd.DataFrame(columns=['Spot']) 
data_new = []
for comp in temp['Compliance Instrument Type'].unique():
    print(comp)
    spot = sum(((temp['Compliance Instrument Type'] == comp)) * ((temp['Comment'].str.lower() == ('OTC ClearBlue').lower())) *(temp['Volume']))
    data_new.append(spot)
    result.loc[comp] = spot

result['Value USD'] = result['Spot'] * [39.23, 30, 1, 40, 1, 9, 1, 1, 1, 1, 1, 1, 1, 1]
result = result.astype(int)

# result.groupby(['Compliance Instrument Type']).sum()

result = result.transpose()
filtered_df = result.loc[:, (result != 0).any(axis=0)]
st.caption('If compliance instrument type is not displayed, then spot value is 0')
st.dataframe(filtered_df, use_container_width = True)



# kpiVER, kpiCER, kpiEUA, kpiCCA, kpiCCO = st.columns(5)

# # fill in those three columns with respective metrics or KPIs
# kpiVER.metric(
#     label="VER",
#     value=f"{df_inv['VER'][0]:,}",
#     delta=f"$ {df_inv['VER'][1]:,}"
# )

# kpiCER.metric(
#     label="CER",
#     value=f"{df_inv['CER'][0].round(0):,}",
#     delta=f"$ {df_inv['CER'][1]:,}"
# )

# kpiEUA.metric(
#     label="EUA",
#     value=f"{df_inv['EUA'][0]:,}",
#     delta=f"$ {df_inv['EUA'][1]:,}"
# )

# kpiCCA.metric(
#     label="CCA",
#     value=f"{df_inv['CCA'][0]:,}",
#     delta=f"$ {df_inv['CCA'][1]:,}"
# )

# kpiCCO.metric(
#     label="CCO",
#     value=f"{(df_inv['CCO'][0]).round(0):,}",
#     delta=f"$ {df_inv['CCO'][1].round(2):,}"
# )
condition = df[(df['Compliance Instrument Type'] == 'VER') & (df['Comment'].str.lower() == 'OTC ClearBlue'.lower())]

VER_table = df[((df['Compliance Instrument Type'] == 'VER') & (df['Comment'].str.lower() == 'OTC ClearBlue'.lower()))]
pivot_table = condition.pivot_table(
    values = 'Volume',
    index=['Protocol', 'Vintage Start', 'Vintage End'],
    aggfunc= 'sum'
)
pivot_table = pivot_table.reset_index()

total = sum(VER_table['Volume'])

total_row = pd.DataFrame({'Protocol': ['Total'], 'Vintage Start': None, 'Vintage End': None, 'Volume': [total]})

result = pd.concat([pivot_table, total_row], ignore_index=True).set_index('Protocol')

st.markdown("***")
# Display the styled DataFrame




condition2 = df[(df['Compliance Instrument Type'] == 'CCA') & (df['Comment'].str.lower() == 'OTC ClearBlue'.lower())]

CCA_table = df[((df['Compliance Instrument Type'] == 'CCA') & (df['Comment'].str.lower() == 'OTC ClearBlue'.lower()))]
pivot_table2 = condition2.pivot_table(
    values = 'Volume',
    index=['Vintage Start', 'Vintage End'],
    aggfunc= 'sum'
)
pivot_table2 = pivot_table2.reset_index()

total2 = sum(CCA_table['Volume'])

total_row2 = pd.DataFrame({'Vintage Start': None, 'Vintage End': None, 'Volume': [total2]})
result2 = pd.concat([pivot_table2, total_row2], ignore_index=True)
as_list = result2.index.tolist()
idx = as_list.index(4)
as_list[idx] = 'Total'
result2.index = as_list

col5, col1, col2, col3, col4= st.columns((1,7,1,7,1))
with col1:
    st.caption('Volume per VER protocol')
    st.dataframe(result, use_container_width = True)
with col3:
    st.caption('Volume per CCA protocol')
    st.dataframe(result2, use_container_width = True)

st.markdown("***")