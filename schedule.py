import csv

SCHEDULE_FIELDNAMES = [
  "week",
  "day",
  "date",
  "time",
  "winner_tie",
  "away_team_won",
  "loser_tie",
  "boxscore_or_preview",
  "pts_winner",
  "pts_loser",
  "yards_winner",
  "turnovers_winner",
  "yards_loser",
  "turnovers_loser"
]

def import_league_schedule_from_csv(csv_file_name, csv_fieldnames=SCHEDULE_FIELDNAMES):
  """
  Imports schedule from the Pro-Football-Reference NFL schedule as a dictionary that contains the week, winning team, losing team, winning team's points, and losing team's points.

    Parameters:
      csv_file_name (str): file name of csv

    Returns:
      schedule (array): array containing each csv row as a dictionary 
  """
  schedule = []
  with open(csv_file_name) as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=csv_fieldnames)
    # skip header row of csv 
    next(reader)
    schedule = [row for row in reader]

  return schedule

