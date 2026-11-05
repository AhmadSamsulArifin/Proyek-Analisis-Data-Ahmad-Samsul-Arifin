# Proyek Analisis Data: Bike Sharing Dataset 📊

Proyek akhir ini merupakan aplikasi pelaporan interaktif yang menganalisis performa penyewaan sepeda berdasarkan tren waktu harian/bulanan tahun 2011-2012, pengaruh kondisi cuaca, serta klasterisasi perilaku pengguna (Manual Clustering).

## Setup Environment - Anaconda
conda create --name bike-sharing-ds python=3.9

conda activate bike-sharing-ds

pip install -r requirements.txt


## Setup Environment - Shell/Terminal
mkdir submission

cd submission

pipenv install

pipenv shell

pip install -r requirements.txt

## Run streamlit app
cd dashboard

streamlit run dashboard.py

