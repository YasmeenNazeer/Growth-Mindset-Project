"""import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

# Streamlit Page Configuration
st.set_page_config(page_title=" Data Profiler & Explorer", layout="wide")

# Custom Styling for Dark Mode UI
st.markdown(
    
    unsafe_allow_html=True
)

def data_profiler():
    st.title("📊 Data Profiler & Explorer")
    st.markdown("🚀 Upload your dataset to **analyze, visualize, and clean** your data effortlessly!")

    uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        # Dataset Overview
        st.subheader("📌 Dataset Overview")
        st.write(f"**Rows:** `{df.shape[0]}` | **Columns:** `{df.shape[1]}`")
        st.dataframe(df.head(10))

        # Sidebar - Data Cleaning Options
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

        # Visualizations
        st.subheader("📊 Data Visualizations")

        # Histogram
        if st.checkbox("📉 Show Histogram"):
            num_columns = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
            if num_columns:
                selected_col = st.selectbox("📊 Select a numeric column", num_columns)
                if selected_col:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    ax.hist(df[selected_col], bins=20, color="dodgerblue", edgecolor="white", alpha=0.8)
                    ax.set_title(f"Histogram of {selected_col}", fontsize=14, color="white")
                    ax.set_facecolor("#1E1E1E")
                    ax.spines["bottom"].set_color("white")
                    ax.spines["left"].set_color("white")
                    ax.xaxis.label.set_color("white")
                    ax.yaxis.label.set_color("white")
                    ax.tick_params(colors="white")
                    st.pyplot(fig)
            else:
                st.warning("⚠️ No numeric columns available for histogram.")

        # Correlation Heatmap
        if st.checkbox("🔥 Show Correlation Heatmap"):
            numeric_df = df.select_dtypes(include=["int64", "float64"])
            if not numeric_df.empty:
                fig, ax = plt.subplots(figsize=(8, 6))
                cax = ax.matshow(numeric_df.corr(), cmap="coolwarm")
                fig.colorbar(cax)
                ax.set_xticks(range(len(numeric_df.columns)))
                ax.set_yticks(range(len(numeric_df.columns)))
                ax.set_xticklabels(numeric_df.columns, rotation=90, color="white")
                ax.set_yticklabels(numeric_df.columns, color="white")
                ax.set_title("🔥 Correlation Heatmap", fontsize=16, color="white")
                st.pyplot(fig)
            else:
                st.warning("⚠️ No numeric columns available for correlation heatmap.")

        # Scatter Plot
        if st.checkbox("📌 Show Scatter Plot"):
            numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
            if len(numeric_cols) >= 2:
                col1 = st.selectbox("Choose X-axis", numeric_cols, key="x_axis")
                col2 = st.selectbox("Choose Y-axis", numeric_cols, key="y_axis")

                fig, ax = plt.subplots(figsize=(8, 4))
                ax.scatter(df[col1], df[col2], color="yellow", edgecolor="white", alpha=0.7)
                ax.set_title(f"Scatter Plot: {col1} vs {col2}", fontsize=14, color="white")
                ax.set_xlabel(col1, color="white")
                ax.set_ylabel(col2, color="white")
                ax.set_facecolor("#1E1E1E")
                ax.spines["bottom"].set_color("white")
                ax.spines["left"].set_color("white")
                ax.xaxis.label.set_color("white")
                ax.yaxis.label.set_color("white")
                ax.tick_params(colors="white")
                st.pyplot(fig)
            else:
                st.warning("⚠️ Need at least 2 numeric columns for scatter plot.")

        # Download Cleaned Data Button
        cleaned_data = BytesIO()
        df.to_csv(cleaned_data, index=False)
        cleaned_data.seek(0)
        st.download_button("⬇️ Download Cleaned Data", cleaned_data, "cleaned_data.csv", "text/csv")

data_profiler()

"""
import pandas as pd
import streamlit as st

# 🎨 Set Page Title
st.set_page_config(page_title="Data Dashboard", layout="wide")

# 🚀 App Title
st.title("📊 Simple Data Dashboard")

# 📂 File Uploader
uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 🕒 Convert 'Date' column to datetime if it exists
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 🔄 Remove spaces from column names
    df.columns = df.columns.str.replace(" ", "_")

    # 🎯 Display Dataset Overview
    st.subheader("🔍 Data Preview")
    st.write(df.head())

    # 📌 Data Summary
    st.subheader("📊 Data Summary")
    st.write(df.describe())

    # 🎛 Data Filtering
    st.subheader("🎚 Filter Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("📌 Select column to filter by", columns)

    if df[selected_column].dtype == object:
        unique_values = df[selected_column].dropna().unique()
        selected_value = st.selectbox("🎯 Select value", unique_values)
        filtered_df = df[df[selected_column] == selected_value]
    else:
        min_value, max_value = float(df[selected_column].min()), float(df[selected_column].max())
        selected_value = st.slider(f"🎯 Select range for {selected_column}", min_value, max_value, (min_value, max_value))
        filtered_df = df[(df[selected_column] >= selected_value[0]) & (df[selected_column] <= selected_value[1])]

    st.write(filtered_df)

    # 📈 Data Visualization
    st.subheader("📉 Plot Data")

    # 🔍 Ensure there are numeric columns for plotting
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    if numeric_columns:
        x_column = st.selectbox("📍 Select X-axis", df.columns.tolist())  # Allow date selection
        y_column = st.selectbox("📍 Select Y-axis (Numeric Only)", numeric_columns)

        if st.button("📊 Generate Plot"):
            if not filtered_df.empty:
                try:
                    st.line_chart(filtered_df.set_index(x_column)[y_column])
                except KeyError:
                    st.error("⚠️ Please select valid X and Y columns!")
            else:
                st.error("⚠️ Filtered data is empty! Adjust the filters.")
    else:
        st.warning("⚠️ No numeric columns available for plotting. Upload a valid dataset.")

else:
    st.write("📌 Upload a CSV file to begin analysis.")
