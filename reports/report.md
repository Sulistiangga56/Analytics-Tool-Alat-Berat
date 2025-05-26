# Analytics Dashboard Project
*Scientific Analytic Engineer Preparation — PAMA Persada*

## 1. Project Overview

Proyek ini bertujuan membangun dashboard analitik interaktif berbasis Streamlit untuk menyajikan data simulasi operasional alat berat, produksi tambang, dan performa unit. Proyek ini juga mencakup eksplorasi data, machine learning (regresi & klasifikasi), serta pengelolaan data dengan PostgreSQL sebagai backend database.

## 2. Use Case

- **Monitoring Kinerja Unit Tambang:** Menyediakan visualisasi konsumsi BBM, jam kerja, dan produktivitas unit.
- **Prediksi Konsumsi BBM:** Menggunakan regresi untuk memprediksi konsumsi BBM berdasarkan histori kerja unit.
- **Klasifikasi Risiko:** Mengelompokkan unit berdasarkan performa atau potensi risiko.

## 3. Arsitektur Sistem

analytics-dashboard/
│
├── app/ # Streamlit app (dashboard + ML + helper)
├── db/ # Koneksi & inisialisasi database PostgreSQL
├── data/ # Data dummy & simulasi
├── notebooks/ # Exploratory Data Analysis (EDA)
├── reports/ # Laporan & visualisasi
└── requirements.txt # Dependencies


## 4. Database Schema

Database menggunakan PostgreSQL dengan tabel utama:
- **units**: Data unit alat berat
- **operations**: Data jam kerja & konsumsi BBM
- **performance_metrics**: Data performa harian/mingguan
- **risk_classification**: Hasil klasifikasi ML (opsional)

Relasi antar tabel berbasis `unit_id` sebagai foreign key.

## 5. Teknologi yang Digunakan

- **Python**: Data processing, modeling, dashboard
- **PostgreSQL**: Database utama
- **SQLAlchemy**: ORM database connection
- **Pandas/Scikit-learn**: Data analysis & modeling
- **Streamlit**: Frontend dashboard
- **Matplotlib/Seaborn/Plotly**: Visualisasi interaktif
- **Jupyter Notebook**: EDA & eksperimen awal

## 6. Analisis & Machine Learning

### Regresi
- **Model**: Linear Regression & Random Forest
- **Target**: `fuel_consumption` (l/day)
- **Fitur**: `engine_hours`, `load_factor`, `unit_type`

### Klasifikasi (Opsional)
- **Model**: Logistic Regression / Decision Tree
- **Target**: `risk_category` (Low, Medium, High)
- **Fitur**: Kombinasi metrik performa

## 7. Hasil & Evaluasi

- Model regresi memberikan akurasi MAE di bawah 10% untuk data simulasi.
- Visualisasi membantu melihat outlier dan tren performa.
- Dashboard responsif & user-friendly.

## 8. Pengembangan Selanjutnya

- Integrasi data real-time dari IoT atau API.
- Validasi model dengan data nyata.
- Menambahkan alert system berbasis rule atau klasifikasi.

## 9. Penutup

Proyek ini menjadi simulasi nyata peran **Scientific Analytic Engineer**, yang menggabungkan kemampuan data engineering, analisis statistik, dan visualisasi yang berdampak pada pengambilan keputusan operasional di dunia pertambangan.