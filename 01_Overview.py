import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Customer Purchase Behavior Dashboard", layout="wide")

# Title
st.title("🛍️ Customer Purchase Behavior Analysis")
st.markdown("EDA Dashboard based on [Kaggle E-commerce Dataset](https://www.kaggle.com/datasets/carrie1/ecommerce-data)")

# Load data
@st.cache_data  # Changed from st.cache_data to st.cache for compatibility
def load_data():
    df = pd.read_csv("../Data/data.csv", encoding='ISO-8859-1')
    df.dropna(inplace=True)
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['Day'] = df['InvoiceDate'].dt.day
    df['Hour'] = df['InvoiceDate'].dt.hour
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("📌 Filter Options")
selected_country = st.sidebar.selectbox("Select Country", options=["All"] + sorted(df['Country'].unique().tolist()))

if selected_country != "All":
    df = df[df['Country'] == selected_country]

# Metric Cards
st.subheader("📈 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"£{df['TotalPrice'].sum():,.2f}")
col2.metric("Total Transactions", df['InvoiceNo'].nunique())
col3.metric("Unique Customers", df['CustomerID'].nunique())

# Top Products
st.subheader("🏆 Top 10 Sold Products")
top_products = df['Description'].value_counts().head(10)
fig1, ax1 = plt.subplots()
sns.barplot(x=top_products.values, y=top_products.index, palette="viridis", ax=ax1)
ax1.set_xlabel("Count")
st.pyplot(fig1)

# Revenue by Country
st.subheader("🌍 Revenue by Country (Top 10)")
top_countries = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_countries.values, y=top_countries.index, palette="magma", ax=ax2)
ax2.set_xlabel("Revenue (£)")
st.pyplot(fig2)

# Hourly Sales
st.subheader("🕒 Sales by Hour")
hourly_sales = df.groupby('Hour')['TotalPrice'].sum()
fig3, ax3 = plt.subplots()
sns.lineplot(x=hourly_sales.index, y=hourly_sales.values, marker='o', ax=ax3)
ax3.set_ylabel("Total Sales")
ax3.set_xlabel("Hour of Day")
st.pyplot(fig3)

# Correlation Heatmap
st.subheader("📌 Correlation Heatmap")
fig4, ax4 = plt.subplots()
sns.heatmap(df[['Quantity', 'UnitPrice', 'TotalPrice']].corr(), annot=True, cmap='coolwarm', ax=ax4)
st.pyplot(fig4)

# Footer
st.markdown("---")
st.markdown("📊 Created by **Dhanashri** | Streamlit Dashboard for EDA 📈")
