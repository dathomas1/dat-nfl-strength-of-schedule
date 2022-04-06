# Constants for value of win, loss, and ties
WON_GAME_VALUE = 1.0 
LOST_GAME_VALUE = 0.0
TIE_GAME_VALUE = 0.5

# Constants for Strength of Schedule calculations
OPPONENT_RECORD_WEIGHT = 2.0
OPPONENT_OPPONENT_RECORD_WEIGHT = 1.0


def get_all_teams(league_schedule):
  """
  Returns an array of all teams that are scheduled to play a game

  Parameters:
    league_schedule (array): array containing dictionary of games

  Returns:
    teams (array): array of team names sorted A to Z
  """
  teams = set()

  # Add the winner and loser of each game to team set. Skip if empty
  for game in league_schedule:
    if game["winner_tie"]:
      teams.add(game["winner_tie"])
    if game["loser_tie"]:
      teams.add(game["loser_tie"])

  return sorted(teams)

def get_team_schedule(team, league_schedule):
  """
  Returns array of games based on team

    Parameters:
      team (str): string to represent team
      league_schedule (array): array containing dictionary of games

    Returns:
      team_schedule (array): array containing games only played by a particular team
  """
  team_schedule = []

  # Build array of games played by the requested team
  for game in league_schedule: 
      if (game["winner_tie"].lower() == team.lower() or 
      game["loser_tie"].lower() == team.lower()):
        team_schedule.append(game)

  return team_schedule


def get_win_loss_tie_value(game, team):
  """
  Determines if a game was won, lost, or tied by a particular. Then returns appropriate value.

    Parameters:
      game (dict): dictionary representing a game between two teams
      team (str): string of the particular team

    Returns:
      game_value (float): appropriate value based on whether the team won, lost, or tied.
  """
  
  # Check if game was a tie
  if int(game["pts_winner"]) == int(game["pts_loser"]):
    return TIE_GAME_VALUE
  elif game["winner_tie"].lower() == team.lower():
    return WON_GAME_VALUE
  else:
    return LOST_GAME_VALUE


def get_opposing_team(game, team):
  """
  Get the opposing team of a particular team from a game

  Parameters:
    game (dict): represents a game between two teams
    team (str): team of interest

  Return:
    opposing_team (str): team that played against the particular team of interest
  """

  # Check if a team is a winner or loser, then return the opposite team
  if game["winner_tie"].lower() == team.lower():
    return game["loser_tie"]
  elif game["loser_tie"].lower() == team.lower():
    return game["winner_tie"]
  else:
    return None


def get_opposing_team_list(team, schedule, played_games_only=True, is_full_league_schedule=True):
  """
  Returns a list of opposing teams that a particular team played against.

  Parameters:
    team (str): string of the particular team
    schedule (array): contains list of league games
    played_games_only (bool): True to only find opponents of actually played games. False to include future opponents
    is_full_league_schedule (bool): True if the supplied schedule is the full league schedule. False if this is the specified team schedule only

  Return:
    opposing_teams (list): list of opposing teams. Duplicates are expected.
  """
  opposing_teams = []
  
  # Get team schedule in case full league schedule is supplied.
  if is_full_league_schedule:
    team_schedule = get_team_schedule(team, schedule)
  else:
    team_schedule = schedule

  for game in team_schedule:
    # If played games is True, then only add opponents that have been played
    if played_games_only:
      if game["pts_winner"] and game["pts_loser"]:
        opposing_team = get_opposing_team(game, team)
        opposing_teams.append(opposing_team)
      else:
        continue
    else:
      opposing_team = get_opposing_team(game, team)
      opposing_teams.append(opposing_team)

  return opposing_teams


def get_unique_opposing_teams(team, schedule, played_games_only=True, is_full_league_schedule=True):
  """
  Returns a list of opposing teams that a particular team played against.

  Parameters:
    team (str): string of the particular team
    schedule (array): contains list of league games
    played_games_only (bool): True to only find opponents of actually played games. False to include future opponents
    is_full_league_schedule (bool): True if the supplied schedule is the full league schedule. False if this is the specified team schedule only

  Return:
    opposing_teams (set): set of opposing teams
  """
  opposing_teams = set()
  
  # Get team schedule in case full league schedule is supplied.
  if is_full_league_schedule:
    team_schedule = get_team_schedule(team, schedule)
  else:
    team_schedule = schedule

  for game in team_schedule:
    # If played games is True, then only add opponents that have been played
    if played_games_only:
      if game["pts_winner"] and game["pts_loser"]:
        opposing_team = get_opposing_team(game, team)
        opposing_teams.add(opposing_team)
      else:
        continue
    else:
      opposing_team = get_opposing_team(game, team)
      opposing_teams.add(opposing_team)

  return opposing_teams

