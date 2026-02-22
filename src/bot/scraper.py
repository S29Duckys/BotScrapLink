import os
import re
import json
import requests
import yt_dlp
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("URL_SITE_CATALOGUE")
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

LANGUAGES = ["vf", "vostfr", "vo"]
SUPPORTED_PLAYERS = ["sibnet", "vidmoly", "sendvid", "anime-sama"]

def build_urls_from_catalogue(catalogue_file="catalogue.json"):
    episodes_urls = {}

    with open(catalogue_file, "r", encoding="utf-8") as f:
        catalogue = json.load(f)

    print(f"  {len(catalogue)} animés trouvés dans le catalogue")

    for slug, nom in catalogue.items():
        anime_url = f"{BASE_URL}{slug}"
        print(f"\nProcessing : {nom} ({anime_url})")
        result = check_seasons(anime_url)
        if result:
            episodes_urls[slug] = result
        else:
            print(f"  ✗ No valid content for : {nom}")

    return episodes_urls

def get_animes():
    anime_list = []
    print("/ to stop, ! to display the list")

    while True:
        anime_input = input("Anime > ").strip()

        if anime_input == "/":
            break
        elif anime_input == "!":
            print(anime_list)
        elif anime_input == "":
            print("Ignored")
        else:
            anime_list.append(anime_input)

    print(f"List : {anime_list}")
    return anime_list


def detect_player(url):
    for player in SUPPORTED_PLAYERS:
        if player in url:
            return player
    return "unknown"


def check_link(url):
    try:
        response = session.head(url, timeout=(3, 5), allow_redirects=True)
        if response.status_code == 200:
            return True
        response = session.get(url, timeout=(3, 5))
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def parse_episodes_js(content):
    groups = {}
    pattern_vars = r'var\s+(eps\w*)\s*=\s*\['
    variables = re.findall(pattern_vars, content)

    for var in variables:
        pattern_links = rf'var\s+{var}\s*=\s*\[(.*?)\];'
        match = re.search(pattern_links, content, re.DOTALL)
        if match:
            block = match.group(1)
            links = re.findall(r"'(https?://[^']+)'", block)
            if links:
                groups[var] = links

    return groups


def find_best_group(groups):
    for group_name, links in groups.items():
        print(f"    Testing group {group_name} ({detect_player(links[0])})...")
        all_valid = True

        for link in links:
            if not check_link(link):
                print(f"    ✗ Dead link : {link}")
                all_valid = False
                break

        if all_valid:
            print(f"    ✓ Group {group_name} fully valid")
            return {
                "player": detect_player(links[0]),
                "group": group_name,
                "episodes": links
            }
        else:
            print(f"    ✗ Group {group_name} incomplete, moving to next")

    return None


def check_content(content):
    if not content or len(content) < 20:
        return False
    keywords = ["http", "sibnet", "sendvid", "mp4", "m3u8", "embed"]
    return any(keyword in content for keyword in keywords)


def check_seasons(url):
    results = {"vf": [], "vostfr": [], "vo": []}
    print(f"\nChecking seasons for : {url}")

    for i in range(1, 100):
        season_found = False

        for language in LANGUAGES:
            try:
                url_season = f"{url}/saison{i}/{language}/episodes.js"
                response = session.get(url_season, timeout=(3, 5))

                if response.status_code == 200 and check_content(response.text):
                    print(f"  ✓ Season {i} [{language}] found")

                    groups = parse_episodes_js(response.text)
                    best = find_best_group(groups)

                    if best:
                        results[language].append({
                            "season": i,
                            "player": best["player"],
                            "episodes": best["episodes"]
                        })
                        season_found = True
                    else:
                        print(f"  ✗ No working player for season {i} [{language}]")

            except requests.exceptions.RequestException as e:
                print(f"  Error : {e}")

        if not season_found:
            print(f"  Stopping at season {i}")
            break

    return {language: data for language, data in results.items() if data}


def build_urls():
    anime_list = get_animes()
    episodes_urls = {}

    for anime in anime_list:
        anime_url = f"{BASE_URL}{anime}"
        print(f"\nProcessing : {anime_url}")
        result = check_seasons(anime_url)
        if result:
            episodes_urls[anime] = result
        else:
            print(f"  ✗ No valid content for : {anime}")

    return episodes_urls


def export_json(episodes_urls, filename="results.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(episodes_urls, f, ensure_ascii=False, indent=4)
    print(f"\n✓ Exported to {filename}")


def download_from_json(filename="results.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    for anime, languages in data.items():
        for language, seasons in languages.items():
            for season_data in seasons:
                season_num = season_data["season"]
                player = season_data["player"]
                episodes = season_data["episodes"]

                # Folder : downloads/anime-name/season1/
                folder = os.path.join("downloads", anime, f"season{season_num}")
                os.makedirs(folder, exist_ok=True)

                print(f"\nDownloading : {anime} | Season {season_num} | {language.upper()} | {player}")

                options = {
                    "format": "best",
                    "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
                    "http_headers": {
                        "Referer": f"https://{player}.ru" if player != "anime-sama" else "https://anime-sama.fr",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    }
                }

                with yt_dlp.YoutubeDL(options) as ydl:
                    for url in episodes:
                        try:
                            ydl.download([url])
                            print(f"  ✓ Downloaded : {url}")
                        except Exception as e:
                            print(f"  ✗ Error : {url} → {e}")



def main():
    print("═" * 50)
    print("  STEP 1 : Scraping links")
    print("═" * 50)
    episodes_urls = build_urls_from_catalogue()

    if not episodes_urls:
        print("\nNo episodes found.")
        return

    print("\n" + "═" * 50)
    print("  STEP 2 : JSON Export")
    print("═" * 50)
    export_json(episodes_urls)

    print("\n" + "═" * 50)
    print("  STEP 3 : Download")
    print("═" * 50)
    download_from_json()


if __name__ == "__main__":
    main()