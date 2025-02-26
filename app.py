import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from io import BytesIO

# Streamlit Page Config
st.set_page_config(page_title="Data Profiler & Explorer", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
        /* Page Background */
        .stApp {
            background-color: #1E1E1E;
            color: white;
        }

        /* Title */
        .stTitle {
            color: #00BFFF;
            text-align: center;
            font-size: 32px;
        }

        /* Subheader */
        .stSubheader {
            color: #FFD700;
            font-size: 24px;
        }

        /* Sidebar */
        .css-1d391kg {
            background-color: #242424 !important;
        }

        /* Buttons */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 10px 24px;
        }

        .stButton>button:hover {
            background-color: #45a049;
        }

        /* File uploader */
        .stFileUploader {
            background-color: #333;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def data_profiler():
    st.title("Data Profiler & Explorer")
    st.markdown("🚀 Upload your dataset to **analyze, visualize, and clean** your data effortlessly!")

    uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        # Dataset Overview
        st.subheader("📌 Dataset Overview")
        st.write(f"**Rows:** `{df.shape[0]}` | **Columns:** `{df.shape[1]}`")
        st.dataframe(df.head(10))

        # Sidebar
        st.sidebar.header("🎛 Data Cleaning & Processing")
        remove_duplicates = st.sidebar.checkbox("Remove Duplicates")
        fill_missing = st.sidebar.checkbox("Fill Missing Values")
        drop_columns = st.sidebar.multiselect("Drop Columns", df.columns.tolist())

        if remove_duplicates:
            df = df.drop_duplicates()
            st.sidebar.success("✅ Duplicates removed")

        if fill_missing:
            fill_value = st.sidebar.text_input("Enter value to fill missing data", "N/A")
            df.fillna(fill_value, inplace=True)
            st.sidebar.success("✅ Missing values filled")

        if drop_columns:
            df.drop(columns=drop_columns, inplace=True)
            st.sidebar.success(f"✅ Dropped columns: `{', '.join(drop_columns)}`")

        # Data Insights
        st.subheader("📊 Data Insights")
        st.write("🔍 **Missing Values & Unique Counts**")
        col_info = pd.DataFrame({
            "Missing Values": df.isnull().sum(),
            "Unique Values": df.nunique(),
            "Data Type": df.dtypes
        })
        st.dataframe(col_info.style.set_properties(**{'background-color': '#333', 'color': 'white'}))

        # Visualizations Section
        st.subheader("📊 Data Visualizations")

        # 🎨 Histogram with Color Palette
        if st.checkbox("📉 Show Histogram"):
            num_columns = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

            if num_columns:
                selected_col = st.selectbox("📊 Select a numeric column", num_columns)
                if selected_col:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    sns.histplot(df[selected_col], kde=True, bins=20, ax=ax, color="dodgerblue")
                    ax.set_title(f"Histogram of {selected_col}", fontsize=14, color="white")
                    ax.set_facecolor("#1E1E1E")  # Background color
                    st.pyplot(fig)
            else:
                st.warning("⚠️ No numeric columns available for histogram.")

        # 🎨 Correlation Heatmap with Viridis Colormap
        if st.checkbox("🔥 Show Correlation Heatmap"):
            numeric_df = df.select_dtypes(include=["int64", "float64"])

            if not numeric_df.empty:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
                ax.set_title("🔥 Correlation Heatmap", fontsize=16, color="white")
                ax.set_facecolor("#1E1E1E")
                st.pyplot(fig)
            else:
                st.warning("⚠️ No numeric columns available for correlation heatmap.")

        # 🎨 Scatter Plot
        if st.checkbox("📌 Show Scatter Plot"):
            numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
            if len(numeric_cols) >= 2:
                col1 = st.selectbox("Choose X-axis", numeric_cols, key="x_axis")
                col2 = st.selectbox("Choose Y-axis", numeric_cols, key="y_axis")

                fig, ax = plt.subplots(figsize=(8, 4))
                sns.scatterplot(x=df[col1], y=df[col2], color="yellow", edgecolor="white", s=100)
                ax.set_title(f"Scatter Plot: {col1} vs {col2}", fontsize=14, color="white")
                ax.set_facecolor("#1E1E1E")
                st.pyplot(fig)
            else:
                st.warning("⚠️ Need at least 2 numeric columns for scatter plot.")

        # 🎨 Download Cleaned Data Button
        cleaned_data = BytesIO()
        df.to_csv(cleaned_data, index=False)
        cleaned_data.seek(0)
        st.download_button("⬇️ Download Cleaned Data", cleaned_data, "cleaned_data.csv", "text/csv")

data_profiler()
