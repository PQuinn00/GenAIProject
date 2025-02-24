# Ensure required libraries are installed
import subprocess
import sys
import streamlit as st
import requests
import pandas as pd
import openai
from bs4 import BeautifulSoup

def install_lxml():
    try:
        import lxml
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "lxml"])
        import lxml
install_lxml()

# Set OpenAI API Key (Replace with your own key)
openai.api_key = "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"


# Function to scrape Nike's revenue data
def get_nike_revenue():
    url = "https://www.macrotrends.net/stocks/charts/NKE/nike/revenue"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    tables = soup.find_all("table")
    revenue_data = []
    
    for table in tables:
        try:
            df = pd.read_html(str(table), flavor="lxml")[0]
            if "Nike Quarterly Revenue" in df.to_string():
                revenue_data.append(df)
        except Exception as e:
            continue
    
    if revenue_data:
        revenue_df = revenue_data[0]
        revenue_df.columns = ["Date", "Revenue"]
        revenue_df.dropna(inplace=True)
        return revenue_df
    else:
        return pd.DataFrame()

# Function to generate AI-based sales predictions
def generate_sales_prediction(historical_data, target_month):
    prompt = f"/"/"/
    Based on the historical revenue trends of Nike, predict the revenue for {target_month}.
    
    Historical Data:
    {historical_data.to_string(index=False)}
    
    Provide an estimated revenue and explain the reasoning behind the prediction based on past trends.
    "/"/"/
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a financial analyst."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]
    
# Streamlit UI
st.title("👟 AI-Powered Nike Sales Prediction Tool")

# Fetch Nike's historical revenue data
nike_revenue = get_nike_revenue()

if not nike_revenue.empty:
    st.write("### Nike's Historical Revenue Data")
    st.dataframe(nike_revenue)
    
    target_month = st.text_input("Enter a month for prediction (e.g., March 2025):")
    
    if st.button("Predict Revenue") and target_month:
        prediction = generate_sales_prediction(nike_revenue, target_month)
        st.subheader("AI-Powered Sales Prediction:")
        st.write(prediction)
else:
    st.error("Could not retrieve Nike's revenue data. Please try again later.")
