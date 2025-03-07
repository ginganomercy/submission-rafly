import streamlit as st
import pandas as pd

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
df['season_name'] = df['season'].map(season_mapping)  # Tambahkan kolom nama musim
season_filter = st.sidebar.multiselect("Pilih Musim", options=df["season_name"].unique(), default=df["season_name"].unique())
filtered_df = df[df["season_name"].isin(season_filter)]

# Filter berdasarkan tahun
year_mapping = {0: 2011, 1: 2012}
filtered_df['year_name'] = filtered_df['yr'].map(year_mapping) # Tambahkan kolom nama tahun
year_filter = st.sidebar.multiselect("Pilih Tahun", options=filtered_df["year_name"].unique(), default=filtered_df["year_name"].unique())
filtered_df = filtered_df[filtered_df["year_name"].isin(year_filter)]

# Visualisasi 1: Jumlah Peminjaman Sepeda per Hari
st.subheader("Jumlah Peminjaman Sepeda per Hari")
fig_daily_rentals = px.line(filtered_df, x="dteday", y="cnt", title="Jumlah Peminjaman Sepeda Harian")
st.plotly_chart(fig_daily_rentals)

# Visualisasi 2: Jumlah Peminjaman Sepeda berdasarkan Musim
st.subheader("Jumlah Peminjaman Sepeda berdasarkan Musim")
fig_season_rentals = px.box(filtered_df, x="season_name", y="cnt", title="Distribusi Peminjaman Sepeda per Musim")
st.plotly_chart(fig_season_rentals)

# Visualisasi 3: Korelasi Antara Suhu dan Jumlah Peminjaman
st.subheader("Korelasi Antara Suhu dan Jumlah Peminjaman")
fig_temp_rentals = px.scatter(filtered_df, x="temp", y="cnt", title="Korelasi Suhu vs. Jumlah Peminjaman")
st.plotly_chart(fig_temp_rentals)

# Visualisasi 4: Distribusi Peminjaman Sepeda per Hari Kerja dan Hari Libur
st.subheader("Distribusi Peminjaman Sepeda per Hari Kerja dan Hari Libur")
fig_workingday_rentals = px.bar(filtered_df, x="workingday", y="cnt", color="holiday", title="Peminjaman Sepeda per Hari Kerja/Libur")
st.plotly_chart(fig_workingday_rentals)

# Tampilkan Data Mentah
if st.checkbox("Tampilkan Data Mentah"):
    st.subheader("Data Mentah")
    st.dataframe(filtered_df)