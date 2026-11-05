# Proyek Analisis Data: Bike Sharing Dataset 📊

Proyek akhir ini merupakan aplikasi pelaporan interaktif yang menganalisis performa penyewaan sepeda berdasarkan tren waktu harian/bulanan tahun 2011-2012, pengaruh kondisi cuaca, serta klasterisasi perilaku pengguna (Manual Clustering).

## Struktur Direktori
submission
├── dashboard
│   ├── dashboard.py
│   └── main_data.csv
├── data
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt

## Langkah Menjalankan Dashboard di Local Perangkat Anda

### 1. Menginstal Dependency (Library Pendukung)
Pastikan path terminal mengarah ke direktori proyek ini, lalu pasang pustaka wajib menggunakan perintah:
pip install -r requirements.txt

### 2. Meluncurkan Aplikasi Dashboard Streamlit
Masuk ke dalam folder dashboard, kemudian jalankan berkas python:
cd dashboard
streamlit run dashboard.py

*Catatan: Gunakan widget filter tanggal pada sidebar untuk melihat visualisasi data secara dinamis dari rentang 2011-01-01 hingga 2012-12-31.*
