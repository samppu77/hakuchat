# PROMPTS.md – Hakuchat-projektin OpenCode-promptit

## 1. Projektin alustaminen

**Komento:** `/init`

**Agentin toiminta:** OpenCode tutki projektikansion ja loi AGENTS.md-tiedoston, joka sisälsi ohjeita projektin rakenteesta, käynnistämisestä ja ympäristömuuttujista.

## 2. weather.py:n toiminnan selittäminen

**Prompti:**

Lue weather.py ja selitä lyhyesti suomeksi, mitä ohjelma tekee. Kerro myös, miten tool_calls toimii tässä esimerkissä. Älä muokkaa mitään tiedostoja.

**Agentin toiminta:** Agentti selitti, miten Python-ohjelma lähettää kysymyksen Nemotronille ja miten kielimalli voi pyytää työkalukutsua. Agentti huomautti, ettei weather.py vielä suorita työkalua, vaan ainoastaan tulostaa pyydetyn funktion ja argumentit.

## 3. AGENTS.md:n tietoturvaohjeet

**Promptin keskeinen sisältö:**

Täydennä olemassa olevaa AGENTS.md-tiedostoa hakuchat-projektin säännöillä. Käytä API-avainta ympäristömuuttujasta, suorita curl-komennot ilman shell=True-asetusta, rajaa työkalusilmukka viiteen kierrokseen ja noudata tietoturvavaatimuksia. Muokkaa vain AGENTS.md-tiedostoa.

**Agentin toiminta:** Agentti lisäsi tiedostoon kymmenen projektisääntöä ja säilytti vanhat ohjeet. Se huomasi myös ristiriidan weather.py:n ja uuden sovelluksen API-avaimen ympäristömuuttujien nimissä.

## 4. Sovelluksen suunnittelu Plan-agentilla

**Promptin keskeinen sisältö:**

Lue weather.py ja AGENTS.md. Suunnittele Pythonilla toteutettava hakuchat-verkkosovellus, jossa on Flask-palvelin, HTML-käyttöliittymä ja curlilla toimiva web_search-työkalu. Listaa tarvittavat tiedostot, funktiot ja toteutusjärjestys. Älä vielä kirjoita koodia.

**Agentin toiminta:** Agentti loi suunnitelman, jossa olivat Flask-palvelin, verkkohaku, kielimalliyhteys ja keskusteluhistoria. Suunnitelmassa oli kuitenkin aluksi väärä tiedostorakenne ja rajapinnan osoite.

## 5. Suunnitelman korjaaminen

**Promptin keskeinen sisältö:**

Korjaa suunnitelma vastaamaan opettajan tehtävänantoa. Erota sovellus tiedostoihin search.py, chat_core.py, app.py ja index.html. Toteuta ensin verkkohaku, sitten tool use -silmukka ja lopuksi Flask-palvelin sekä käyttöliittymä. Käytä POST /api/chat -rajapintaa.

**Agentin toiminta:** Agentti teki uuden suunnitelman, jossa ohjelma jaettiin pieniin testattaviin kokonaisuuksiin.

## 6. search.py:n toteuttaminen

**Promptin keskeinen sisältö:**

Toteuta search.py, jossa on web_search(query, max_results=5). Käytä Wikipedian OpenSearch API:a, curlia ja subprocess.run-kutsua ilman shell=True-asetusta. Lisää aikaraja, virheenkäsittely ja komentorivitesti.

**Agentin toiminta:** Agentti loi search.py-tiedoston ja testasi sitä. Wikipedia-haku palautti otsikoita ja URL-osoitteita. Komentoinjektiotestissä ei syntynyt ylimääräistä tiedostoa.

## 7. chat_core.py:n toteuttaminen

**Promptin keskeinen sisältö:**

Toteuta chat_core.py, joka käyttää OpenRouteria ja Nemotronia. Määrittele web_search-työkalu ja toteuta enintään viiden kierroksen tool use -silmukka. Säilytä keskusteluhistoria ja käsittele API-virheet sekä virheelliset työkalukutsut.

**Agentin toiminta:** Agentti loi chat_core.py-tiedoston. Nemotron vastasi tavalliseen kysymykseen, mutta verkkohakutestissä työkalusilmukka saavutti viiden kierroksen rajan.

## 8. Hakusilmukan ongelman korjaaminen

**Promptin keskeinen sisältö:**

Korjaa chat_core.py:n ongelma, jossa Nemotron kutsuu web_search-työkalua viisi kertaa ilman hakutuloksia. Ohjeista mallia käyttämään lyhyempiä hakusanoja, estä toistuvat haut ja lisää selkeä virheenkäsittely sekä lokitus.

**Agentin toiminta:** Agentti muokkasi chat_core.py- ja search.py-tiedostoja. Se lisäsi hakusanojen käsittelyä, toistuvien hakujen tunnistamista ja lokitusta.

Korjattua toteutusta ei kuitenkaan voitu testata loppuun asti, koska OpenRouter palautti myöhemmin HTTP 429 -käyttörajavirheen.

## Yhteenveto

OpenCode auttoi projektin suunnittelussa, koodin kirjoittamisessa ja virheiden korjaamisessa. Käytin agenttia pienissä vaiheissa ja testasin toimintoja ennen seuraavaan vaiheeseen siirtymistä.

Suurin ongelma liittyi verkkohakua käyttävään työkalusilmukkaan. Lisäksi ilmaisen kielimallin käyttörajoitus esti lopullisen testauksen.

Projektin Flask-palvelin ja selainkäyttöliittymä toteutettiin tämän jälkeen erikseen ilman OpenCodea.
