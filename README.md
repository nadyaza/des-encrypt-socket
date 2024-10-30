# TUGAS 2 KEAMANAN INFORMASI
### Implementasi Enkripsi dan Dekripsi DES dengan Socket Programming

## Deskripsi Tugas
Pada tugas ini, kami mengembangkan program enkripsi dan dekripsi menggunakan algoritma DES dengan mode CBC. Program ini memungkinkan transfer string terenkripsi antara dua pengguna (client dan server) melalui *socket programming*. Client dapat mengirim pesan terenkripsi ke server, dan server akan mendekripsi pesan tersebut, menampilkan hasilnya, kemudian mengirim balasan yang juga terenkripsi.

### Anggota Kelompok
1. **Nadya Zuhria Amana**  
   - **NRP**: 5025211058  
   - **Role**: Pengembangan Kode Server (`server.py`)  

2. **Dilla Wahdana**  
   - **NRP**: 502521060  
   - **Role**: Pengembangan Kode Client (`client.py`)  

### Pembagian Tugas

- **Nadya Zuhria Amana (Server)**  
  - Implementasi kode `server.py` untuk:
    - Menjalankan server yang menerima koneksi dari client menggunakan *socket programming*.
    - Menggunakan algoritma DES untuk enkripsi dan dekripsi pesan dengan mode **CBC**.
    - Menangani pesan yang diterima dari client, melakukan dekripsi, dan menampilkan hasil dekripsi di server.
    - Mengirimkan balasan yang terenkripsi kembali ke client.

- **Dilla Wahdana (Client)**  
  - Implementasi kode `client.py` untuk:
    - Menjalankan client yang terhubung ke server menggunakan *socket programming*.
    - Menggunakan algoritma DES untuk enkripsi pesan dengan mode **CBC** sebelum dikirimkan ke server.
    - Menerima pesan balasan terenkripsi dari server, mendekripsinya, dan menampilkan hasil dekripsi di sisi client.
    - Mengelola interaksi pengguna untuk memasukkan pesan yang akan dikirim ke server dan menerima respons dari server.

## Cara Menjalankan Program

1. **Menjalankan Server**
   - Buka terminal, arahkan ke direktori yang berisi `server.py`, lalu jalankan perintah:
     ```bash
     python server.py
     ```
   - Server akan berjalan dan menunggu koneksi dari client.

2. **Menjalankan Client**
   - Buka terminal lain, arahkan ke direktori yang berisi `client.py`, lalu jalankan perintah:
     ```bash
     python client.py
     ```
   - Masukkan pesan yang ingin dikirim ke server, dan pesan tersebut akan terenkripsi sebelum dikirim.
   - Client akan menerima balasan dari server dalam bentuk terenkripsi, lalu mendekripsi dan menampilkan hasilnya.

## Lisensi
Kode ini dibuat untuk memenuhi Tugas 2 Keamanan Informasi

