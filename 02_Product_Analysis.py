import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Use st.cache instead of st.cache_data for compatibility
@st.cache_data
def load_data():
    df = pd.read_csv("../Data/data.csv", encoding='ISO-8859-1')
    df.dropna(inplace=True)
    # Remove cancelled transactions (InvoiceNo starting with 'C')
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    # Filter for positive quantity and price
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    # Calculate total price per row
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    # Convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    # Extract useful time features
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['Day'] = df['InvoiceDate'].dt.day
    df['Hour'] = df['InvoiceDate'].dt.hour
    return df

df = load_data()

st.title("🏷️ Product Analysis")

# Top 10 sold products by quantity
st.subheader("Top 10 Sold Products")
top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)

fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.barplot(x=top_products.values, y=top_products.index, palette='viridis', ax=ax1)
ax1.set_xlabel("Quantity Sold")
ax1.set_ylabel("Product")
st.pyplot(fig1)

# Top 10 revenue-generating products
st.subheader("Top 10 Revenue Generating Products")
top_revenue = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)

fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.barplot(x=top_revenue.values, y=top_revenue.index, palette='rocket', ax=ax2)
ax2.set_xlabel("Revenue (£)")
ax2.set_ylabel("Product")
st.pyplot(fig2)

# Average unit price per product for top 10 products by revenue
st.subheader("Average Unit Price of Top 10 Revenue Products")
top_products_for_avg_price = top_revenue.index.tolist()
avg_unit_price = df[df['Description'].isin(top_products_for_avg_price)].groupby('Description')['UnitPrice'].mean().sort_values(ascending=False)

fig3, ax3 = plt.subplots(figsize=(8, 6))
sns.barplot(x=avg_unit_price.values, y=avg_unit_price.index, palette='coolwarm', ax=ax3)
ax3.set_xlabel("Average Unit Price (£)")
ax3.set_ylabel("Product")
st.pyplot(fig3)

# Products with highest return rates (where quantity < 0 indicates returns; filtered out earlier but just in case)
# Optional: If returns are filtered out, you can remove this section or adapt it.

# Footer
st.markdown("---")
st.markdown("📊 Created by **Dhanashri** | Product Analysis Page")
