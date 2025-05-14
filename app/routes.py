from flask import Blueprint, jsonify, request
from pydantic import BaseModel, ValidationError, Field

from app.services.scraping import (
    get_wikipedia_intro_en,
    get_infobox_it,
    get_league_teams,
    get_live_league_ranking,
    scrape_top_scorers,
    get_league_giornate
)

bp = Blueprint("api", __name__)


class LeagueSeasonParams(BaseModel):
    league: str = Field(..., min_length=2, max_length=30)
    start: int = Field(..., ge=1990, le=2100)
    end: int = Field(..., ge=1990, le=2100)


class LeagueParam(BaseModel):
    league: str = Field(..., min_length=2, max_length=30)


@bp.route("/intro", methods=["GET"])
def wikipedia_intro():
    """
    Get the introduction of the Serie A season from English Wikipedia
    ---
    parameters:
      - name: league
        in: query
        type: string
        required: true
        description: league name
      - name: start
        in: query
        type: integer
        required: true
        description: Start year of the season
      - name: end
        in: query
        type: integer
        required: true
        description: End year of the season
    responses:
      200:
        description: Intro HTML and text
    """
    try:
        params = LeagueSeasonParams(
            league=request.args.get("league"),
            start=int(request.args.get("start")),
            end=int(request.args.get("end")),
        )
    except (ValidationError, TypeError, ValueError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    
    return jsonify(get_wikipedia_intro_en(params.league,params.start, params.end))


@bp.route("/infobox", methods=["GET"])
def get_infoboxit():
    """
    Get the infobox data for a Serie A season from Italian Wikipedia
    ---
    parameters:
      - name: league
        in: query
        type: string
        required: true
        description: league name
      - name: start
        in: query
        type: integer
        required: true
        description: Start year of the season
      - name: end
        in: query
        type: integer
        required: true
        description: End year of the season
    responses:
      200:
        description: Infobox key data
    """
    try:
        params = LeagueSeasonParams(
            league=request.args.get("league"),
            start=int(request.args.get("start")),
            end=int(request.args.get("end")),
        )
    except (ValidationError, TypeError, ValueError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    

    return jsonify(get_infobox_it(params.league, params.start, params.end))


@bp.route("/teams", methods=["GET"])
def get_league_teams_call():
    """
    Get the list of participating teams for a Serie A season
    ---
    parameters:
      - name: league
        in: query
        type: string
        required: true
        description: league name
      - name: start
        in: query
        type: integer
        required: true
        description: Start year of the season
      - name: end
        in: query
        type: integer
        required: true
        description: End year of the season
    responses:
      200:
        description: List of participating teams
    """
    try:
        params = LeagueSeasonParams(
            league=request.args.get("league"),
            start=int(request.args.get("start")),
            end=int(request.args.get("end")),
        )
    except (ValidationError, TypeError, ValueError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    

    return jsonify(get_league_teams(params.league, params.start, params.end))


@bp.route("/ranking", methods=["GET"])
def ranking():
    """
    Get the current LEAGUE ranking from Eurosport
    ---
    parameters:
      - name: league
        in: query
        type: string
        required: true
        description: league name
    responses:
      200:
        description: Current Serie A standings
    """
    try:
        paramLeague = LeagueParam(
            league=request.args.get("league"),
 
        )

    except (ValidationError, TypeError, ValueError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    

    return jsonify(get_live_league_ranking(paramLeague.league))


@bp.route("/scorers", methods=["GET"])
def top_scorers():
    """
    Get the top scorers of a Serie A season from Eurosport
    ---
    parameters:
      - name: league
        in: query
        type: string
        required: true
        description: league name
      - name: start
        in: query
        type: integer
        required: true
        description: Start year of the season
      - name: end
        in: query
        type: integer
        required: true
        description: End year of the season
    responses:
      200:
        description: List of top scorers
    """
    try:
        params = LeagueSeasonParams(
            league=request.args.get("league"),
            start=int(request.args.get("start")),
            end=int(request.args.get("end")),
        )
    except (ValidationError, TypeError, ValueError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    

    data = scrape_top_scorers(params.league, params.start, params.end)
    return jsonify(data)


@bp.route("/gamedays", methods=["GET"])
def giornate():
    """
    Get the full matchday schedule for a Serie A season from Wikipedia
    ---
    parameters:
      - name: start
        in: query
        type: integer
        required: true
        description: Start year of the season
      - name: end
        in: query
        type: integer
        required: true
        description: End year of the season
    responses:
      200:
        description: JSON with full matchday schedule
    """

    try:
        params = LeagueSeasonParams(
            league=request.args.get("league"),
            start=int(request.args.get("start")),
            end=int(request.args.get("end")),
        )
    except (ValidationError, TypeError, ValueError) as e:
        return jsonify({"success": False, "error": str(e)}), 400
    

    data = get_league_giornate(params.league, params.start, params.end)
    return data  # JSON string
