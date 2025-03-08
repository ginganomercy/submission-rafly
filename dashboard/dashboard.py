import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data_path = 'dashboard/all_data.csv'
df = pd.read_csv(data_path)

# Convert 'datetime' column to datetime type
df['datetime'] = pd.to_datetime(df['datetime'])
df['hour'] = df['datetime'].dt.hour
df['day'] = df['datetime'].dt.day
df['month'] = df['datetime'].dt.month
df['year'] = df['datetime'].dt.year
df['weekday'] = df['datetime'].dt.weekday
df['is_weekend'] = df['weekday'] >= 5
df['is_holiday'] = df['holiday'] == 1

st.title("Bike Sharing Data Dashboard")
st.sidebar.header("Filter Data")

year_filter = st.sidebar.multiselect("Select Year", df['year'].unique(), default=df['year'].unique())
df = df[df['year'].isin(year_filter)]

# 1. Pola Penggunaan Sepeda per Jam
st.subheader("Pola Penggunaan Sepeda per Jam")
hourly_counts = df.groupby('hour')['count'].mean()
plt.figure(figsize=(10, 5))
sns.lineplot(x=hourly_counts.index, y=hourly_counts.values, marker='o')
plt.xlabel("Jam dalam Sehari")
plt.ylabel("Rata-rata Penyewaan Sepeda")
plt.title("Pola Penggunaan Sepeda per Jam")
st.pyplot(plt)
st.write("Puncak penggunaan terjadi pada jam sibuk kerja (pagi dan sore).")

# 2. Tren Penggunaan Sepeda Harian dan Tahunan
st.subheader("Tren Penggunaan Sepeda Harian dan Tahunan")
daily_counts = df.groupby('datetime')['count'].sum()
plt.figure(figsize=(12, 5))
sns.lineplot(x=daily_counts.index, y=daily_counts.values)
plt.xlabel("Tanggal")
plt.ylabel("Total Penyewaan Sepeda")
plt.title("Tren Penyewaan Sepeda Harian")
st.pyplot(plt)
st.write("Terlihat peningkatan penggunaan dari tahun ke tahun dan pola musiman yang jelas.")

# 3. Pengaruh Musim terhadap Penyewaan Sepeda
st.subheader("Pengaruh Musim terhadap Penyewaan Sepeda")
season_counts = df.groupby('season')['count'].mean()
plt.figure(figsize=(8, 5))
sns.barplot(x=season_counts.index, y=season_counts.values, palette="coolwarm")
plt.xlabel("Musim")
plt.ylabel("Rata-rata Penyewaan")
plt.title("Rata-rata Penyewaan Sepeda per Musim")
st.pyplot(plt)
st.write("Musim gugur memiliki jumlah penyewaan tertinggi, sedangkan musim dingin terendah.")

# 4. Perbedaan Hari Kerja dan Akhir Pekan
st.subheader("Perbedaan Hari Kerja vs Akhir Pekan")
weekend_counts = df.groupby('is_weekend')['count'].mean()
plt.figure(figsize=(6, 4))
sns.barplot(x=['Hari Kerja', 'Akhir Pekan'], y=weekend_counts.values, palette="viridis")
st.pyplot(plt)
st.write("Akhir pekan memiliki lebih banyak penyewaan untuk keperluan rekreasi.")

# 5. Pengaruh Cuaca terhadap Penyewaan
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
weather_counts = df.groupby('weather')['count'].mean()
plt.figure(figsize=(6, 4))
sns.barplot(x=weather_counts.index, y=weather_counts.values, palette="magma")
st.pyplot(plt)
st.write("Cuaca cerah memiliki jumlah penyewaan tertinggi, sedangkan hujan terendah.")

# 6. Puncak dan Penurunan Penyewaan per Bulan
st.subheader("Puncak dan Penurunan Penyewaan Sepeda per Bulan")
monthly_counts = df.groupby('month')['count'].mean()
plt.figure(figsize=(10, 5))
sns.lineplot(x=monthly_counts.index, y=monthly_counts.values, marker='o')
st.pyplot(plt)
st.write("Puncak penyewaan terjadi pada musim panas dan awal musim gugur.")

# 7. Hubungan antara Suhu, Kelembaban, dan Penyewaan Sepeda
st.subheader("Hubungan antara Suhu, Kelembaban, dan Penyewaan Sepeda")
plt.figure(figsize=(10, 5))
sns.scatterplot(x=df['temp'], y=df['count'], alpha=0.5)
st.pyplot(plt)
st.write("Ada korelasi positif antara suhu dan penyewaan sepeda.")

# 8. Perbedaan Hari Kerja dan Hari Libur
st.subheader("Perbedaan Hari Kerja vs Hari Libur")
holiday_counts = df.groupby('is_holiday')['count'].mean()
plt.figure(figsize=(6, 4))
sns.barplot(x=['Hari Kerja', 'Hari Libur'], y=holiday_counts.values, palette="coolwarm")
st.pyplot(plt)
st.write("Hari libur memiliki jumlah penyewaan yang lebih tinggi.")

# 9. Tren Penggunaan Sepeda dari Tahun ke Tahun
st.subheader("Tren Penggunaan Sepeda dari Tahun ke Tahun")
yearly_counts = df.groupby('year')['count'].sum()
plt.figure(figsize=(8, 5))
sns.barplot(x=yearly_counts.index, y=yearly_counts.values, palette="Blues")
st.pyplot(plt)
st.write("Peningkatan jumlah penyewaan sepeda yang signifikan di tahun 2012 dibandingkan 2011.")

# 10. Perbedaan Penyewa Biasa vs Terdaftar
st.subheader("Perbedaan Penyewa Biasa vs Terdaftar")
user_type_counts = df[['casual', 'registered']].sum()
plt.figure(figsize=(6, 4))
sns.barplot(x=['Casual', 'Registered'], y=user_type_counts.values, palette="Set2")
st.pyplot(plt)
st.write("Penyewa terdaftar lebih dominan dibanding penyewa biasa, dengan pola penggunaan yang mirip.")

st.write("Dashboard ini memberikan wawasan mendalam tentang pola penggunaan sepeda berdasarkan berbagai faktor seperti waktu, musim, cuaca, dan jenis pengguna.")
