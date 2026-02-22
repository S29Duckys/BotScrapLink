import re
import json
import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})


def get_anime_slug(url):
    match = re.search(r'/catalogue/([^/]+)', url)
    return match.group(1) if match else None


def scrape_catalogue():
    animes = {}
    page = 1

    while True:
        print(f"Scraping page {page}...")

        url = f"https://anime-sama.tv/catalogue/?page={page}"
        response = session.get(url, timeout=(3, 5))

        if response.status_code != 200:
            print(f"  ✗ Erreur {response.status_code}, arrêt")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        titres = soup.find_all("h2", class_="card-title")

        if not titres:
            print(f"  Aucun animé trouvé page {page}, arrêt")
            break

        for titre in titres:
            nom = titre.get_text(strip=True)
            lien = titre.find_parent("a")
            href = lien["href"] if lien else None
            slug = get_anime_slug(href) if href else None

            if nom and slug:
                animes[slug] = nom
                print(f"  ✓ {nom} → {slug}")

        print(f"  Page {page} terminée : {len(titres)} animés trouvés")
        page += 1

    return animes


def export_json(data, filename="catalogue.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"\n✓ {len(data)} animés exportés dans {filename}")


def main():
    print("═" * 50)
    print("  Scraping du catalogue Anime-sama")
    print("═" * 50)

    animes = scrape_catalogue()

    if not animes:
        print("Aucun animé trouvé.")
        return

    export_json(animes)


if __name__ == "__main__":
    main()