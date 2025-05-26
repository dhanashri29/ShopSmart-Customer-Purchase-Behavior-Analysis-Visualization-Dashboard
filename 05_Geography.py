import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Page config
st.set_page_config(page_title="🌍 Geography Analysis", layout="wide")

# Load Data with cache_data decorator
@st.cache_data
def load_data():
    df = pd.read_csv("../Data/data.csv", encoding='ISO-8859-1')
    df.dropna(inplace=True)
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]  # Remove canceled orders
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    return df

df = load_data()

# Sidebar filter for Country selection
st.sidebar.header("🌎 Filter by Country")
selected_country = st.sidebar.selectbox("Select Country", options=["All"] + sorted(df['Country'].unique().tolist()))

# Filter dataset by selected country if not 'All'
if selected_country != "All":
    df = df[df['Country'] == selected_country]

st.title("🌍 Geography Analysis of Customer Purchases")

# Total Revenue by Country
st.subheader("💰 Total Revenue by Country")
revenue_by_country = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.barh(revenue_by_country.index, revenue_by_country.values, color='#007acc')  # changed to bright blue
ax1.invert_yaxis()
ax1.set_xlabel("Revenue (£)")
ax1.set_title("Top 10 Countries by Revenue")
st.pyplot(fig1)

# Interactive Map: Revenue by Country (Top 20)
st.subheader("🗺️ Revenue Map by Country (Top 20)")
top_countries = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(20).reset_index()

# Use Plotly for interactive choropleth map with different color scale
fig2 = px.choropleth(
    top_countries,
    locations='Country',
    locationmode='country names',
    color='TotalPrice',
    color_continuous_scale='plasma',  # changed from 'Viridis' to 'plasma'
    labels={'TotalPrice': 'Revenue (£)'},
    title="Top 20 Countries by Revenue"
)
st.plotly_chart(fig2, use_container_width=True)

# Country-wise Quantity Sold
st.subheader("📦 Quantity Sold by Country")
quantity_by_country = df.groupby('Country')['Quantity'].sum().sort_values(ascending=False).head(10)

fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.barh(quantity_by_country.index, quantity_by_country.values, color='#ff6f61')  # coral-like warm red
ax3.invert_yaxis()
ax3.set_xlabel("Quantity Sold")
ax3.set_title("Top 10 Countries by Quantity Sold")
st.pyplot(fig3)

# Footer
st.markdown("---")
st.markdown("📊 Created by **Dhanashri** | Geography Analysis Page")
