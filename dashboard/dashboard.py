import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Mengatur tema visualisasi dasar agar rapi
sns.set_theme(style="whitegrid")

# Konfigurasi Halaman Dashboard Web Streamlit
st.set_page_config(page_title="Bike Sharing Interactive Dashboard", layout="wide")

# Fungsi untuk memuat data dashboard (menggunakan main_data.csv di folder dashboard)
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

try:
    main_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat berkas 'dashboard/main_data.csv'. Pastikan posisi berkas sudah benar. Error: {e}")
    st.stop()

# ==========================================
# KOMPONEN SIDEBAR INTERAKTIF
# ==========================================
st.sidebar.header("Filter Analisis Waktu")

min_date = main_df['dteday'].min()
max_date = main_df['dteday'].max()

# Widget interaktif pilihan rentang tanggal di web
start_date, end_date = st.sidebar.date_input(
    label='Tentukan Rentang Tanggal:',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter dataset utama berdasarkan tanggal yang dipilih oleh user
filtered_df = main_df[(main_df['dteday'] >= pd.to_datetime(start_date)) & 
                       (main_df['dteday'] <= pd.to_datetime(end_date))]

# ==========================================
# MAIN PAGE DASHBOARD (TAMPILAN WEB)
# ==========================================
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Aplikasi interaktif pemantauan performa rental sepeda berdasarkan tren waktu dan kondisi lingkungan.")

# Layout KPI (Key Performance Indicators) Utama
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan (Total)", value=f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Pengguna Terdaftar (Registered)", value=f"{filtered_df['registered'].sum():,}")
with col3:
    st.metric("Pengguna Kasual (Casual)", value=f"{filtered_df['casual'].sum():,}")

st.markdown("---")

# Pengelompokan Tab Visualisasi di Halaman Web
tab1, tab2 = st.tabs(["📊 Tren Performa Rental", "🌦️ Distribusi Per Musim"])

with tab1:
    st.subheader("Grafik Tren Penyewaan Sepeda Harian")
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(filtered_df['dteday'], filtered_df['cnt'], color='crimson', alpha=0.8, linewidth=1.5)
    ax.set_xlabel("Tanggal Operasional")
    ax.set_ylabel("Jumlah Total Peminjaman")
    st.pyplot(fig)

with tab2:
    st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Kategori Musim")
    season_mapping = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    filtered_df['season_label'] = filtered_df['season'].map(season_mapping)
    season_data = filtered_df.groupby('season_label')['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=season_data, x='season_label', y='cnt', palette='viridis', hue='season_label', legend=False, ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan Per Hari")
    st.pyplot(fig)

st.caption("Hak Cipta © Proyek Akhir Analisis Data - Kelas Dicoding Indonesia")
