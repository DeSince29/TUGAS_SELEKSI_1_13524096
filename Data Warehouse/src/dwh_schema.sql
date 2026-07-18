-- Setup database DWH
CREATE DATABASE IF NOT EXISTS btd6_dwh;
USE btd6_dwh;

-- Dimensi: bloon
CREATE TABLE IF NOT EXISTS dim_bloon (
    bloon_key INT AUTO_INCREMENT PRIMARY KEY,
    bloon_id INT NOT NULL UNIQUE, -- id dari data asli
    bloon_name VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- Dimensi: round
CREATE TABLE IF NOT EXISTS dim_round (
    round_key INT AUTO_INCREMENT PRIMARY KEY,
    round_id INT NOT NULL UNIQUE, -- id dari OLTP
    duration DECIMAL(10,2),
    base_rbe INT,
    pop_cash DECIMAL(10,2),
    bonus_cash DECIMAL(10,2),
    total_cash DECIMAL(10,2),     -- pop_cash + bonus_cash
    layers INT,
    base_xp INT
) ENGINE=InnoDB;

-- Fact table: spawn
CREATE TABLE IF NOT EXISTS fact_spawn (
    spawn_key INT AUTO_INCREMENT PRIMARY KEY,
    spawn_id INT NOT NULL UNIQUE,  -- referensi dari data awal
    round_key INT NOT NULL,
    bloon_key INT NOT NULL,
    quantity INT,
    extracted_at DATETIME,

    -- relasi ke dimensi
    FOREIGN KEY (round_key) REFERENCES dim_round(round_key),
    FOREIGN KEY (bloon_key) REFERENCES dim_bloon(bloon_key)
) ENGINE=InnoDB;