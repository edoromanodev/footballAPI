import requests
from bs4 import BeautifulSoup
import html 
import json


leagues = {
    "SerieA": "Serie_A_",
    "SerieB": "Serie_B_",
    "PremierLeague": "Premier_League_",
    "Bundesliga": "Bundesliga_",
    # "PrimeraSpain": "Primera_División_XX_(Spagna)",
    "Ligue1": "Ligue_1_",
    "Eredivisie": "Eredivisie_",
    "PrimeiraLiga": "Primeira_Liga_",
    "ProLeague": "Pro_League_",
    "SuperLig": "Süper_Lig_",
    "ScottishPremiership": "Scottish_Premiership_",
    "RussianLiga": "Prem%27er-Liga_",
    "SuperLeague": "Super_League_",
    "italy": "Serie_A_",
    "england": "Premier_League_",
    "germany": "Bundesliga_",
    "france": "Ligue_1_",
    "netherlands": "Eredivisie_",
    "holland": "Eredivisie_",
    "portugal": "Primeira_Liga_",
    "belgium": "Pro_League_",
    "turkey": "Süper_Lig_",
    "scotland": "Scottish_Premiership_",
    "russia": "Prem%27er-Liga_",
    "swiss": "Super_League_",
}




def get_wikipedia_intro_en(league_key: str, year_start: int, year_end: int) -> dict:
    """
    Fetches the lead section of the Italian Wikipedia page for a given league season.

    Args:
        league_key (str): Key to look up in the leagues dictionary (e.g., 'SerieA', 'italy')
        year_start (int): Start year (e.g., 2022)
        year_end (int): End year (e.g., 2023)

    Returns:
        dict: {
            'success': bool,
            'data': {
                'title': str,
                'html': str,
                'text': str
            } | None,
            'error': str | None
        }
    """
    if league_key not in leagues:
        return {
            "success": False,
            "data": None,
            "error": f"League key '{league_key}' not found in dictionary."
        }

    base_title = leagues[league_key].rstrip("_")  # rimuove eventuale underscore finale
    page_title = f"{base_title}_{year_start}-{year_end}"

    url = "https://it.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "exintro": True,
        "explaintext": False,
        "titles": page_title,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        if not pages:
            return {
                "success": False,
                "data": None,
                "error": "No pages found in the response."
            }

        page = next(iter(pages.values()))
        if "missing" in page:
            return {
                "success": False,
                "data": None,
                "error": f"The page '{page_title}' does not exist on it.wikipedia.org."
            }

        html_extract = page.get("extract", "")
        soup = BeautifulSoup(html_extract, "html.parser")
        plain_text = soup.get_text()

        return {
            "success": True,
            "data": {
                "title": page.get("title"),
                "html": html_extract,
                "text": plain_text
            },
            "error": None
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "data": None,
            "error": f"Request error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"Internal error: {str(e)}"
        }


# Example usage:
#result = get_wikipedia_intro_en("SerieA", 2023, 2024)
# if result["success"]:
#print(result)
# else:
#     print("Error:", result["error"])





def get_infobox_it(league_key: str, year_start: int, year_end: int) -> dict:
    """
    Scrapes the infobox from the Italian Wikipedia page for a given league season.

    Args:
        league_key (str): Key to look up in the leagues dictionary (e.g., 'SerieA', 'italy')
        year_start (int): Season start year
        year_end (int): Season end year

    Returns:
        dict: {
            'success': bool,
            'data': dict | None,
            'error': str | None
        }
    """
    if league_key not in leagues:
        return {
            "success": False,
            "data": None,
            "error": f"League key '{league_key}' not found in dictionary."
        }

    base_title = leagues[league_key].rstrip("_")  # rimuove underscore finale
    page_title = f"{base_title}_{year_start}-{year_end}"
    url = f"https://it.wikipedia.org/wiki/{page_title}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        infobox = soup.find("table", class_="infobox sinottico")

        if not infobox:
            return {
                "success": False,
                "data": None,
                "error": "Infobox not found in the page."
            }

        rows = infobox.find_all("tr")
        result = {}
        current_section = None

        for row in rows:
            if row.find("th", colspan="2"):
                section = row.get_text(strip=True)
                current_section = section
                result[current_section] = {}
            elif row.find("th") and row.find("td"):
                key = row.find("th").get_text(strip=True)
                value = row.find("td").get_text(" ", strip=True)
                if current_section:
                    result[current_section][key] = value
                else:
                    result[key] = value

        return {
            "success": True,
            "data": result,
            "error": None
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "data": None,
            "error": f"Request error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"Parsing error: {str(e)}"
        }


