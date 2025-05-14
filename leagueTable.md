
# Wikipedia Football Squad Fetcher

This tool allows you to fetch football team squad information from Wikipedia pages for various European leagues.
It supports league-to-country mappings and includes Eurosport availability.

## Supported Leagues

| Key                 | Key2           | League Name (English)        | Wikipedia Title Prefix         | Eurosport Support |
|---------------------|----------------|------------------------------|--------------------------------|--------------------|
| SerieA              | italy          | Serie A (Italy)              | `Serie_A_`                     | ✅ Yes             |
| SerieB              | italy          | Serie B (Italy)              | `Serie_B_`                     | ❌ No              |
| PremierLeague       | england        | Premier League (England)     | `Premier_League_`              | ✅ Yes             |
| Bundesliga          | germany        | Bundesliga (Germany)         | `Bundesliga_`                  | ✅ Yes             |
| Ligue1              | france         | Ligue 1 (France)             | `Ligue_1_`                     | ✅ Yes             |
| Eredivisie          | netherlands    | Eredivisie (Netherlands)     | `Eredivisie_`                  | ✅ Yes             |
| PrimeiraLiga        | portugal       | Primeira Liga (Portugal)     | `Primeira_Liga_`               | ✅ Yes             |
| ProLeague           | belgium        | Belgian Pro League           | `Pro_League_`                  | ✅ Yes             |
| SuperLig            | turkey         | Süper Lig (Turkey)           | `Süper_Lig_`                   | ✅ Yes             |
| ScottishPremiership | scotland       | Scottish Premiership         | `Scottish_Premiership_`        | ✅ Yes             |
| RussianLiga         | russia         | Russian Premier League       | `Prem%27er-Liga_`              | ✅ Yes             |
| SuperLeague         | switzerland    | Swiss Super League           | `Super_League_`                | ✅ Yes             |

## Usage

To fetch a team squad:

```python
import scraping

#api call http://localhost:5000/api/teams?league=italy&start=2022&end=2023

league_key = "SerieA"
start = 2023
end = 2024

squad = fetch_team_squad(league_key, start, end)
```

Make sure to use the proper `league_key` from the table above.

## Notes

- Wikipedia page formats may vary. This tool works best with standard season pages (e.g., `Team_Name_2023–2024`).
- Only leagues with ✅ Eurosport support are guaranteed to match additional Eurosport data if needed.
