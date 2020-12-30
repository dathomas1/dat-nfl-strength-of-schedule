
import random
from flask import Flask, render_template, request, jsonify

# Handles csv conversion and gets lists from that season
from schedule import import_league_schedule_from_csv

# Import functions from Strength of Schedule File
from strengthofschedule import get_all_teams, get_nfl_strength_of_schedule, get_team_wins_and_games

# 2020 NFL Schedule Import
nfl_schedule = import_league_schedule_from_csv("nflschedule.csv")

# All 2020 NFL teams
nfl_teams = get_all_teams(nfl_schedule)

"""
Flask setup
"""

# Create a flask app
app = Flask(
  __name__,
  template_folder="templates",
  static_folder="static"
)
app.config["DEBUG"] = True

# Homepage
@app.route("/", methods=["GET"])
def home():
  return render_template("home.html", teams=nfl_teams)


# Display Strength of Schedule for all teams
@app.route("/all")
def all_nfl_teams():
  teams = []
  for team in nfl_teams:
    nfl_sos = get_nfl_strength_of_schedule(team, nfl_schedule)
    team_record = get_team_wins_and_games(team, nfl_schedule)
    wins = team_record["wins"]
    losses = team_record["losses"]
    ties = team_record["ties"]
    winning_percentage = team_record["win_values"] / team_record["game_count"]
    teams.append({ "team": team.title(), "wins": wins, "losses": losses, "ties": ties,"winning_percentage": winning_percentage, "sos": nfl_sos})

  # Sort teams by Strength of Schedule (lowest to highest)
  teams.sort(key=lambda x: (x.get("winning_percentage"), x.get("sos")))

  return render_template("nfl-sos.html", teams=teams)


# Display Strength of Schedule based on request
@app.route("/api/v1/nfl-team-sos", methods=["GET"])
def api_team_sos():
  if "team" in request.args:
    team = request.args["team"]
    nfl_sos = get_nfl_strength_of_schedule(team, nfl_schedule)
    result = {"team": team.title(), "sos": nfl_sos}
    return jsonify(result)
  else:
    return "Error: could not find the requested team."


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)