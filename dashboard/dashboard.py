import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Load Data
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

# Preprocessing
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
day_df['day_name'] = day_df['dteday'].dt.day_name()

# Filter date range
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚴‍♂️ Bike Sharing Data Dashboard")

# Sidebar
with st.sidebar:
    st.image("BIKE RENT.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Tren Penyewaan", "Musim & Cuaca", "Faktor Lingkungan", "Perbandingan Penyewa"])

with tab1:
    st.subheader("Tren Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=day_df['dteday'], y=day_df['cnt'], ax=ax)
    ax.set_title("Tren Penyewaan Sepeda Harian")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    st.write("***Insight:*** Penyewaan sepeda menunjukkan tren peningkatan dari tahun ke tahun dengan pola fluktuatif harian dan bulanan yang konsisten.")

    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_avg = day_df.groupby('mnth')['cnt'].mean().reset_index()
    sns.lineplot(x=monthly_avg['mnth'], y=monthly_avg['cnt'], ax=ax)
    ax.set_title("Tren Penyewaan Sepeda per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    st.write("Insight: Puncak penggunaan terjadi pada bulan-bulan musim panas dan awal musim gugur, sementara musim dingin menunjukkan penurunan signifikan.")

with tab2:
    st.subheader("Penyewaan Berdasarkan Musim & Cuaca")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='season', y='cnt', data=day_df, ax=ax)
    ax.set_title("Penyewaan Sepeda Berdasarkan Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    st.write("Insight: Penyewaan tertinggi terjadi pada musim gugur, diikuti oleh musim panas. Musim dingin memiliki jumlah penyewaan terendah.")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='weathersit', y='cnt', data=day_df, ax=ax)
    ax.set_title("Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    st.write("Insight: Cuaca cerah mendorong penyewaan sepeda tertinggi, sementara hujan dan kondisi buruk menurunkan jumlah penyewaan secara signifikan.")

with tab3:
    st.subheader("Pengaruh Faktor Lingkungan")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='temp', y='cnt', data=day_df, ax=ax)
    ax.set_title("Pengaruh Suhu terhadap Penyewaan Sepeda")
    ax.set_xlabel("Suhu (Normalized)")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    st.write("Insight: Penyewaan sepeda meningkat pada suhu yang nyaman dan menurun pada suhu ekstrem.")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='hum', y='cnt', data=day_df, ax=ax)
    ax.set_title("Pengaruh Kelembaban terhadap Penyewaan Sepeda")
    ax.set_xlabel("Kelembaban (Normalized)")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    st.write("Insight: Kelembaban tinggi memiliki korelasi negatif dengan jumlah penyewaan sepeda.")

with tab4:
    st.subheader("Perbandingan Penyewa")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='dteday', y='casual', data=day_df, label='Casual', ax=ax)
    sns.lineplot(x='dteday', y='registered', data=day_df, label='Registered', ax=ax)
    ax.set_title("Perbandingan Penyewa Casual dan Registered")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewa")
    ax.legend()
    st.pyplot(fig)
    st.write("Insight: Penyewa terdaftar jauh lebih dominan dibandingkan penyewa kasual. Penyewa kasual cenderung lebih aktif pada akhir pekan dan musim panas.")

if __name__ == "__main__":
    st.write("@BIKE RENT 2025, All Rights Reserved")
