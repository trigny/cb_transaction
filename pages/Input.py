
import time  # to simulate a real time data, time loop
import datetime
from datetime import date
#required for building the interactive dashboard
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import streamlit as st
from streamlit.runtime.state import SessionState  
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
df['Delivery Date'] = df['Delivery Date'].dt.date

currency = {
    'Exchange': ['EUR:USD', 'CAD/USD', 'GBP/USD'],
    'Values': [1.07, 0.73, 1.26]
}

df_currency = pd.DataFrame(currency)
df_currency.set_index('Exchange', inplace=True)


st.title("Transaction Form")

# Input fields
trade_date = st.date_input("Trade Date")
buyer = st.text_input("Buyer")
seller = st.text_input("Seller")
compliance_instrument_type = st.selectbox("Compliance Instrument Type", options=df['Compliance Instrument Type'].unique())
jurisdiction = st.selectbox("Jurisdiction", options=df['Jurisdiction'].unique())
contact_cbm = st.selectbox("Contact CBM", options=df['Contact CBM'].unique())
client_type = st.selectbox("Client Type", options=df['Client Type'].unique())
protocol = st.text_input("Protocol")
vintage_start = st.number_input("Vintage Start", min_value=2015, max_value=2030)
vintage_end = st.number_input("Vintage End", min_value=2015, max_value=2030)
volume = st.number_input("Volume")
price = st.number_input("Price")
price_mtm = st.number_input("Price for MtM")
pnl = st.number_input("P&L")
currency = st.selectbox("Currency", options=df['Currency'].unique())
comment = st.selectbox("Comment", options=df['Comment'].unique())
fee = st.number_input("Fee")
note = st.text_area("Note")
contract_signed = st.checkbox("Contract Signed")
invoice_received = st.checkbox("Invoice received")
delivery_date = st.date_input("Delivery Date")


# Function to update the initial DataFrame
def update_initial_df(df, edited_df):
    # Replace the rows in the initial DataFrame with the edited rows
    df.loc[df.index.max() + 1] = edited_df.loc[edited_df.index.max()].values
    return df


# Submit button
if st.button("Submit"):
    if not (trade_date and buyer and seller and compliance_instrument_type and jurisdiction and contact_cbm
            and client_type and protocol and vintage_start and vintage_end and volume
            and currency and delivery_date):
        st.warning("Please fill in all the required fields before submitting.")
    else:
        # Append form values to the DataFrame
        input = ({
            'Trade Date': [trade_date],
            'Buyer': [buyer],
            'Seller': [seller],
            'Compliance Instrument Type': [compliance_instrument_type],
            'Jurisdiction': [jurisdiction],
            'Contact CBM': [contact_cbm],
            'Client Type': [client_type],
            'Protocol': [protocol],
            'Vintage Start': [vintage_start],
            'Vintage End': [vintage_end],
            'Volume': [volume],
            'Price': [price],
            'Price for MtM': [price_mtm],
            'P&L': [pnl],
            'Currency': [currency],
            'Comment': [comment],
            'Fee': [fee],
            'Note': [note],
            'Contract Signed': [contract_signed],
            'Invoice received ': [invoice_received],
            'Delivery Date': [delivery_date]
        })
        input = pd.DataFrame(input)
        
        df = pd.concat([df, input], ignore_index=False)
        # st.write(df.tail())
        df.to_csv('Transactions.csv', index=False)
        st.success('Changes saved to CSV file.')
# Submit button to save changes
# if st.sidebar.button("Aprrove Changes"):
#     try:
#         # Update the initial DataFrame with the edited values
#         # Save the updated initial DataFrame as a CSV file
#         df.to_csv('Transactions.csv', index=False)
#         # Display a success message
#         st.success('Changes saved to CSV file.')
#     except Exception as e:
#         # Display an error message if something goes wrong
#         st.error(f'Error while saving changes: {str(e)}')