# Example usage
#data = get_serie_a_infobox(2024, 2025)
#if data["success"]:
 #   from pprint import pprint
  #  pprint(data["data"])
#else:
  #  print("Error:", data["error"])

def get_league_teams(league_key: str, year_start: int, year_end: int) -> dict:
    """
    Scrapes the table of participating teams from the Italian Wikipedia page for a given league season.

    Args:
        league_key (str): Key to look up in the leagues dictionary (e.g., 'SerieA', 'portugal')
        year_start (int): Season start year
        year_end (int): Season end year

    Returns:
        dict: {
            'success': bool,
            'data': list[dict] | None,
            'error': str | None
        }
    """
    if league_key not in leagues:
        return {
            "success": False,
            "data": None,
            "error": f"League key '{league_key}' not found in dictionary."
        }

    base_title = leagues[league_key].rstrip("_")
    page_title = f"{base_title}_{year_start}-{year_end}"
    url = f"https://it.wikipedia.org/wiki/{page_title}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        header = soup.find(id="Squadre_partecipanti")
        if not header:
            return {
                "success": False,
                "data": None,
                "error": "Section 'Squadre partecipanti' not found."
            }

        table = header.find_next("table", class_="wikitable")
        if not table:
            return {
                "success": False,
                "data": None,
                "error": "Table not found under 'Squadre partecipanti' section."
            }

        rows = table.find_all("tr")
        headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]
        data = []

        for row in rows[1:]:
            cols = row.find_all(["td", "th"])
            if len(cols) != len(headers):
                continue
            entry = {headers[i]: cols[i].get_text(" ", strip=True) for i in range(len(headers))}
            data.append(entry)

        return {
            "success": True,
            "data": data,
            "error": None
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "data": None,
            "error": f"Request error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"Parsing error: {str(e)}"
        }





def get_live_league_ranking(league_key: str) -> dict:
    import requests
    from bs4 import BeautifulSoup

    leaguesRank = {
        "SerieA": "serie-a",
        "PremierLeague": "Premier-League",
        "Bundesliga": "Bundesliga",
        "Ligue1": "Ligue-1",
        "Eredivisie": "Eredivisie",
        "PrimeiraLiga": "superliga",
        "SuperLig": "campionato-turco",
        "ScottishPremiership": "campionato-scozzese",
        "RussianLiga": "campionato-russo",
        "SuperLeague": "campionato-svizzero",
        "italy": "serie-a",
        "england": "Premier-League",
        "germany": "Bundesliga",
        "france": "Ligue-1",
        "netherlands": "Eredivisie",
        "holland": "Eredivisie",
        "portugal": "superliga",
        "turkey": "campionato-turco",
        "scotland": "campionato-scozzese",
        "russia": "campionato-russo",
        "swiss": "campionato-svizzero",
    }

    if league_key not in leaguesRank:
        return {
            "success": False,
            "data": None,
            "error": f"League key '{league_key}' not found in leaguesRank dictionary."
        }

    path = leaguesRank[league_key]
    url = f"https://www.eurosport.it/calcio/{path}/classifica.shtml"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'data-testid': 'table'})

        if not table:
            return {"success": False, "data": None, "error": "Table not found on page."}

        standings = []
        for row in table.find('tbody').find_all('tr', {'data-testid': 'table-row-data'}):
            cols = row.find_all('td')
            if len(cols) < 10:
                continue  # skip malformed rows

            team_data = {
                "Rank": cols[1].get_text(strip=True),
                "Team": cols[3].get_text(strip=True),   # Wins
                "Match": cols[5].get_text(strip=True),   # Losses
                "Win": cols[6].get_text(strip=True),  # Goals For
                "Draw": cols[7].get_text(strip=True),  # Goals Against
                "Loss": cols[8].get_text(strip=True),  # Goal Difference
                "goals scored": cols[9].get_text(strip=True), # Points
                "goals conceded": cols[10].get_text(strip=True), # Points
                "Goals +/-": cols[11].get_text(strip=True), # Points
                "Points": cols[12].get_text(strip=True), # Points
            }

            standings.append(team_data)

        return {
            'success': True,
            'data': standings,
            'error': None
        }

    except requests.RequestException as e:
        return {'success': False, 'data': None, 'error': f'Request error: {str(e)}'}
    except Exception as e:
        return {'success': False, 'data': None, 'error': f'Parsing error: {str(e)}'}




