# Docker Microservices Demo – Muistiinpanosovellus

Tämä projekti on **mikropalveluarkkitehtuuria** hyödyntävä harjoitustyö, jonka tavoitteena on demonstroida **Dockerin**, **Docker Composen** ja konttien välistä orkestrointia.

Sovellus on yksinkertainen **muistiinpanoalusta**, jossa käyttäjä voi **luoda, lukea ja poistaa muistiinpanoja**. Data säilyy pysyvästi, vaikka kontit sammutettaisiin.

---

## Arkkitehtuuri ja teknologiat

Järjestelmä koostuu kahdesta pääkontista, jotka keskustelevat keskenään Dockerin sisäverkossa.

### 1. Frontend & Reverse Proxy (Nginx)

* **Teknologia:** Nginx (Alpine Linux), HTML5, Vanilla JS, [Pico.css](https://picocss.com)
* **Rooli:** Toimii sovelluksen julkisivuna (portti 80)
* **Toiminnallisuus:**

  * Tarjoilee staattiset sivut käyttäjälle
  * Toimii **reverse proxyna** ja ohjaa `/api/`-alkuiset pyynnöt taustalla olevalle backendille
  * Estää suoran pääsyn backendiin julkisesta verkosta

### 2. Backend (FastAPI)

* **Teknologia:** Python 3.11, FastAPI, Uvicorn
* **Rooli:** REST API (portti 8000, vain sisäverkossa)
* **Toiminnallisuus:**

  * Käsittelee datan (CRUD-operaatiot)
  * Generoi uniikit ID:t (UUID) muistiinpanoille
  * Tallentaa tiedot JSON-muodossa levylle

### Datan pysyvyys (Persistence)

Projektissa käytetään **Docker Volumea**. Backend kirjoittaa tiedot kontin sisäiseen `/data`-kansioon, joka on bind mountattu isäntäkoneen kansioon:

```
./notes-data
```

Data säilyy, vaikka kontit sammutetaan tai rakennetaan uudelleen.

---

## Asennus ja käynnistys

Seuraa näitä ohjeita saadaksesi projektin pystyyn omalla koneellasi.

### Esivaatimukset

* Docker Desktop *(tai Docker Engine + Compose plugin)*
* Git

### 1. Kloonaa repositorio

```bash
git clone https://github.com/idakilpi/docker-microservices-demo.git
cd docker-microservices-demo
```

### 2. Käynnistä sovellus

```bash
docker compose up --build
```

### 3. Avaa sovellus selaimessa

[http://localhost](http://localhost)

---

## Konfiguraatio (valinnainen)

Oletuksena sovellus käyttää porttia **80**. Jos portti on varattu, voit määrittää portit `.env`-tiedostolla projektin juuressa.

### `.env`-esimerkki

```env
FRONTEND_PORT=8080
BACKEND_PORT=8000
```

---

## Projektin rakenne

```
.
├── frontend/             # Frontendin lähdekoodi & Nginx-konfiguraatio
├── notes-api/            # Backendin (FastAPI) lähdekoodi
├── notes-data/           # Pysyvä data (Docker luo automaattisesti)
├── docker-compose.yml    # Koko järjestelmän orkestrointi
└── README.md             # Tämä tiedosto
```

---