# TODO: Change function name to get_team_record
def get_team_wins_and_games(team, schedule, omit_games_against=[], is_full_league_schedule=True):
  """
  Returns an object with the amount of wins and total games. This can be used to calculate winning percentage. This function includes an optional parameter to exclude games against certain teams. This is useful for strength of schedule calculations. See www.nationalchamps.net/NCAA/BCS/strength_of_schedule_explain.htm

  Parameters:
    team (str): string of the particular team
    schedule (array): contains list of league games
    omit_games_against (array): list of teams to exclude the game results
    is_full_league_schedule (bool): True if the supplied schedule is the full league schedule. False if this is the specified team schedule only.
    played_games_only (bool): True to only find opponents of actually played games. False to include future opponents

  Return:
    {win_values, game_count, wins, losses, ties} (dict): represents the amount of wins and a total of all eligible games 
  """
  # Count of eligible games without excluded teams
  game_count = 0.0

  # Total amount of value from wins and ties
  win_values = 0.0

  # Total amount of games won
  wins = 0

  # Total amount of games tied
  ties = 0

  # Total amount of games lost
  losses = 0

  # Convert all items in omit games list to lowercase to help with string checks
  omit_games_against_lower = [item.lower() for item in omit_games_against]

  # Get team schedule in case full league schedule is supplied.
  if is_full_league_schedule:
    team_schedule = get_team_schedule(team, schedule)
  else:
    team_schedule = schedule

  for game in team_schedule:
    # Skip games against excluded opponents
    if get_opposing_team(game, team).lower() in omit_games_against_lower:
      continue
    # Check if game has score then determine win value
    elif game["pts_winner"] and game["pts_loser"]:
      game_count += 1.0
      game_win_value = get_win_loss_tie_value(game, team)
      win_values += game_win_value
      if game_win_value == WON_GAME_VALUE:
        wins += 1
      elif game_win_value == TIE_GAME_VALUE:
        ties += 1
      else:
        losses += 1

    # Something unexpected happened, so continue to next item
    else:
      continue
  
  # Check if team played any eligible games to avoid 0 division
  if game_count > 0:
    return { "win_values": win_values, "game_count": game_count, "wins": wins, "losses": losses, "ties": ties}
  else:
    return None


def get_opponent_record(team, league_schedule, team_opponents=None, played_games_only=False):
  """
  Get combined record of a team's opponents. The opponents winning record doesn't include the head-to-head games of the requested team.

  Parameters:
    team (str): string of the particular team
    league_schedule (array): contains list of league games
    is_full_league_schedule (bool): True if the supplied schedule is the full league schedule. False if this is the specified team schedule only.

  Return:
    {win_values, game_count} (dict): opponents record of all eligible games
  """
  # Count of eligible games without excluded teams
  opponent_game_count = 0.0

  # Total amount of value from wins and ties
  opponent_win_values = 0.0

  if team_opponents:
    opponents = team_opponents
  else:
    # TODO: flag if unique opponents only
    # Get team schedule and use to get opponents
    team_schedule = get_team_schedule(team, league_schedule)
    opponents = get_unique_opposing_teams(team, team_schedule, played_games_only,is_full_league_schedule=False)

  # Get the cumulative wins and total games of a team's opponents
  for opponent in opponents:
    wins_and_total_games = get_team_wins_and_games(opponent, league_schedule, omit_games_against=[team])

    opponent_game_count += wins_and_total_games["game_count"]
    opponent_win_values += wins_and_total_games["win_values"]

  # Check if team played any eligible games to avoid 0 division
  if opponent_game_count > 0:
    return { "win_values": opponent_win_values, "game_count": opponent_game_count}
  else:
    return None


#TODO: combine nfl method with college
def get_nfl_opponent_record(team, league_schedule, team_opponents=None, played_games_only=False):
  """
  Get combined record of a team's opponents. The opponents winning record doesn't include the head-to-head games of the requested team.

  Parameters:
    team (str): string of the particular team
    league_schedule (array): contains list of league games
    is_full_league_schedule (bool): True if the supplied schedule is the full league schedule. False if this is the specified team schedule only.

  Return:
    {win_values, game_count} (dict): opponents record of all eligible games
  """
  # Count of eligible games without excluded teams
  opponent_game_count = 0.0

  # Total amount of value from wins and ties
  opponent_win_values = 0.0

  if team_opponents:
    opponents = team_opponents
  else:
    # TODO: flag if unique opponents only
    # Get team schedule and use to get opponents
    team_schedule = get_team_schedule(team, league_schedule)
    opponents = get_opposing_team_list(team, team_schedule, played_games_only,is_full_league_schedule=False)

  # Get the cumulative wins and total games of a team's opponents
  for opponent in opponents:
    wins_and_total_games = get_team_wins_and_games(opponent, league_schedule)

    opponent_game_count += wins_and_total_games["game_count"]
    opponent_win_values += wins_and_total_games["win_values"]

  # Check if team played any eligible games to avoid 0 division
  if opponent_game_count > 0:
    return { "win_values": opponent_win_values, "game_count": opponent_game_count}
  else:
    return None


# TODO: pass played games only flag down and add omit wins against team list
def get_college_strength_of_schedule(team, league_schedule, played_games_only=False):
  opponent_opponent_game_count = 0.0
  opponent_opponent_win_values = 0.0
  
  opponents = get_unique_opposing_teams(team, league_schedule, played_games_only)

  opponent_record = get_opponent_record(team, league_schedule, opponents)

  for opponent in opponents:
    opponent_opponent_record = get_opponent_record(opponent, league_schedule)
    opponent_opponent_game_count += opponent_opponent_record["game_count"]
    opponent_opponent_win_values += opponent_opponent_record["win_values"]
  
  opponent_win_percentage = opponent_record["win_values"] / opponent_record["game_count"]

  opponent_opponent_win_percentage = opponent_opponent_win_values / opponent_opponent_game_count
  
  return (OPPONENT_RECORD_WEIGHT * opponent_win_percentage + OPPONENT_OPPONENT_RECORD_WEIGHT * opponent_opponent_win_percentage) / (OPPONENT_RECORD_WEIGHT + OPPONENT_OPPONENT_RECORD_WEIGHT)
    

# TODO: pass played games only flag down
def get_nfl_strength_of_schedule(team, league_schedule, played_games_only=False):
  
  opponents = get_opposing_team_list(team, league_schedule, played_games_only)

  opponent_record = get_nfl_opponent_record(team, league_schedule, opponents)

  opponent_win_percentage = opponent_record["win_values"] / opponent_record["game_count"]

  return opponent_win_percentage