def scrape_top_scorers(league_key: str, year_start: int, year_end: int) -> dict:
    import requests
    from bs4 import BeautifulSoup
    import html

    leaguesRank = {
        "SerieA": "serie-a",
        "PremierLeague": "Premier-League",
        "Bundesliga": "Bundesliga",
        "Ligue1": "Ligue-1",
        "Eredivisie": "Eredivisie",
        "PrimeiraLiga": "superliga",
        "ScottishPremiership": "campionato-scozzese",
        "RussianLiga": "campionato-russo",
        "SuperLeague": "campionato-svizzero",
        "italy": "serie-a",
        "england": "Premier-League",
        "germany": "Bundesliga",
        "france": "Ligue-1",
        "netherlands": "Eredivisie",
        "holland": "Eredivisie",
        "portugal": "superliga",
        "scotland": "campionato-scozzese",
        "russia": "campionato-russo",
        "swiss": "campionato-svizzero",
    }

    if league_key not in leaguesRank:
        return {
            "success": False,
            "data": None,
            "error": f"League key '{league_key}' not found in leaguesRank dictionary."
        }

    league_path = leaguesRank[league_key]
    url = f"https://www.eurosport.it/calcio/{league_path}/{year_start}-{year_end}/standingperson.shtml"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='standing-table')

        if not table:
            return {
                "success": False,
                "data": None,
                "error": "Top scorers table not found."
            }

        top_scorers = []
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 5:
                position = cols[0].get_text(strip=True)
                cell = cols[1]
                team_span = cell.find('span', class_='team-name')
                if team_span:
                    team_span.decompose()

                player = html.unescape(cell.get_text(strip=True))

                team = html.unescape(cols[2].get_text(strip=True))
                appearances = cols[3].get_text(strip=True)
                goals = cols[4].get_text(strip=True)

                top_scorers.append({
                    "Position": position,
                    "Player": player,
                    "Team": team,
                    "Appearances": appearances,
                    "Goals": goals
                })

        return {
            "success": True,
            "data": top_scorers,
            "error": None
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "data": None,
            "error": f"Request error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"Parsing error: {str(e)}"
        }




def get_league_giornate(league_key, year_start, year_end):
    leagues = {
        "SerieA": "Serie_A_",
        "SerieB": "Serie_B_",
        "PremierLeague": "Premier_League_",
        "Bundesliga": "Bundesliga_",
        "Ligue1": "Ligue_1_",
        "italy": "Serie_A_",
        "england": "Premier_League_",
        "germany": "Bundesliga_",
        "france": "Ligue_1_",
    }

    if league_key not in leagues:
        return json.dumps({
            "success": False,
            "error": f"Chiave lega '{league_key}' non trovata nel dizionario.",
            "data": None
        })

    path = leagues[league_key]
    url = f"https://it.wikipedia.org/wiki/{path}{year_start}-{year_end}#Tabellone"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    giornate = []

    for table in soup.find_all("table", {"width": "99%"}):
        rows = []
        date = ""
        h3_tag = table.find_previous('h3')
        if h3_tag:
            date = h3_tag.get_text(strip=True)

        for tr in table.find_all("tr"):
            cells = tr.find_all(['td', 'th'])

            if len(cells) == 3:
                home_team = cells[0].get_text(strip=True)
                score = cells[1].get_text(strip=True)
                away_team = cells[2].get_text(strip=True)
                match_time = None

                if ':' in home_team:
                    match_time = home_team
                    home_team = "N/A"
                    score = away_team
                    away_team = score.split('-')[0]
                    score = score.split('-')[1] if '-' in score else "-"

                if "-" in away_team and away_team != "":
                    match = {
                        'date': home_team,
                        'match': score,
                        'score': away_team,
                        'match_time': match_time
                    }
                    rows.append(match)

                elif ":" in away_team and away_team != "":
                    match = {
                        'date': home_team,
                        'match': score,
                        'score': "-",
                        'match_time': away_team
                    }
                    rows.append(match)

        giornate.append(rows)

    return json.dumps(giornate, ensure_ascii=False, indent=4)