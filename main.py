import streamlit as st

st.set_page_config(page_title="🛍️ ShopSmart", layout="wide")

dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=False)

light_css = """
    /* Gradient background for main content */
    .css-1d391kg {
        background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
        min-height: 100vh;
        padding: 3rem 2rem 5rem 2rem;
    }
    .main-title {
        font-size: 56px;
        font-weight: 900;
        color: #0D1B2A;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-bottom: 0.1rem;
        letter-spacing: 0.04em;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.1);
    }
    /* Subtitle */
    .subtitle {
        max-width: 720px;
        margin: 2rem auto 3rem auto;
        background-color: #F0F4F8;
        padding: 30px 40px;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        font-size: 20px;
        line-height: 1.7;
        color: #243B55;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        user-select: none;
        text-align: center;
        white-space: pre-line;
    }
    .footer {
        text-align: center;
        font-size: 16px;
        color: #6B7A8F;
        margin-top: 4rem;
        user-select: none;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    @media (max-width: 768px) {
        .main-title {
            font-size: 40px;
        }
        .subtitle {
            padding: 25px 20px;
            font-size: 18px;
        }
    }
"""

dark_css = """
    /* Dark background */
    .css-1d391kg {
        background: #121212;
        min-height: 100vh;
        padding: 3rem 2rem 5rem 2rem;
    }
    .main-title {
        font-size: 56px;
        font-weight: 900;
        color: #E0E0E0;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-bottom: 0.1rem;
        letter-spacing: 0.04em;
        text-shadow: 1px 1px 4px rgba(255,255,255,0.1);
    }
    .subtitle {
        max-width: 720px;
        margin: 2rem auto 3rem auto;
        background-color: #1E1E1E;
        padding: 30px 40px;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(255,255,255,0.1);
        font-size: 20px;
        line-height: 1.7;
        color: #E0E0E0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        user-select: none;
        text-align: center;
        white-space: pre-line;
    }
    .footer {
        text-align: center;
        font-size: 16px;
        color: #AAAAAA;
        margin-top: 4rem;
        user-select: none;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    @media (max-width: 768px) {
        .main-title {
            font-size: 40px;
        }
        .subtitle {
            padding: 25px 20px;
            font-size: 18px;
        }
    }
"""

st.markdown(f"<style>{dark_css if dark_mode else light_css}</style>", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-title">🛍️ ShopSmart</div>', unsafe_allow_html=True)

# New subtitle content replacing the old welcome box list
st.markdown("""
<div class="subtitle">
    Welcome! Explore your data effortlessly by navigating the sidebar.<br>
    Dive into key insights about products, customers, sales forecasts, and geography.
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">📊 Created by <strong>Dhanashri</strong> | Streamlit Dashboard for EDA 📈</div>', unsafe_allow_html=True)
