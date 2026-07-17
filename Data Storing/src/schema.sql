-- Buat database
CREATE DATABASE IF NOT EXISTS btd6_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Pakai database-nya
USE btd6_db;


-- TABEL UTAMA

-- Data tiap round
CREATE TABLE IF NOT EXISTS round (
    round_id INT PRIMARY KEY,
    duration DECIMAL(10,2),
    base_rbe INT,
    pop_cash DECIMAL(10,2),
    bonus_cash DECIMAL(10,2),
    layers INT,
    base_xp INT
) ENGINE=InnoDB;

-- Daftar jenis bloon
CREATE TABLE IF NOT EXISTS bloon (
    bloon_id INT PRIMARY KEY,
    bloon_name VARCHAR(100) NOT NULL
) ENGINE=InnoDB;


-- Tabel RELASI (SPAWN)

-- Relasi round ↔ bloon (plus jumlah)
CREATE TABLE IF NOT EXISTS spawn (
    spawn_id INT PRIMARY KEY,
    round_id INT NOT NULL,
    bloon_id INT NOT NULL,
    quantity INT NOT NULL,

    -- FK ke round
    CONSTRAINT fk_spawn_round
        FOREIGN KEY (round_id)
        REFERENCES round(round_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- FK ke bloon
    CONSTRAINT fk_spawn_bloon
        FOREIGN KEY (bloon_id)
        REFERENCES bloon(bloon_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;