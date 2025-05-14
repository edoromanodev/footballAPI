# European Football League API

A python API that aggregates football data from various sources including Wikipedia and Eurosport. Designed to support any major European league, it provides structured information on teams, rankings, matchdays, top scorers, and more.

## 🌍 Features

- Retrieve Wikipedia introductions and infoboxes for any supported league and season range.
- Fetch participating teams per season.
- Get current live rankings.
- Retrieve top scorers across seasons.
- Access full matchday schedules.
- Built-in data validation with Pydantic.
- Swagger UI for interactive API documentation.

## 📌 Base URL

```
http://localhost:5000
```

## 📖 API Endpoints

### `GET /intro`
Fetches the introductory section from English Wikipedia.

**Parameters:**
- `league`: League name (e.g., `serie-a`, `premier-league`) *(required)*
- `start`: Start year *(required)*
- `end`: End year *(required)*

### `GET /infobox`
Returns infobox data from Italian Wikipedia.

**Parameters:**
- `league`: League name *(required)*
- `start`: Start year *(required)*
- `end`: End year *(required)*

### `GET /teams`
Lists the teams in a given league for the specified seasons.

**Parameters:**
- `league`: League name *(required)*
- `start`: Start year *(required)*
- `end`: End year *(required)*

### `GET /ranking`
Provides current league standings from Eurosport.

**Parameters:**
- `league`: League name *(required)*

### `GET /scorers`
Top scorers from the selected seasons.

**Parameters:**
- `league`: League name *(required)*
- `start`: Start year *(required)*
- `end`: End year *(required)*

### `GET /giornate`
Full matchday schedule for a league.

**Parameters:**
- `league`: League name *(required)*
- `start`: Start year *(required)*
- `end`: End year *(required)*

## 🧪 API Documentation

Visit [http://localhost:5000/apidocs/](http://localhost:5000/apidocs/) for interactive Swagger UI documentation.

## ⚙️ Installation

### Requirements

- Python 3.7+
- pip

### Setup

```bash
git clone https://github.com/edoromanodev/european-football-api.git
cd european-football-api
pip install -r requirements.txt
python main.py
```

## 🤝 Contributing

1. Fork the repository.
2. Create a branch: `git checkout -b feature-name`.
3. Make your changes and commit: `git commit -am 'Add new feature'`.
4. Push your branch: `git push origin feature-name`.
5. Open a pull request.

## 🪪 License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**Made with ❤️ by Edoardo Romano**
