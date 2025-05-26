import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

# Page Config
st.set_page_config(page_title="📉 Sales Forecast", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("../Data/data.csv", encoding='ISO-8859-1')
    df.dropna(inplace=True)
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

df = load_data()

# Sidebar selections
st.sidebar.header("🔍 Forecast Settings")
forecast_type = st.sidebar.selectbox("Forecast Type", ["Overall", "By Country", "By Product"])
frequency = st.sidebar.selectbox("Forecast Frequency", ["Daily", "Weekly", "Monthly"])

# Dynamic filtering based on selection
if forecast_type == "By Country":
    country_list = df['Country'].unique().tolist()
    selected_country = st.sidebar.selectbox("Select Country", country_list)
    df = df[df['Country'] == selected_country]
    title_suffix = f" - {selected_country}"
elif forecast_type == "By Product":
    product_list = df['Description'].value_counts().index.tolist()[:50]
    selected_product = st.sidebar.selectbox("Select Product", product_list)
    df = df[df['Description'] == selected_product]
    title_suffix = f" - {selected_product}"
else:
    title_suffix = ""

# Aggregation by frequency
if frequency == "Daily":
    df_grouped = df.resample('D', on='InvoiceDate').sum()
elif frequency == "Weekly":
    df_grouped = df.resample('W', on='InvoiceDate').sum()
else:  # Monthly
    df_grouped = df.resample('M', on='InvoiceDate').sum()

# Prepare data for Prophet
sales = df_grouped[['TotalPrice']].reset_index().rename(columns={"InvoiceDate": "ds", "TotalPrice": "y"})

# Title
st.title(f"📉 Sales Forecast{title_suffix}")
st.markdown(f"Forecasting **{frequency.lower()}** sales using **Facebook Prophet**.")

# Prophet Forecast
model = Prophet()
model.fit(sales)

# Forecast for next 30 periods (days/weeks/months)
future = model.make_future_dataframe(periods=30, freq='D' if frequency == "Daily" else 'W' if frequency == "Weekly" else 'M')
forecast = model.predict(future)

# Plot Forecast
fig1 = model.plot(forecast)
st.subheader("📈 Forecast Chart")
st.pyplot(fig1)

# Forecast Components
st.subheader("🧩 Forecast Components")
fig2 = model.plot_components(forecast)
st.pyplot(fig2)

# Raw forecast data
with st.expander("🔍 View Raw Forecast Data"):
    st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10))

# Footer
st.markdown("---")
st.markdown("📊 Created by **Dhanashri** | Enhanced Forecast with Prophet")
