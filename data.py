import pybaseball
import statsapi
import global_vars as g

def lookup():
    for team in g.list_of_teams:
        print(team, statsapi.lookup_team(team)[0]['id'])