import scoring
import global_vars as g
import statsapi

if __name__=="__main__":
    print("Welcome to MLB-FR data collector.")
    gamePks = [statsapi.last_game(id) for id in g.id_of_teams]
    scoring.score_games(gamePks)
