@echo off
echo Memulai proses Data Scraping dan Storing...
cd "C:\Users\Moreno\Documents\GitHub\TUGAS_SELEKSI_1_13524096"
python "Data Scraping\src\scraper.py"
python "Data Storing\src\import_data.py"

echo Menjalankan proses ETL Data Warehouse...
mysql -u root -e "SOURCE Data Warehouse/src/dwh_etl.sql"

echo Proses selesai.
exit