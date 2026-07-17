import requests
from bs4 import BeautifulSoup
import json
import time
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

# Link Tujuan
BASE_URL = 'https://www.bloonswiki.com/List_of_rounds_in_BTD6'

# Batas sesuai round yang tidak random
MAX_ROUND = 140

# No no spam
DELAY = 2


def fetch_html(url: str) -> bytes:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64); Seleksi Asisten Basis Data/13524096@std.stei.itb.ac.id'
    }

    logging.info(f"Fetching: {url}")
    time.sleep(DELAY)

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch page (status {response.status_code})")

    return response.content


def clean_number(text: str) -> str:
    # "All in One" aahh function
    return (
        # Hapus akumulasi
        text.split('(')[0]
        .replace(',', '')
        .replace('$', '')
        .replace('s', '')
        .strip()
    )


def parse_cash(text: str) -> tuple[float, float]:
    base = text.split('(')[0]
    parts = base.split('+')

    pop_cash = float(clean_number(parts[0]))
    bonus_cash = float(clean_number(parts[1])) if len(parts) > 1 else 0.0

    return pop_cash, bonus_cash


def parse_bloon_text(text: str) -> tuple[str, int]:
    # "Red x 10" -> ["Red", 10]
    if '×' in text:
        name, qty = text.split('×')
        return name.strip(), int(qty.replace(',', '').strip())
    return text.strip(), 1


def parse_round_table(html: bytes):
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', class_='wikitable')
    if table is None:
        raise ValueError("Round table not found")

    rows = table.find('tbody').find_all('tr')

    rounds = []
    spawns = []
    bloons = {}

    bloon_id_counter = 1
    spawn_id_counter = 1

    for row in rows:
        header = row.find('th')
        if not header:
            continue

        text = header.text.strip()
        if not text.isdigit():
            continue

        round_id = int(text)
        # Batasi 140 ronde, tabel sekarang memang sampai 140, tapi kalau nanti tabelnya bertambah jadi tetap berhenti di 140 yak
        if round_id > MAX_ROUND:
            break

        cols = row.find_all('td')
        # Pls kolomnya jangan berubah lagi
        if len(cols) < 6:
            continue

        try:
            duration = float(clean_number(cols[1].text))
            rbe = int(clean_number(cols[2].text))
            pop_cash, bonus_cash = parse_cash(cols[3].text)
            layers = int(clean_number(cols[4].text))
            xp = int(clean_number(cols[5].text))

            rounds.append({
                "round_id": round_id,
                "duration": duration,
                "base_rbe": rbe,
                "pop_cash": pop_cash,
                "bonus_cash": bonus_cash,
                "layers": layers,
                "base_xp": xp
            })

            spans = cols[0].find_all('span', class_='explain')

            for span in spans:
                name, qty = parse_bloon_text(
                    span.get_text(separator=' ', strip=True)
                )

                if name not in bloons:
                    bloons[name] = bloon_id_counter
                    bloon_id_counter += 1

                spawns.append({
                    "spawn_id": spawn_id_counter,
                    "round_id": round_id,
                    "bloon_id": bloons[name],
                    "quantity": qty
                })

                spawn_id_counter += 1

        except ValueError as e:
            logging.warning(f"Skip round {round_id}: {e}")

    bloons_list = [
        {"bloon_id": bid, "bloon_name": name}
        for name, bid in bloons.items()
    ]

    return rounds, spawns, bloons_list


def save_json(data, filename: str):
    base_dir = os.path.dirname(__file__)
    output_path = os.path.join(base_dir, '..', 'data', filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logging.info(f"Saved: {filename}")


def main():
    try:
        html = fetch_html(BASE_URL)
        rounds, spawns, bloons = parse_round_table(html)

        save_json(rounds, 'rounds.json')
        save_json(bloons, 'bloons.json')
        save_json(spawns, 'spawns.json')

        logging.info(f"Done.")

    except Exception as e:
        logging.error(f"Fatal error: {e}")


if __name__ == "__main__":
    main()