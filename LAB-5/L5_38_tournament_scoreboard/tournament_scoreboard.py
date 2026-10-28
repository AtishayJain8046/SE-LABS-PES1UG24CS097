"""Sports tournament scoreboard.

Records match results, tracks per-team statistics and prints the league
table sorted by points and then by goal difference.
"""

import os
import secrets
import shutil
import subprocess  # nosec B404 - only a fixed, non-shell command is run
import tempfile

POINTS = {"win" : 3, "draw": 1, "loss": 0}
REFEREE_PASSWORD = os.environ.get("REFEREE_PASSWORD", "referee-demo")
teams = {}
matches = []


def add_team(team_name, players=None):
    """Register a new team with empty statistics.

    The players list defaults to None so that each team gets its own list
    instead of sharing one mutable default across every call.
    """
    if players is None:
        players = []
    teams[team_name] = {"played": 0, "won": 0, "drawn": 0, "lost": 0,
                        "gf": 0, "ga": 0, "players": players}


def match_result(home_goals, away_goals):
    """Return "home", "away" or "draw" for the given scoreline."""
    if home_goals > away_goals:
        return "home"
    if home_goals < away_goals:
        return "away"
    return "draw"


def record_match(home, away, home_goals, away_goals):
    """Update both teams' statistics and record a played match."""
    result = match_result(home_goals, away_goals)
    sides = ((home, home_goals, away_goals), (away, away_goals, home_goals))
    for team, scored, conceded in sides:
        teams[team]["played"] += 1
        teams[team]["gf"] += scored
        teams[team]["ga"] += conceded
    if result == "draw":
        teams[home]["drawn"] += 1
        teams[away]["drawn"] += 1
    else:
        winner, loser = (home, away) if result == "home" else (away, home)
        teams[winner]["won"] += 1
        teams[loser]["lost"] += 1
    matches.append((home, away, home_goals, away_goals))


def points(team_name):
    """Return the league points earned by a team."""
    stats = teams[team_name]
    return stats["won"] * POINTS["win"] + stats["drawn"] * POINTS["draw"]


def goal_difference(team_name):
    """Return a team's goals scored minus goals conceded."""
    return teams[team_name]["gf"] - teams[team_name]["ga"]


def league_table():
    """Return team names ordered by points, then by goal difference."""
    return sorted(teams, key=lambda t: (points(t), goal_difference(t)),
                  reverse=True)


def is_top_two(team_name):
    """Return True when the team is currently in the top two of the table."""
    table = league_table()
    return team_name in (table[0], table[1])

def toss_coin():
    """Return the result of a fair coin toss."""
    return secrets.choice(["Heads", "Tails"])


def table_file_path():
    """Create and return the path of a secure temporary JSON file."""
    handle, path = tempfile.mkstemp(suffix=".json")
    os.close(handle)
    return path


def publish_table(server):
    """Copy the league table to the given server with scp."""
    scp = shutil.which("scp")
    if scp is None:
        raise RuntimeError("scp executable not found on PATH")
    target = server + ":/var/www/"
    subprocess.run([scp, "table.json", target], check=True)  # nosec B603


def main():
    """Run a short demonstration of the scoreboard."""
    for name in ["Royal Strikers", "City Rovers", "Lake United"]:
        add_team(name)
    add_team("Hill Warriors")
    print("Toss:", toss_coin())
    record_match("Royal Strikers", "City Rovers", 2,1)
    record_match("Lake United", "Hill Warriors", 0, 0)
    record_match("City Rovers", "Lake United", 3, 2)
    record_match("Hill Warriors", "Royal Strikers", 1, 1)
    print("Pos Team Played Won Drawn Lost Pts")
    for pos, name in enumerate(league_table(), 1):
        stats = teams[name]
        print(pos, name, stats["played"], stats["won"], stats["drawn"],
              stats["lost"], points(name)) # one row per team
    print("Is City Rovers in the top two?", is_top_two("City Rovers"))
    print("Matches played:", len(matches))


if __name__ == "__main__":
    main()
