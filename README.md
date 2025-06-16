# Nama Kelompok
- Ikhwan Ash-Shiddiqi
- Irma Fitriani

# Sistem Pendukung Keputusan Perekrutan Teknisi - Metode COPRAS

![Sistem Pendukung Keputusan](https://img.shields.io/badge/Metode-COPRAS-blue)
![Bahasa Pemrograman](https://img.shields.io/badge/Python-3.x-blueviolet)
![Framework Web](https://img.shields.io/badge/Flask-Web-green)
![Frontend](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FBootstrap-orange)

## Deskripsi Proyek

Proyek ini adalah sebuah Sistem Pendukung Keputusan (SPK) berbasis web yang dirancang untuk membantu dalam proses perekrutan karyawan, khususnya untuk posisi teknisi. Sistem ini mengimplementasikan metode **COPRAS (Complex Proportional Assessment)** untuk melakukan penilaian dan perangkingan calon pegawai berdasarkan berbagai kriteria yang telah ditentukan. Pengguna dapat mengunggah data calon pegawai dalam format CSV, dan sistem akan secara otomatis menghitung skor COPRAS serta menampilkan ranking alternatif yang direkomendasikan.

Tujuan utama dari sistem ini adalah untuk menyediakan alat yang objektif dan transparan dalam pengambilan keputusan perekrutan, mengurangi bias subjektif, dan mempercepat proses seleksi.

## Fitur Utama

* **Perekrutan Berbasis Kriteria:** Mendukung penilaian calon berdasarkan kriteria yang dapat disesuaikan (misalnya, Pengalaman, Pendidikan, Usia, Status Perkawinan, Alamat, dll.).
* **Metode COPRAS:** Menggunakan algoritma COPRAS yang robust untuk perhitungan prioritas alternatif.
* **Antarmuka Web Interaktif:** Dibangun dengan Flask (Python) dan Bootstrap (HTML/CSS) untuk antarmuka pengguna yang intuitif dan responsif.
* **Upload File CSV:** Memungkinkan pengguna untuk mengunggah data calon pegawai dari file CSV, sehingga memudahkan integrasi dengan data yang sudah ada.
* **Tampilan Hasil Komprehensif:** Menampilkan ranking alternatif beserta detail perhitungan COPRAS (nilai $S_{i+}$, $S_{i-}$, $Q_i$, dan $N_i$) dalam bentuk tabel yang mudah dibaca.
* **Validasi Input:** Dilengkapi dengan validasi dasar untuk memastikan format file CSV dan kelengkapan data kriteria.
* **Konfigurasi Kriteria Dinamis:** Kriteria, bobot, dan jenis kriteria (benefit/cost) dapat dengan mudah dikonfigurasi di sisi backend (`app.py`).

## Instalasi

Ikuti langkah-langkah berikut untuk menjalankan proyek ini di lingkungan lokal Anda.

### Prasyarat

Pastikan Anda telah menginstal:
* [Python 3.x](https://www.python.org/downloads/)
* `pip` (manajer paket Python)

### Langkah-langkah Instalasi

1.  **Clone Repositori:**
    ```bash
    git clone [https://github.com/USERNAME_ANDA/NAMA_REPOSITORI_ANDA.git](https://github.com/USERNAME_ANDA/NAMA_REPOSITORI_ANDA.git)
    cd NAMA_REPOSITORI_ANDA
    ```
    *(Ganti `USERNAME_ANDA` dan `NAMA_REPOSITORI_ANDA` dengan detail GitHub Anda)*

2.  **Buat Virtual Environment (Disarankan):**
    ```bash
    python -m venv venv
    ```

3.  **Aktifkan Virtual Environment:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Instal Dependensi:**
    ```bash
    pip install pandas numpy Flask
    ```

5.  **Struktur Folder Proyek:**
    Pastikan struktur folder Anda seperti ini:
    ```
    copras_spk_perekrutan/
    ├── app.py
    ├── copras_logic.py
    ├── templates/
    │   └── index.html
    └── uploads/
    ```
    Folder `uploads/` akan dibuat secara otomatis saat aplikasi berjalan jika belum ada.
