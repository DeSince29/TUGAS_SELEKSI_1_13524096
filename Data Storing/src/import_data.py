import mysql.connector
import json
import os

# Config Database
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'btd6_db'
}

# Path ke folder JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, '..', '..', 'Data Scraping', 'data')

def load_json(filename):
    filepath = os.path.join(JSON_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("Start Import...")

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Load data
        print("Load JSON...")
        bloons = load_json('bloons.json')
        rounds = load_json('rounds.json')
        spawns = load_json('spawns.json')

        # Ubah ke format tuple (biar bisa executemany)
        bloon_values = [(b['bloon_id'], b['bloon_name']) for b in bloons]

        round_values = [(
            r['round_id'], r['duration'], r['base_rbe'],
            r['pop_cash'], r['bonus_cash'], r['layers'], r['base_xp']
        ) for r in rounds]

        spawn_values = [(
            s['spawn_id'], s['round_id'], s['bloon_id'], s['quantity']
        ) for s in spawns]

        # Insert dulu tabel utama
        print(f"Insert bloon ({len(bloon_values)} data)...")
        cursor.executemany(
            "INSERT INTO bloon (bloon_id, bloon_name) VALUES (%s, %s)",
            bloon_values
        )

        print(f"Insert round ({len(round_values)} data)...")
        cursor.executemany(
            "INSERT INTO round (round_id, duration, base_rbe, pop_cash, bonus_cash, layers, base_xp) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            round_values
        )

        # Terakhir tabel spawn (karena ada FK)
        print(f"Insert spawn ({len(spawn_values)} data)...")
        cursor.executemany(
            "INSERT INTO spawn (spawn_id, round_id, bloon_id, quantity) VALUES (%s, %s, %s, %s)",
            spawn_values
        )

        conn.commit()
        print("Don.")

    except mysql.connector.Error as err:
        print(f"[DB ERROR] {err}")
        if 'conn' in locals() and conn.is_connected():
            conn.rollback()
            print("Rollback")

    except FileNotFoundError as err:
        print(f"[FILE ERROR] {err}")

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    main()