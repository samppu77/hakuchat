# Hakuchat – OpenCode + Nemotron

## Projektin kuvaus

Tämän projektin tarkoituksena oli rakentaa selaimessa toimiva tekoälychat OpenCode-koodausagentin avulla. Sovellus käyttää Pythonia, Flaskia, OpenRouteria ja NVIDIA Nemotron -kielimallia.

Kielimalli pystyy päättämään, tarvitseeko käyttäjän kysymykseen vastaaminen verkkohakua. Verkkohaku toteutetaan Pythonin `subprocess.run`-funktion ja `curl`-komennon avulla.

Sovellukseen kuuluu myös selainkäyttöliittymä, jossa käyttäjä voi kirjoittaa viestejä, tarkastella keskusteluhistoriaa ja nähdä kielimallin tekemät haut.

## Projektin tiedostot

- `app.py` – Flask-palvelin ja chat-rajapinta.
- `chat_core.py` – Nemotron-yhteys ja tool use -silmukka.
- `search.py` – Wikipedia-verkkohaku curlilla.
- `templates/index.html` – chatin selainkäyttöliittymä.
- `weather.py` – tehtävän pohjana käytetty esimerkkitiedosto.
- `AGENTS.md` – OpenCode-agentin projektiohjeet.
- `PROMPTS.md` – projektissa käytetyt tärkeimmät promptit.
- `requirements.txt` – Python-riippuvuudet.

## Asennus ja käynnistäminen

Projekti on toteutettu WSL2 Ubuntu -ympäristössä.

Siirry projektikansioon:

```bash
cd ~/projektit/hakuchat
```

Luo ja aktivoi Python-virtuaaliympäristö:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Asenna tarvittavat kirjastot:

```bash
pip install -r requirements.txt
```

Varsinaisen kielimallin käyttö edellyttää OpenRouterin API-avainta, joka asetetaan ympäristömuuttujaan `OPENROUTER_API_KEY`.

Käynnistä sovellus:

```bash
python app.py
```

Avaa selaimessa:

`http://127.0.0.1:5000`

Sovelluksen käyttöliittymää voi testata ilman kielimallia komennolla:

```bash
MOCK_MODE=1 python app.py
```

Tässä tilassa sovellus palauttaa testivastauksia eikä tee OpenRouterin API-kutsuja.

## Tool use -silmukan toiminta

Kun käyttäjä lähettää kysymyksen, se välitetään Flask-palvelimen kautta `chat_core.py`-tiedostolle. Ohjelma lähettää keskusteluhistorian ja käytettävissä olevan `web_search`-työkalun kuvauksen Nemotron-kielimallille.

Kielimalli päättää kysymyksen perusteella, tarvitseeko se verkkohakua. Jos hakua ei tarvita, se voi vastata suoraan käyttäjälle.

Jos malli pyytää verkkohakua, ohjelma lukee mallin palauttaman `tool_calls`-tiedon. Tämän perusteella Python suorittaa `search.py`-tiedoston `web_search`-funktion, joka hakee tietoa Wikipedian haku-API:sta curlilla.

Haun tulokset palautetaan kielimallille JSON-muodossa, minkä jälkeen mallia kutsutaan uudelleen. Työkalusilmukassa on enintään viisi kierrosta, jotta ohjelma ei jää hakemaan loputtomasti.

Kielimalli ei siis suorita curl-komentoa itse, vaan Python-ohjelma suorittaa sen mallin pyynnöstä.

## Tietoturva

Projektissa huomioitiin seuraavat tietoturva-asiat:

- API-avain luetaan ympäristömuuttujasta eikä sitä tallenneta lähdekoodiin.
- `.gitignore` estää `.env`- ja `.venv`-tiedostojen lisäämisen Git-versionhallintaan.
- `subprocess.run` käyttää argumenttilistaa ilman `shell=True`-asetusta.
- Curl-kutsuille on asetettu aikaraja.
- Hakutuloksia käsitellään epäluotettavana tietona.
- Työkalusilmukan kierrosmäärä on rajattu viiteen.
- Flask-palvelin kuuntelee vain osoitetta `127.0.0.1`.

