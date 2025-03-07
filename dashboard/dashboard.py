import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Muat dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/day.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# Judul Dashboard
st.title("Bike Sharing Dataset Dashboard")

# Sidebar untuk Filter
st.sidebar.header("Filter Data")

# Filter berdasarkan musim (ubah nilai musim menjadi nama)
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
df['season_name'] = df['season'].map(season_mapping)
season_filter = st.sidebar.multiselect("Pilih Musim", options=df["season_name"].unique(), default=df["season_name"].unique())
filtered_df = df[df["season_name"].isin(season_filter)]

# Filter berdasarkan tahun
year_mapping = {0: 2011, 1: 2012}
filtered_df['year_name'] = filtered_df['yr'].map(year_mapping)
year_filter = st.sidebar.multiselect("Pilih Tahun", options=filtered_df["year_name"].unique(), default=filtered_df["year_name"].unique())
filtered_df = filtered_df[filtered_df["year_name"].isin(year_filter)]

# Visualisasi 1: Jumlah Peminjaman Sepeda per Hari
st.subheader("Jumlah Peminjaman Sepeda per Hari")
fig_daily_rentals, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_df['dteday'], filtered_df['cnt'])
ax.set_title("Jumlah Peminjaman Sepeda Harian")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig_daily_rentals)

# Visualisasi 2: Jumlah Peminjaman Sepeda berdasarkan Musim
st.subheader("Jumlah Peminjaman Sepeda berdasarkan Musim")
fig_season_rentals, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x='season_name', y='cnt', data=filtered_df, ax=ax)
ax.set_title("Distribusi Peminjaman Sepeda per Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig_season_rentals)

# Visualisasi 3: Korelasi Antara Suhu dan Jumlah Peminjaman
st.subheader("Korelasi Antara Suhu dan Jumlah Peminjaman")
fig_temp_rentals, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x='temp', y='cnt', data=filtered_df, ax=ax)
ax.set_title("Korelasi Suhu vs. Jumlah Peminjaman")
ax.set_xlabel("Suhu")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig_temp_rentals)

# Visualisasi 4: Distribusi Peminjaman Sepeda per Hari Kerja dan Hari Libur
st.subheader("Distribusi Peminjaman Sepeda per Hari Kerja dan Hari Libur")
fig_workingday_rentals, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='workingday', y='cnt', hue='holiday', data=filtered_df, ax=ax)
ax.set_title("Peminjaman Sepeda per Hari Kerja/Libur")
ax.set_xlabel("Hari Kerja (0: Tidak, 1: Ya)")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig_workingday_rentals)

# Tampilkan Data Mentah
if st.checkbox("Tampilkan Data Mentah"):
    st.subheader("Data Mentah")
    st.dataframe(filtered_df)