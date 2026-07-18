# Tugas Seleksi 1 Asisten Basis Data 2026 🎈🐒

## Author
**Nama:** Moreno Syawali Ganda Sugita  
**NIM:** 13524096  

---

## Deskripsi Singkat Data dan DBMS
Tugas seleksi ini melakukan ekstraksi (Web Scraping) dan pemodelan data (Data Storing) dari ronde pada permainan **Bloons Tower Defense 6 (BTD6)**. Data yang diambil mencakup statistik setiap ronde (seperti durasi, pendapatan, dan RBE) serta detail Bloons waves yang muncul.

**DBMS yang digunakan:** MariaDB (Engine InnoDB).

**Alasan Memilih Topik:**
Yang pertama, saya sedang kecanduan main BTD6. Yang kedua, saya sedang addicted main BTD6. Namun, karena sudah waktunya mengerjakan tugas seleksi, saya mau mengerjakan yang berkaitan dengan game permusuhan antara monyet dan balon. Secara teknis, alasan saya memilih topik ini karena tabelnya terlihat sederhana. Namun, setelah ditilik lebih lanjut, terdapat beberapa keputusan desain dikarenakan mekanisme permainan yang tidak sesederhana itu. Oleh karena itu, saya tertarik untuk mencoba topik ini.

---

## Tahap 1: Data Scraping
Skrip *scraper* ditulis menggunakan Python dan `BeautifulSoup` untuk melakukan *parsing* elemen HTML DOM dari halaman web wiki BTD6.

**1. Instalasi Dependencies:**  
Pastikan Python 3 sudah terinstal, lalu instal library eksternal:

    pip install requests beautifulsoup4

**2. Eksekusi Skrip:**  
Jalankan skrip *scraper* dari *root* repositori:

    python "Data Scraping/src/scraper.py"

## Struktur File JSON
Hasil keluaran dari skrip *scraper* dipisah menjadi 3 *file* JSON untuk pendekatan normalisasi, sehingga mempermudah proses Load ke dalam RDBMS. Ketiga *file* ini di simpan di dalam direktori `Data Scraping/data/`.

**1. `bloons.json`**
Berisi daftar unik jenis Bloon yang pernah muncul pada ronde 1-140.
* `bloon_id` (Integer): ID unik untuk setiap jenis bloon.
* `bloon_name` (String): Nama varian bloon (contoh: "Camo Regrow Yellow").

**2. `rounds.json`**
Berisi data statistik spesifik dari setiap ronde permainan.
* `round_id` (Integer): Nomor urut ronde permainan.
* `duration` (Decimal): Lama durasi ronde dalam detik.
* `base_rbe` (Integer): Kepadatan bloon di ronde tersebut (*Red Bloon Equivalent*).
* `pop_cash` (Decimal): Total uang hasil memecahkan seluruh bloon.
* `bonus_cash` (Decimal): Uang bonus di akhir ronde.
* `layers` (Integer): Total lapisan bloon.
* `base_xp` (Integer): Base poin pengalaman (XP) yang diberikan ronde.

**3. `spawns.json`**
Berisi informasi gelombang kemunculan bloon pada suatu ronde.
* `spawn_id` (Integer): *Surrogate Key* untuk setiap gelombang.
* `round_id` (Integer): Referensi ke `rounds.json`.
* `bloon_id` (Integer): Referensi ke `bloons.json`.
* `quantity` (Integer): Jumlah bloon yang muncul pada gelombang tersebut.

---

## Tahap 2: Data Storing (RDBMS)
Tahap ini memuat data JSON ke dalam sistem basis data relasional MariaDB.

**1. Persiapan Skema (DDL):**  
Buka terminal MariaDB dan eksekusi *file* skema untuk membuat *database* `btd6_db` beserta tabel-tabelnya:

    source C:/path/to/repo/Data Storing/src/schema.sql;

**2. Proses Load Data (ETL):**  
Pastikan *library* konektor Python ke MySQL/MariaDB sudah terinstal:

    pip install mysql-connector-python

Lalu, jalankan skrip *Data Loader* melalui PowerShell/terminal untuk mengekstrak JSON dan melakukan `INSERT` ke MariaDB:

    python "Data Storing/src/import_data.py"

**3. Ekspor / Data Dump:**  
Hasil akhir *database* lengkap telah diekspor dan dapat direstorasi melalui *file* SQL berikut:
    `Data Storing/export/btd6_database.sql`

---

## Struktur ERD dan Diagram Relasional

### 1. ERD
![ERD](Data%20Storing/design/ERD.png)

### 2. Relational Model
![Relational Model](Data%20Storing/design/Relational%20Model.png)

**Translasi ERD menjadi Relational Model**
Relasi *Many-to-Many* (M:N) ditranslasikan menjadi tabel bernama `spawn`. Yang secara teori, umumnya menggunakan *Composite Primary Key* (`round_id` + `bloon_id`). Namun, sistem BTD6 memiliki mekanisme **Repeating Waves**, di mana tipe Bloon yang sama dapat muncul beberapa kali secara terpisah pada ronde yang sama. Jika *Composite Key* digunakan, DBMS akan menolak penyimpanan gelombang kedua. Sebagai solusi, atribut `spawn_id` ditambahkan sebagai **Surrogate Key**.

---

## Screenshots Eksekusi Program

### 1. Eksekusi Scraper
![Data Scraping](Data%20Scraping/screenshots/bukti.png)

