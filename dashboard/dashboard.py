import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Mengatur tema visualisasi dasar agar rapi dan bersih
sns.set_theme(style="whitegrid")

# Konfigurasi Halaman Dashboard Web Streamlit
st.set_page_config(page_title="Bike Sharing Interactive Dashboard", layout="wide")

# Fungsi untuk memuat data harian dan data per jam secara efisien
@st.cache_data
def load_data():
    # Memuat data harian untuk metrik, tren bulanan, dan cuaca
    day_df = pd.read_csv("dashboard/main_data.csv")
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    
    # Memuat data per jam khusus untuk visualisasi analisis lanjutan (clustering)
    hour_df = pd.read_csv("data/hour.csv")
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

try:
    day_df, hour_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat berkas data. Pastikan posisi berkas sudah benar. Error: {e}")
    st.stop()

# Pemetaan label kategorikal agar sinkron dengan Google Colab
weather_mapping = {
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Ice Pallets'
}
day_df['weather_label'] = day_df['weathersit'].map(weather_mapping)
hour_df['weather_label'] = hour_df['weathersit'].map(weather_mapping)

# ==========================================
# KOMPONEN SIDEBAR INTERAKTIF
# ==========================================
st.sidebar.header("Filter Analisis Waktu")

min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

# Widget interaktif pilihan rentang tanggal di web
start_date, end_date = st.sidebar.date_input(
    label='Tentukan Rentang Tanggal:',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter dataset berdasarkan tanggal yang dipilih oleh user
filtered_day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & 
                         (day_df['dteday'] <= pd.to_datetime(end_date))]

filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & 
                           (hour_df['dteday'] <= pd.to_datetime(end_date))]

# ==========================================
# MAIN PAGE DASHBOARD (TAMPILAN WEB)
# ==========================================
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Aplikasi interaktif pemantauan performa rental sepeda berdasarkan tren waktu dan kondisi lingkungan.")

# Layout KPI Utama
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan (Total)", value=f"{filtered_day_df['cnt'].sum():,}")
with col2:
    st.metric("Pengguna Terdaftar (Registered)", value=f"{filtered_df['registered'].sum():,}" if 'filtered_df' in locals() else f"{filtered_day_df['registered'].sum():,}")
with col3:
    st.metric("Pengguna Kasual (Casual)", value=f"{filtered_df['casual'].sum():,}" if 'filtered_df' in locals() else f"{filtered_day_df['casual'].sum():,}")

st.markdown("---")

# Pengelompokan Tab Visualisasi di Halaman Web (Kembar dengan Colab 1, 2, 3)
tab1, tab2, tab3 = st.tabs(["📊 1. Tren Performa Rental 2012", "🌦️ 2. Pengaruh Kondisi Cuaca", "🚀 3. Analisis Lanjutan (Clustering)"])

with tab1:
    st.subheader("Tren Penyewaan Sepeda Bulanan Sepanjang Tahun 2012")
    # Agregasi bulanan khusus tahun 2012 (yr = 1)
    df_2012 = filtered_day_df[filtered_day_df['yr'] == 1]
    if not df_2012.empty:
        monthly_rent_2012 = df_2012.groupby('mnth').agg({'casual':'sum', 'registered':'sum', 'cnt':'sum'}).reset_index()
        
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(monthly_rent_2012['mnth'], monthly_rent_2012['registered'], marker='o', label='Registered', color='royalblue', linewidth=2)
        ax.plot(monthly_rent_2012['mnth'], monthly_rent_2012['casual'], marker='s', label='Casual', color='orange', linewidth=2)
        ax.plot(monthly_rent_2012['mnth'], monthly_rent_2012['cnt'], marker='D', label='Total', color='crimson', linestyle='--', linewidth=2)
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Penyewaan (Unit)")
        ax.set_xticks(monthly_rent_2012['mnth'])
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'])
        ax.legend(title="Tipe Pengguna")
        st.pyplot(fig)
    else:
        st.warning("Silakan sesuaikan rentang waktu filter di sidebar untuk menyertakan tahun 2012.")

with tab2:
    st.subheader("Rata-rata Penyewaan Sepeda per Jam Berdasarkan Kondisi Cuaca")
    weather_hourly_rent = filtered_hour_df.groupby('weather_label').agg({'cnt': 'mean'}).sort_values(by='cnt', ascending=False).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=weather_hourly_rent, x='weather_label', y='cnt', palette='Blues_r', hue='weather_label', legend=False, ax=ax)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan (Unit/Jam)")
    st.pyplot(fig)

with tab3:
    st.subheader("Karakteristik Penyewaan Berdasarkan Klaster Jam dan Hari Kerja")
    
    # Fungsi klasterisasi berbasis jam (Sama persis seperti di Google Colab Anda)
    def cluster_hours(hour):
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            return 'Peak Commute Hours (Jam Sibuk)'
        elif 10 <= hour <= 16:
            return 'Midday Leisure (Jam Santai)'
        else:
            return 'Off-Peak Hours (Jam Sepi)'

    filtered_hour_df['hour_cluster'] = filtered_hour_df['hr'].apply(cluster_hours)
    advanced_cluster = filtered_hour_df.groupby(['hour_cluster', 'workingday']).agg({'cnt': 'mean'}).reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=advanced_cluster, x='hour_cluster', y='cnt', hue='workingday', palette='Set2', ax=ax)
    ax.set_xlabel("Klaster Waktu")
    ax.set_ylabel("Rata-rata Penyewaan (Unit)")
    ax.legend(title="Hari Kerja", labels=["Hari Libur/Akhir Pekan (0)", "Hari Kerja (1)"])
    st.pyplot(fig)
