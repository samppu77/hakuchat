#!/usr/bin/env python3
"""
Wikipedia-hakutyökalu curlilla ja subprocessilla.
Tekee OpenSearch API -haun ja palauttaa rajatun määrän tuloksia.
"""

import subprocess
import json
import sys


def web_search(query: str, max_results: int = 5) -> list[dict]:
    """
    Hakee Wikipedia OpenSearch API:sta annettuun hakusanaan liittyvät artikkelit.

    Args:
        query: Hakusana tai -lauseke.
        max_results: Palautettavien tulosten maksimimäärä (1–10, oletus 5).

    Returns:
        Lista sanakirjoja, joissa avaimet 'title' ja 'url'.
        Virhetilanteissa palauttaa tyhjän listan.
    """
    # Rajoita max_results turvallisesti välille 1–10
    if max_results < 1:
        max_results = 1
    elif max_results > 10:
        max_results = 10

    # Wikipedia OpenSearch API -URL
    # action=opensearch palauttaa JSON-muodossa: [hakusana, [otsikot], [kuvaukset], [urlit]]
    api_url = "https://en.wikipedia.org/w/api.php"

    # Rakennetaan curl-komento argumenttilistana (ei shell=True)
    # -s = silent, -G = GET-pyyntö, --data-urlencode = URL-enkoodaa parametrit automaattisesti
    # --max-time 10 = curl:in oma aikaraja sekunteina
    cmd = [
        "curl",
        "-s",
        "-G",
        "--max-time", "10",
        "--data-urlencode", f"action=opensearch",
        "--data-urlencode", f"search={query}",
        "--data-urlencode", f"limit={max_results}",
        "--data-urlencode", "namespace=0",
        "--data-urlencode", "format=json",
        api_url
    ]

    try:
        # Suorita curl-komento 10 sekunnin aikarajalla (Pythonin tasolla)
        # capture_output=True palauttaa stdout/stderr, text=True merkkijonona
        result = subprocess.run(
            cmd,
            timeout=10,
            capture_output=True,
            text=True
        )
    except subprocess.TimeoutExpired:
        # Curl tai prosessi ei vastannut ajoissa
        return []
    except FileNotFoundError:
        # curl-komentoa ei löydy järjestelmästä
        return []
    except Exception:
        # Muut odottamattomat virheet prosessin ajossa
        return []

    # Tarkista curl:in paluukoodi (0 = onnistui)
    if result.returncode != 0:
        return []

    # Jäsennä JSON-vastaus
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        # Virheellinen JSON
        return []

    # Wikipedia OpenSearch palauttaa listan: [query, titles[], descriptions[], urls[]]
    # Varmista että rakenne on odotettu
    if not isinstance(data, list) or len(data) < 4:
        return []

    titles = data[1]
    urls = data[3]

    # Yhdistä otsikot ja URL:t sanakirjoiksi
    results = []
    for title, url in zip(titles, urls):
        if isinstance(title, str) and isinstance(url, str):
            results.append({"title": title, "url": url})

    return results


if __name__ == "__main__":
    # Salli komennonriviltä hakusana: python search.py "WSL2 docker" [max_results]
    if len(sys.argv) < 2:
        print("Käyttö: python search.py \"hakusana\" [max_results]")
        sys.exit(1)

    # Yhdistä argumentit hakusanaksi (poista mahdollinen max_results loppusta)
    args = sys.argv[1:]
    max_results = 5

    # Jos viimeinen argumentti on numero, käytä sitä max_resultsina
    if args and args[-1].isdigit():
        max_results = int(args[-1])
        args = args[:-1]

    search_query = " ".join(args)

    # Suorita haku
    results = web_search(search_query, max_results=max_results)

    # Tulosta tulos JSON-muodossa helpolle lukemiselle
    print(json.dumps(results, ensure_ascii=False, indent=2))