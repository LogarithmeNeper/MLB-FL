import pybaseball
import statsapi
import global_vars as g

# Example game : 706907

def get_id_last_games():
    last_games = [statsapi.last_game(id) for id in g.id_of_teams]
    return last_games   