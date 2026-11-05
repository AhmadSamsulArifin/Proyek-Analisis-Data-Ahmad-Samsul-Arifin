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
    day_df = pd.read_csv("dashboard/main_data.csv")
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    
    hour_df = pd.read_csv("data/hour.csv")
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

try:
    day_df, hour_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat berkas data. Pastikan posisi berkas sudah benar. Error: {e}")
    st.stop()

# Pemetaan label kategorikal
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
    st.metric("Pengguna Terdaftar (Registered)", value=f"{filtered_day_df['registered'].sum():,}")
with col3:
    st.metric("Pengguna Kasual (Casual)", value=f"{filtered_day_df['casual'].sum():,}")

st.markdown("---")

# Pengelompokan Tab Visualisasi di Halaman Web
tab1, tab2, tab3 = st.tabs(["📊 1. Tren Performa Rental 2012", "🌦️ 2. Pengaruh Kondisi Cuaca", "🚀 3. Analisis Lanjutan (Clustering)"])

with tab1:
    st.subheader("Tren Penyewaan Sepeda Bulanan Sepanjang Tahun 2012")
    # Agregasi bulanan khusus tahun 2012 (yr = 1) dari data yang terfilter
    df_2012 = filtered_day_df[filtered_day_df['yr'] == 1]
    
    if not df_2012.empty:
        monthly_rent_2012 = df_2012.groupby('mnth').agg({'casual':'sum', 'registered':'sum', 'cnt':'sum'}).reset_index()
        
        # Mengubah angka bulan menjadi label nama bulan secara dinamis
        month_names = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'Mei', 6:'Jun', 7:'Jul', 8:'Agu', 9:'Sep', 10:'Okt', 11:'Nov', 12:'Des'}
        monthly_rent_2012['month_label'] = monthly_rent_2012['mnth'].map(month_names)
        
        fig, ax = plt.subplots(figsize=(12, 5))
        # Menggunakan 'month_label' langsung sebagai sumbu X agar Matplotlib memetakan label secara otomatis dan dinamis
        ax.plot(monthly_rent_2012['month_label'], monthly_rent_2012['registered'], marker='o', label='Registered', color='royalblue', linewidth=2)
        ax.plot(monthly_rent_2012['month_label'], monthly_rent_2012['casual'], marker='s', label='Casual', color='orange', linewidth=2)
        ax.plot(monthly_rent_2012['month_label'], monthly_rent_2012['cnt'], marker='D', label='Total', color='crimson', linestyle='--', linewidth=2)
        
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Penyewaan (Unit)")
        ax.legend(title="Tipe Pengguna")
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data untuk tahun 2012 pada rentang tanggal yang Anda pilih. Silakan sesuaikan filter rentang waktu di sidebar.")

with tab2:
    st.subheader("Rata-rata Penyewaan Sepeda per Jam Berdasarkan Kondisi Cuaca (2011-2012)")
    if not filtered_hour_df.empty:
        weather_hourly_rent = filtered_hour_df.groupby('weather_label').agg({'cnt': 'mean'}).sort_values(by='cnt', ascending=False).reset_index()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=weather_hourly_rent, x='weather_label', y='cnt', palette='Blues_r', hue='weather_label', legend=False, ax=ax)
        ax.set_xlabel("Kondisi Cuaca")
        ax.set_ylabel("Rata-rata Penyewaan (Unit/Jam)")
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data tersedia untuk rentang tanggal yang dipilih.")

with tab3:
    st.subheader("Karakteristik Penyewaan Berdasarkan Klaster Jam dan Hari Kerja")
    
    if not filtered_hour_df.empty:
        def cluster_hours(hour):
            if 7 <= hour <= 9 or 17 <= hour <= 19:
                return 'Peak Commute Hours (Jam Sibuk)'
            elif 10 <= hour <= 16:
                return 'Midday Leisure (Jam Santai)'
            else:
                return 'Off-Peak Hours (Jam Sepi)'

        # Menyalin dataframe untuk menghindari SettingWithCopyWarning
        hour_cluster_df = filtered_hour_df.copy()
        hour_cluster_df['hour_cluster'] = hour_cluster_df['hr'].apply(cluster_hours)
        advanced_cluster = hour_cluster_df.groupby(['hour_cluster', 'workingday']).agg({'cnt': 'mean'}).reset_index()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=advanced_cluster, x='hour_cluster', y='cnt', hue='workingday', palette='Set2', ax=ax)
        ax.set_xlabel("Klaster Waktu")
        ax.set_ylabel("Rata-rata Penyewaan (Unit)")
        ax.legend(title="Hari Kerja", labels=["Hari Libur/Akhir Pekan (0)", "Hari Kerja (1)"])
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data tersedia untuk rentang tanggal yang dipilih.")
