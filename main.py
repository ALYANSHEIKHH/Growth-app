import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import time

# Page Configuration
st.set_page_config(page_title="Advanced Data Dashboard", layout="wide")

# Custom CSS for styling, animations, and hover effects
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        * { font-family: 'Poppins', sans-serif; }
        
        /* Light Mode */
        .light-mode {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            color: #333;
        }
        .light-mode .stButton > button {
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
        .light-mode .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        
        /* Dark Blue Mode */
        .dark-blue-mode {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
        }
        .dark-blue-mode .stButton > button {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .dark-blue-mode .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        
        /* Cards */
        .card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .dark-blue-mode .card {
            background: rgba(30, 30, 30, 0.9);
            color: white;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        
        /* Progress Bar */
        .stProgress > div > div {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            border-radius: 12px;
        }
        
        /* Custom Toggle Switch */
        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 60px;
            height: 34px;
        }
        .toggle-switch input { opacity: 0; width: 0; height: 0; }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            transition: 0.4s;
            border-radius: 34px;
        }
        .slider:before {
            position: absolute;
            content: "🌙";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background: white;
            transition: 0.4s;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
        }
        input:checked + .slider { background: linear-gradient(135deg, #1e3c72, #2a5298); }
        input:checked + .slider:before { transform: translateX(26px); content: "☀️"; }
    </style>
""", unsafe_allow_html=True)

# JavaScript for Theme Toggle
st.markdown("""
    <script>
        function toggleTheme() {
            const body = document.body;
            if (body.classList.contains('light-mode')) {
                body.classList.remove('light-mode');
                body.classList.add('dark-blue-mode');
            } else {
                body.classList.remove('dark-blue-mode');
                body.classList.add('light-mode');
            }
        }
    </script>
""", unsafe_allow_html=True)

# Theme Toggle Button


# Title with an emoji and animation
st.title("🚀 Advanced Data Dashboard")

# File Upload with progress bar
uploaded_file = st.file_uploader("📂 Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Simulate loading with a progress bar
    with st.spinner("Loading data..."):
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)  # Simulate loading time
            progress_bar.progress(percent_complete + 1)
        df = pd.read_csv(uploaded_file)

    # Create two columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Data Preview")
        st.write(df.head())

    with col2:
        st.subheader("📈 Data Summary")
        st.write(df.describe())

    # Interactive Data Cards
    st.subheader("📌 Key Metrics")
    col3, col4, col5 = st.columns(3)
    with col3:
        st.markdown('<div class="card"><h4>Total Rows</h4><h2>{}</h2></div>'.format(len(df)), unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="card"><h4>Total Columns</h4><h2>{}</h2></div>'.format(len(df.columns)), unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="card"><h4>Missing Values</h4><h2>{}</h2></div>'.format(df.isnull().sum().sum()), unsafe_allow_html=True)

    # Data Filtering
    st.subheader("🔍 Filter Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", columns, key="filter_column")
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Select value", unique_values, key="filter_value")

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    # Data Visualization
    st.subheader("📌 Plot Data")
    x_column = st.selectbox("Select x-axis column", columns, key="x_column")
    y_column = st.selectbox("Select y-axis column", columns, key="y_column")

    # Ensure selected columns are valid
    if not filtered_df.empty and x_column in filtered_df.columns and y_column in filtered_df.columns:
        if pd.api.types.is_numeric_dtype(filtered_df[y_column]):
            col6, col7, col8 = st.columns(3)

            with col6:
                if st.button("📊 Generate Line Chart"):
                    with st.spinner("Generating Line Chart..."):
                        time.sleep(1)  # Simulate chart generation time
                        st.line_chart(filtered_df.set_index(x_column)[y_column])

            with col7:
                if st.button("📊 Generate Pie Chart"):
                    with st.spinner("Generating Pie Chart..."):
                        time.sleep(1)  # Simulate chart generation time
                        fig, ax = plt.subplots()
                        filtered_df[y_column].value_counts().plot.pie(
                            autopct="%1.1f%%", startangle=90, cmap='coolwarm', ax=ax
                        )
                        st.pyplot(fig)

            with col8:
                if st.button("📊 Generate Bar Chart"):
                    with st.spinner("Generating Bar Chart..."):
                        time.sleep(1)  # Simulate chart generation time
                        fig, ax = plt.subplots()
                        sns.barplot(x=filtered_df[x_column], y=filtered_df[y_column], ax=ax, palette="coolwarm")
                        plt.xticks(rotation=45)
                        st.pyplot(fig)

        else:
            st.error(f"⚠️ Selected Y-axis column '{y_column}' must contain numeric values!")

    else:
        st.error("⚠️ Invalid selection. Please choose valid columns.")

    # Download Filtered Data with animation
    st.subheader("💾 Download Filtered Data")

    def convert_df(df):
        output = BytesIO()
        df.to_csv(output, index=False)
        processed_data = output.getvalue()
        return processed_data

    if st.button("📥 Download CSV", key="download-button"):
        with st.spinner("Preparing download..."):
            time.sleep(1)  # Simulate download preparation time
            st.download_button(
                label="📥 Download CSV",
                data=convert_df(filtered_df),
                file_name="filtered_data.csv",
                mime="text/csv",
            )

else:
    st.write("⚡ Waiting for file upload...")