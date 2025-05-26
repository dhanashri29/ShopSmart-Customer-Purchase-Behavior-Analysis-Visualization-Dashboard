import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="Customer Analysis", layout="wide")
st.title("👥 Customer Analysis")
st.markdown("Explore customer behavior using **RFM Analysis** (Recency, Frequency, Monetary).")

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

# Calculate RFM metrics
st.markdown("### 🧮 Calculating RFM Scores")
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'TotalPrice': 'sum'
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# Normalize and score
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4]).astype(int)
rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

# Show data
st.dataframe(rfm.head())

# Visualizations
st.markdown("### 📊 RFM Distribution")

col1, col2, col3 = st.columns(3)

with col1:
    fig1, ax1 = plt.subplots()
    sns.histplot(rfm['Recency'], kde=True, bins=20, ax=ax1)
    ax1.set_title("Recency Distribution")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    sns.histplot(rfm['Frequency'], kde=True, bins=20, ax=ax2)
    ax2.set_title("Frequency Distribution")
    st.pyplot(fig2)

with col3:
    fig3, ax3 = plt.subplots()
    sns.histplot(rfm['Monetary'], kde=True, bins=20, ax=ax3)
    ax3.set_title("Monetary Distribution")
    st.pyplot(fig3)

# Customer Segments - Fixed Bin Edges and Labels
st.markdown("### 🧩 Segment Customers Based on RFM Score")

# Ensure unique bin edges and labels
rfm['Segment'] = pd.cut(rfm['RFM_Score'],
                        bins=[1, 6, 9, 10, 12],
                        labels=['Low Value', 'Mid Value', 'High Value', 'Best Customers'],
                        include_lowest=True)

segment_counts = rfm['Segment'].value_counts().sort_index()
fig4, ax4 = plt.subplots()
segment_counts.plot(kind='bar', color='skyblue', ax=ax4)
ax4.set_ylabel("Number of Customers")
ax4.set_xlabel("Customer Segment")
ax4.set_title("Customer Segments by RFM Score")
st.pyplot(fig4)

# Footer
st.markdown("---")
st.markdown("🛍️ Created by **Dhanashri** | Customer Segmentation with RFM Analysis")
