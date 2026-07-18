USE btd6_db;


-- 1. Index untuk pencarian nama bloon

-- tanpa index, query ini bisa agak lambat kalau datanya besar
SELECT bloon_id, bloon_name
FROM bloon
WHERE bloon_name = 'DDT';

-- tambahin index agar lookup lebih cepat
CREATE INDEX idx_bloon_name ON bloon(bloon_name);

-- query yang sama, tapi sekarang sudah pakai index (ref)
SELECT bloon_id, bloon_name
FROM bloon
WHERE bloon_name = 'DDT';


-- 2. Subquery vs JOIN

-- versi subquery (kurang efisien)
SELECT round_id, quantity
FROM spawn
WHERE bloon_id IN (
    SELECT bloon_id
    FROM bloon
    WHERE bloon_name = 'ZOMG'
);

-- versi join, biasanya lebih ringan
SELECT s.round_id, s.quantity
FROM spawn s
JOIN bloon b ON s.bloon_id = b.bloon_id
WHERE b.bloon_name = 'ZOMG';


-- 3. WHERE vs HAVING

-- filter setelah GROUP BY (kurang optimal)
SELECT round_id, COUNT(spawn_id) AS total_waves
FROM spawn
GROUP BY round_id
HAVING round_id > 100;

-- filter dulu baru agregasi
SELECT round_id, COUNT(spawn_id) AS total_waves
FROM spawn
WHERE round_id > 100
GROUP BY round_id;