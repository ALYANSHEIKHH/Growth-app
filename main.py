import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import time

# Page Configuration
st.set_page_config(page_title="Advanced Data Dashboard", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        * { font-family: 'Poppins', sans-serif; }

        .stButton > button {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🚀 Advanced Data Dashboard")

# File Upload
uploaded_file = st.file_uploader("📂 Choose a CSV file", type="csv")

if uploaded_file is not None:
    with st.spinner("Loading data..."):
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        df = pd.read_csv(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Data Preview")
        st.write(df.head())
    
    with col2:
        st.subheader("📈 Data Summary")
        st.write(df.describe())

    # Key Metrics
    st.subheader("📌 Key Metrics")
    col3, col4, col5 = st.columns(3)
    col3.metric("Total Rows", len(df))
    col4.metric("Total Columns", len(df.columns))
    col5.metric("Missing Values", df.isnull().sum().sum())

    # Data Filtering
    st.subheader("🔍 Filter Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Select value", unique_values)
    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    # Data Visualization
    st.subheader("📌 Plot Data")
    x_column = st.selectbox("Select x-axis column", columns)
    y_column = st.selectbox("Select y-axis column", columns)

    if not filtered_df.empty and pd.api.types.is_numeric_dtype(filtered_df[y_column]):
        col6, col7, col8 = st.columns(3)
        
        with col6:
            if st.button("📊 Generate Line Chart"):
                st.line_chart(filtered_df.set_index(x_column)[y_column])
        
        with col7:
            if st.button("📊 Generate Pie Chart"):
                fig, ax = plt.subplots()
                filtered_df[y_column].value_counts().plot.pie(autopct="%1.1f%%", startangle=90, cmap='coolwarm', ax=ax)
                st.pyplot(fig)
        
        with col8:
            if st.button("📊 Generate Bar Chart"):
                fig, ax = plt.subplots()
                sns.barplot(x=filtered_df[x_column], y=filtered_df[y_column], ax=ax, palette="coolwarm")
                plt.xticks(rotation=45)
                st.pyplot(fig)
    else:
        st.error("⚠️ Selected Y-axis column must contain numeric values!")

    # Download Filtered Data
    st.subheader("💾 Download Filtered Data")
    def convert_df(df):
        output = BytesIO()
        df.to_csv(output, index=False)
        return output.getvalue()

    if st.button("📥 Download CSV"):
        st.download_button(
            label="📥 Download CSV",
            data=convert_df(filtered_df),
            file_name="filtered_data.csv",
            mime="text/csv",
        )
else:
    st.write("⚡ Waiting for file upload...")
