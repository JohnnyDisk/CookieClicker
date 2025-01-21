# Cookie Clicker Game

Et web-basert spill bygget med Flask hvor brukere kan konkurrere om å klikke mest på 30 sekunder. Spillet har også en leaderboard-funksjon for å vise de beste spillerne. Dette prosjektet kombinerer backend-funksjonalitet, en responsiv frontend, og enkle animasjoner for å skape en engasjerende opplevelse.

## Funksjonalitet

- **Start Spill:** Brukeren kan starte spillet ved å skrive inn et brukernavn.
- **Klikk:** Klikk på knappen for å samle poeng.
- **CPS (klikk per sekund):** Vis CPS i sanntid, og lagre høyeste CPS.
- **Leaderboard:** Viser en oversikt over spillerne med høyest poengsum, begrenset til maksimalt 600 klikk.
- **Profanity Check:** Filtrerer bort upassende brukernavn ved bruk av `better-profanity`.
- **Responsive Animasjoner:** Interaktive smuler ved knappetrykk for å forbedre brukeropplevelsen.

## Teknologier

- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Profanity filter:** `better-profanity`
- **Statiske filer:** CSS og JS ligger i `static/`-mappen.

## Hvordan kjøre prosjektet

1. **Klon prosjektet fra GitHub:**

   ```bash
   git clone https://github.com/JohnnyDisk/CookieClicker.git
   cd CookieClicker
   ```

2. **Installer avhengigheter:**

   Bruk en virtuell miljø for å holde avhengighetene isolert:

   ```bash
   python -m venv venv
   source venv/bin/activate # For Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Initialiser databasen:**

   Kør scriptet for å opprette nødvendige tabeller i SQLite-databasen:

   ```bash
   python app.py
   ```

   Tabellen `clicks` og `game_state` opprettes automatisk ved oppstart.

4. **Start serveren:**

   ```bash
   flask run
   ```

5. **Åpne nettleseren:**

   Besøk [http://127.0.0.1:5000](http://127.0.0.1:5000) for å spille spillet.

## Endepunkter

### `GET /`

- Returnerer hovedsiden for spillet.

### `POST /start_game`

- Starter et nytt spill.
- Input: JSON med `username`.
- Validerer brukernavnet for upassende innhold.

### `POST /count_clicks`

- Registrerer et klikk.
- Input: JSON med `username`.
- Krever at spillet er aktivt for brukeren.

### `POST /save_click_data`

- Lagrer klikkdata og setter spillet til inaktiv for brukeren.
- Input: JSON med `username`, `count` og `highestCps`.
- Validerer høyeste CPS og upassende brukernavn.

### `GET /leaderboard`

- Returnerer en oversikt over de beste spillerne med maksimal poengsum på 600 klikk.

## Spillregler

1. Hvert spill varer i **30 sekunder**.
2. Maksimal poengsum er **600 klikk**.
3. Brukernavn må være uten støtende språk.

## Eksempelbruk

- **Start et spill:**
  - Gå til hovedsiden, skriv inn brukernavnet ditt og klikk på "Click me!"-knappen.
  - Klikk så raskt du kan for å samle poeng.
- **Leaderboard:**
  - Besøk `/leaderboard` for å se din plassering.

## Mappeoversikt

```
CookieClicker/
├── app.py                # Flask-backend
├── requirements.txt      # Avhengigheter
├── templates/
│   ├── index.html        # Hovedsiden for spillet
│   └── leaderboard.html  # Leaderboard-siden
├── static/
│   ├── styles.css        # CSS-filer
│   └── script.js         # JavaScript-filer
└── click_data.db         # SQLite-database
```

## Videre arbeid

- **Utvidelse av spillfunksjonalitet:**
  - Legge til flere spillmoduser (f.eks. tidsangrep eller presisjonsklikk).
- **Brukerautentisering:**
  - Tillat brukere å opprette kontoer og logge inn.
- **Globalt leaderboard:**
  - Implementer en skyløsning for å vise poengsummer på tvers av deployerte instanser.
- **Optimalisering:**
  - Forbedre ytelsen ved høy trafikk.

## Bidrag

Bidrag er velkomne! Lag en pull request eller opprett en issue dersom du har forslag til forbedringer.

## Lisens

Dette prosjektet er åpen kildekode under [MIT-lisensen](LICENSE).

---

Besøk prosjektet på GitHub: [Cookie Clicker Game](https://github.com/JohnnyDisk/CookieClicker).
