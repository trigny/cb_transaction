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

def page2():
    st.markdown("# Inventory 🎉")
    st.sidebar.markdown("# Inventory 🎉")
    
def page3():
    st.markdown("# Analysis ")
    st.sidebar.markdown("# Analysis ")

page_names_to_funcs = {
    "Main Page": main_page,
    "Page 2": page2,
    "Page 3": page3,
}

st.title("Analysis")

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


result = pd.DataFrame()  
data_new = []

temp = df[['Buyer', 'Volume', 'Compliance Instrument Type', 'Comment', 'Delivery Date']]
temp = temp[(temp['Comment'].str.lower() == 'OTC ClearBlue'.lower()) | (temp['Comment'].str.lower() == 'OTC ClearBlue BTB'.lower()) | (temp['Comment'].str.lower() == 'OTC Direct'.lower()) | (temp['Comment'].str.lower() == 'OTC Evo'.lower())]
temp['offset'] = temp['Compliance Instrument Type'].apply(lambda x: 0 if x in ["CCA", "EUA", "SC"] else 1)
temp['abs volume'] = abs(temp['Volume'])
temp['Year'] = temp['Delivery Date'].dt.year

pivot_table1 = temp.pivot_table(
    values = 'abs volume',
    index=['Year', 'Buyer'],
    columns= 'offset',
    aggfunc= 'sum'
)


pivot_table1 = pivot_table1.reset_index()
Table1 = pd.DataFrame(pivot_table1)
Table1.rename(columns={'Year': 'Year', 'Buyer': 'Buyer', 0: 'Allowance', 1: 'Offset/REC'}, inplace=True)
# Table1['Year'] = pd.to_numeric(Table1['Year'])
Table1['Year']= Table1['Year'].astype(int)
Table1.set_index(['Year', 'Buyer'], inplace=True)


# total2 = sum(CCA_table['Volume'])

# total_row2 = pd.DataFrame({'Vintage Start': None, 'Vintage End': None, 'Volume': [total2]})
# result2 = pd.concat([pivot_table2, total_row2], ignore_index=True)
# as_list = result2.index.tolist()
# idx = as_list.index(4)
# as_list[idx] = 'Total'
# result2.index = as_list

col5, col1, col2, col3, col4= st.columns((1,5,1,5,1))
with col1:
    st.caption('Total Allowances and Offsets per Buyer')
    st.dataframe(Table1, use_container_width = True)
with col3:
    st.caption('Volume per CCA protocol')
    # st.dataframe(result2, use_container_width = True)

st.markdown("***")