### 2. Eksekusi ETL
![Bukti CREATE TABLE](Data%20Storing/screenshots/bukti_create.png)
![Bukti ETL](Data%20Storing/screenshots/bukti_etl.png)

### 3. Contoh Query
* Menampilkan waves bloon pada ronde 4
![Image 1](Data%20Storing/screenshots/image1.png)
* Menampilkan ronde mana saja yang memunculkan bloon tipe MOAB
![Image 2a](Data%20Storing/screenshots/image2a.png)
![Image 2a](Data%20Storing/screenshots/image2b.png)
* Menampilkan 5 ronde yang memiliki kuantitas terbanyak
![Image 3](Data%20Storing/screenshots/image3.png)
* Menampilkan 5 ronde yang menghasilkan pendapatan terbanyak
![Image 4](Data%20Storing/screenshots/image4.png)

---

## Tahap 3 (Bonus): Data Warehouse

**1. Arsitektur Pemodelan (Star Schema):**
Skema relasional diubah menjadi bentuk *Star Schema*:
* **`fact_spawn`**: Tabel fakta yang mencatat kejadian (*event*) munculnya gelombang bloon (menyimpan `quantity`).
* **`dim_round`**: Tabel dimensi yang menyimpan atribut statis ronde permainan (termasuk *pre-computed column* `total_cash` untuk meringankan beban agregasi analitik).
* **`dim_bloon`**: Tabel dimensi yang berisi katalog jenis bloon.

**Keputusan Desain:**
Pada Data Warehouse ini, identitas asli dari sistem operasional (`round_id` dan `bloon_id`) tetap dipertahankan di dalam tabel dimensi sebagai *Natural Key* (Business Key) untuk menjaga agar data tetap bisa dicari. Namun, *Primary Key* utama untuk mengikat relasi antar tabel menggunakan **Surrogate Key** buatan (`round_key`, `bloon_key`, `spawn_key` dengan tipe `AUTO_INCREMENT`). 
Pendekatan ini diterapkan untuk mengantisipasi *Slowly Changing Dimensions* (SCD) serta memastikan stabilitas sistem analitik dari potensi anomali perubahan ID pada sistem sumber.

**2. Proses Migrasi:**
Pemindahan data dari `btd6_db` (OLTP) ke `btd6_dwh` (OLAP) dilakukan secara *bulk* menggunakan SQL murni (`INSERT INTO ... SELECT`). Skrip ini memanfaatkan relasi `JOIN` untuk mencocokkan *Natural Key* dan menghasilkan relasi *Surrogate Key* yang valid pada *Fact Table*.
![Bukti CREATE TABLE](Data%20Warehouse/screenshots/bukti_create.png)
![Bukti ETL](Data%20Warehouse/screenshots/bukti_etl.png)

**3. Data Analytics:**
Data Warehouse ini telah diuji keandalannya menggunakan *query* analitik kompleks untuk mendemonstrasikan efisiensi agregasi *Star Schema*, antara lain:
* Menampilkan jenis bloon yang paling banyak muncul.
![Image 1](Data%20Warehouse/screenshots/image1.png)
* Analisis rasio "Harga per Kemunculan Bloon" di 5 ronde tersibuk.
![Image 2](Data%20Warehouse/screenshots/image2.png)
* Melacak ronde dengan kemunculan MOAB terbanyak.
![Image 3](Data%20Warehouse/screenshots/image3.png)

---

## Deklarasi Penggunaan AI

**1. Bagian-bagian yang dibantu oleh AI:**
* **Debugging:** Menyelesaikan kendala teknis *environment* lokal.
* **Perekomendasian:** Memberi referensi/rekomendasi web page yang cocok untuk dijadikan bahan scraping (bukan memberikan link, melainkan ciri-cirinya saja).
* **Pemformatan Dokumentasi:** Membantu merapikan layout pada dokumen README ini.

**2. Bagian-bagian yang tetap dikerjakan sendiri:**
* **Perancangan Arsitektur:** Pemilihan topik, desain ERD dan Relational Model.
* **Pengembangan Skrip:** Analisis elemen HTML pada BTD6 wiki dan ekstraksi menggunakan library `BeautifulSoup`.
* **Eksekusi Keseluruhan:** Eksekusi program di terminal lokal, serta pengujian *query* SQL untuk membuktikan relasi berjalan dengan benar.

**3. Refleksi dari Penggunaan AI:**
Penggunaan AI dalam tugas seleksi ini sangat meningkatkan efisiensi, terutama dalam debugging masalah teknis yang mungkin membutuhkan waktu berjam-jam untuk mencari tahu kesalahan pengaturan laptop. Namun, saya tidak secara mentah memberikan seluruh data ke AI untuk dikerjakan seluruhnya, melainkan untuk bagian analisis, perancangan, dan eksekusi tetap dikerjakan oleh saya sendiri. In the end, saya harus memiliki pemahaman mengenai materi ini terlebih dahulu agar output yang AI hasilkan dapat divalidasi, dikoreksi, dan diintegrasikan dengan benar.

---

## Referensi
* **Target Data:** [BTD6 Wiki - List of rounds in BTD6](https://www.bloonswiki.com/List_of_rounds_in_BTD6)
* **Python Stack:** Requests, BeautifulSoup4, JSON, mysql-connector-python.
* **DBMS Engine:** MariaDB (InnoDB).
* **Teori Basis Data:** A. Silberschatz, H.F. Korth, S. Sudarshan, ‘Database System Concepts’, McGraw Hill. (Referensi Materi Kuliah)