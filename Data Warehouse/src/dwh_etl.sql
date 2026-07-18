USE btd6_dwh;


-- isi dim_bloon dari data awal
INSERT IGNORE INTO dim_bloon (bloon_id, bloon_name)
SELECT 
    bloon_id, 
    bloon_name
FROM btd6_db.bloon;


-- isi dim_round (sekalian hitung total_cash)
INSERT IGNORE INTO dim_round (
    round_id, duration, base_rbe, 
    pop_cash, bonus_cash, total_cash, 
    layers, base_xp
)
SELECT 
    round_id,
    duration,
    base_rbe,
    pop_cash,
    bonus_cash,
    pop_cash + bonus_cash,   -- biar ga hitung ulang nanti
    layers,
    base_xp
FROM btd6_db.round;


-- fact table (butuh key dari dimensi)
INSERT IGNORE INTO fact_spawn (spawn_id, round_key, bloon_key, quantity, extracted_at)
SELECT 
    s.spawn_id,
    dr.round_key,
    db.bloon_key,
    s.quantity,
    s.extracted_at
FROM btd6_db.spawn s
JOIN dim_round dr ON s.round_id = dr.round_id
JOIN dim_bloon db ON s.bloon_id = db.bloon_id;