Komentoinjektiota testattiin hakusanalla `test; touch /tmp/hakkeroitu`. Testin jälkeen tarkistettiin, ettei `/tmp/hakkeroitu`-tiedostoa ollut syntynyt.

## Testaus ja rajoitukset

Projektin aikana Wikipedia-verkkohaku testattiin onnistuneesti erillisenä Python-toimintona. Hakufunktio palautti Wikipedia-artikkeleiden otsikoita ja URL-osoitteita.

Nemotron-kielimalli vastasi myös onnistuneesti tavalliseen kysymykseen Python-ohjelmointikielestä.

Verkkohakua vaativassa testissä kielimalli teki viisi hakukutsua, mutta käytetyt hakusanat eivät tuottaneet tuloksia. Tämän vuoksi työkalusilmukan enimmäiskierrosmäärä tuli vastaan.

Korjasin agentin avulla hakusanojen käsittelyä, toistuvien hakujen estämistä ja virheenkäsittelyä.

Korjausten jälkeen OpenRouter palautti HTTP 429 -virheen (`RateLimitError`). Käyttörajoituksen vuoksi en pystynyt testaamaan korjattua tool use -silmukkaa loppuun asti oikealla kielimallilla.

Flask-palvelinta ja selainkäyttöliittymää testattiin erikseen `MOCK_MODE=1`-tilassa. Palvelimen `/api/chat`- ja `/api/history`-rajapinnat palauttivat HTTP 200 -vastauksia.

Mock-tilan onnistuminen ei kuitenkaan tarkoita, että Nemotronin lopullinen verkkohakutoiminto olisi vahvistettu toimivaksi.

## Omat johtopäätökset ja reflektio

Tämän tehtävän aikana opin käyttämään OpenCode-koodausagenttia ohjelmointiprojektin suunnitteluun ja toteuttamiseen. Aluksi asensin WSL2 Ubuntu -ympäristön ja OpenCoden sekä yhdistin agentin OpenRouteriin. Tämän jälkeen aloin rakentaa sovellusta pienissä vaiheissa.

Agentin käyttäminen helpotti ohjelmointia, koska minun ei tarvinnut kirjoittaa kaikkea koodia itse. Huomasin kuitenkin, että tekoälyn tekemää koodia pitää testata ja tarkistaa. Esimerkiksi ensimmäinen suunnitelma ei vastannut täysin tehtävänantoa, joten pyysin agenttia korjaamaan tiedostorakenteen ja toteutusjärjestyksen.

Yksi suurimmista ongelmista tuli vastaan työkalusilmukassa. Nemotron yritti käyttää verkkohakua useita kertoja, mutta hakusanat eivät tuottaneet tuloksia. Ohjelma saavutti viiden kierroksen rajan eikä pystynyt muodostamaan lopullista vastausta. Korjasin ongelmaa ohjaamalla agenttia tekemään lyhyempiä hakukyselyitä ja estämään samojen hakujen toistumista.

Myöhemmin OpenRouterin käyttöraja tuli vastaan, ja sain HTTP 429 -virheen. Tämä esti korjatun toiminnon lopullisen testaamisen. Jatkoin kuitenkin projektin muiden osien rakentamista ja testasin Flask-palvelinta ilman kielimallia.

Ymmärrän nyt paremmin, miten kielimallin työkalukutsut toimivat. Malli ei suorita verkkohakua itse, vaan Python-ohjelma vastaanottaa työkalupyynnön, suorittaa haun ja palauttaa tulokset mallille.

Vaikeimmaksi osaksi koin työkalusilmukan keskusteluhistorian käsittelyn, erityisesti `tool_call_id`-tunnisteiden käytön. Tätä voisin oppia paremmin tutkimalla koodia rivi riviltä ja tekemällä lisää testejä.

Agentin käyttäminen nopeutti projektin rakentamista, mutta opin myös, ettei tekoälyn tuottamaan koodiin voi luottaa ilman testaamista. Jatkossa käyttäisin samaa vaiheittaista työskentelytapaa ja varmistaisin jokaisen toiminnon ennen seuraavaan siirtymistä.
