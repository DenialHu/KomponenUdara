import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Excel Data Viewer", layout="wide")

# Title
st.title("Simulasi Komponen Udara menggunakan Distribusi Probabilitas")

# Create the data from your Excel sheet
data = {
    'Day': list(range(1, 31)),
    'Zi': [5, 4, 54, 94, 126, 50, 40, 32, 51, 117, 119, 19, 66, 2, 27, 47, 63, 25, 20, 16, 89, 122, 123, 73, 83, 1, 77, 87, 95, 76],
    'Ui': [0.04, 0.03, 0.43, 0.74, 0.99, 0.39, 0.31, 0.25, 0.40, 0.92, 0.94, 0.15, 0.52, 0.02, 0.21, 0.37, 0.50, 0.20, 0.16, 0.13, 0.70, 0.96, 0.97, 0.57, 0.66, 0.01, 0.61, 0.69, 0.75, 0.60],
    'ln(Ui)': [-3.23, -3.46, -0.86, -0.30, -0.01, -0.93, -1.16, -1.38, -0.91, -0.08, -0.07, -1.90, -0.65, -4.15, -1.55, -0.99, -0.70, -1.63, -1.85, -2.07, -0.36, -0.04, -0.03, -0.55, -0.35, -4.84, -0.50, -0.38, -0.29, -0.51],
    'SO2': [115.44, 123.41, 30.52, 10.74, 0.28, 33.27, 41.23, 49.19, 32.56, 2.93, 2.32, 67.80, 23.36, 148.14, 55.26, 35.48, 25.02, 58.00, 65.97, 73.93, 12.69, 1.43, 1.14, 19.76, 48.10, 172.88, 17.86, 13.50, 10.36, 18.32],
    'PM2,5': [293.59, 313.85, 77.62, 27.31, 0.72, 84.61, 104.86, 125.11, 82.81, 7.44, 5.91, 172.43, 59.41, 376.76, 140.53, 90.22, 63.63, 147.52, 167.77, 188.02, 32.27, 3.65, 2.90, 50.26, 122.32, 439.67, 45.42, 34.33, 26.35, 46.60],
    '-ln(Ui)': [3.23, 3.46, 0.86, 0.30, 0.01, 0.93, 1.16, 1.38, 0.91, 0.08, 0.07, 1.90, 0.65, 4.15, 1.55, 0.99, 0.70, 1.63, 1.85, 2.07, 0.36, 0.04, 0.03, 0.55, 0.35, 4.84, 0.50, 0.38, 0.29, 0.51],
    'NO2': [118.35, 121.77, 67.03, 42.89, 9.06, 69.54, 76.22, 82.20, 68.91, 24.61, 22.29, 94.27, 59.79, 131.66, 86.38, 71.48, 61.57, 88.19, 93.18, 97.83, 46.06, 18.14, 16.46, 55.67, 81.41, 140.64, 53.31, 47.30, 42.24, 53.90],
    'PM10': [273.52, 284.15, 127.89, 70.40, 8.80, 134.34, 151.87, 168.00, 132.71, 33.50, 29.35, 201.79, 109.77, 315.41, 179.53, 139.37, 114.16, 184.58, 198.66, 212.05, 77.45, 22.28, 19.56, 99.76, 163.84, 344.51, 94.15, 80.24, 68.98, 95.55],
    'Rasio SO2/NO2': [0.975, 1.013, 0.455, 0.250, 0.031, 0.478, 0.541, 0.599, 0.473, 0.119, 0.104, 0.719, 0.391, 1.125, 0.640, 0.496, 0.406, 0.658, 0.708, 0.756, 0.275, 0.079, 0.069, 0.355, 0.591, 1.229, 0.335, 0.285, 0.245, 0.340],
    'Rasio PM2,5/PM10': [1.07, 1.10, 0.61, 0.39, 0.08, 0.63, 0.69, 0.74, 0.62, 0.22, 0.20, 0.85, 0.54, 1.19, 0.78, 0.65, 0.56, 0.80, 0.84, 0.89, 0.42, 0.16, 0.15, 0.50, 0.74, 1.28, 0.48, 0.43, 0.38, 0.49]
}

tab1, tab2 = st.tabs(['Tabel Data', 'Diagram Histogram'])

with tab1:
    # Create DataFrame
    df = pd.DataFrame(data)

    # Display the data
    st.subheader("Data Overview")

    # Display the dataframe
    st.dataframe(df, use_container_width=True)

    # Display basic statistics
    st.subheader("Basic Statistics")
    st.dataframe(df.describe(), use_container_width=True)

    # Option to download the data
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='TestMosi.csv',
        mime='text/csv',
    )

with tab2:
    # Create DataFrame for tab2
    df = pd.DataFrame(data)
    
    st.subheader("Data Histogram")
    
    # Selectbox to choose which variable to plot
    variables = ['Zi', 'Ui', 'ln(Ui)', 'SO2', 'PM2,5', '-ln(Ui)', 'NO2', 'PM10', 'Rasio SO2/NO2', 'Rasio PM2,5/PM10']
    selected_var = st.selectbox("Pilih variabel untuk histogram:", variables)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create histogram using matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(df[selected_var], bins=10, alpha=0.7, color='skyblue', edgecolor='black')
        ax.set_title(f'Histogram of {selected_var}')
        ax.set_xlabel(selected_var)
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        # Create histogram using Streamlit's built-in chart
        st.subheader(f"Distribution of {selected_var}")
        st.bar_chart(pd.Series(df[selected_var]).value_counts().sort_index())
    
    # Show multiple histograms at once
    st.subheader("All Variables Histograms")
    
    # Create a grid of histograms for all numeric variables
    numeric_vars = ['Zi', 'Ui', 'SO2', 'PM2,5', 'NO2', 'PM10', 'Rasio SO2/NO2', 'Rasio PM2,5/PM10']
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 10))
    axes = axes.flatten()
    
    for i, var in enumerate(numeric_vars):
        axes[i].hist(df[var], bins=8, alpha=0.7, color='lightcoral', edgecolor='black')
        axes[i].set_title(f'{var}')
        axes[i].set_xlabel(var)
        axes[i].set_ylabel('Frequency')
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Summary statistics for selected variable
    st.subheader(f"Summary Statistics for {selected_var}")
    stats_df = pd.DataFrame({
        'Statistic': ['Mean', 'Median', 'Std Dev', 'Min', 'Max'],
        'Value': [
            df[selected_var].mean(),
            df[selected_var].median(),
            df[selected_var].std(),
            df[selected_var].min(),
            df[selected_var].max()
        ]
    })
    st.dataframe(stats_df, use_container_width=True)