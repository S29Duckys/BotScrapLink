import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("URL_SITE_CATALOGUE")


def recup_animes():
    tab_animes = []
    i = 0
    
    while i <= 50:
        input_anime = input("Entrez un animé : ")
        tab_animes.append(input_anime)
        
        if input_anime == "/":
            break

        elif input_anime == "!":
            print(tab_animes)

        i += 1
    print(tab_animes)
    return tab_animes


def verif_saisons(url):
    tab_verif = []

    for i in range(1, 100):
        try:
            url_saisons = f"{url}/saison{i}/vostfr/episodes.js"
            response = requests.head(url_saisons, timeout=(3, 5))

            print(response.status_code)

            if response.status_code == 200:
                print(url_saisons)
                tab_verif.append(url_saisons)
            else:
                break
        
        except requests.Timeout:
            print("La requête a expiré.")

    return tab_verif


def URL_construct():
    tab = recup_animes()
    tab_verif = []

    for element in tab:
        if element == "/" or element == "!" or element =="":
            pass
        else:
            url_transform = f"{url}{element}"
            print(url_transform)
            verif = verif_saisons(url_transform)
            tab_verif.extend(verif)

    return tab_verif       
    
def recup_liens(url):
    print("----------------------------------")
    for element in url:
        try:
            response = requests.get(element, timeout=(3, 5))
            print(response.text)
        except requests.Timeout:
            print("La requête a expiré.")

def main():
    url = URL_construct()
    recup_liens(url)

    


if __name__ == "__main__":    
    main()