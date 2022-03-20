import scoring
import global_vars as g
import statsapi

if __name__=="__main__":
    print("Welcome to MLB-FR data collector.")
    # sample_gamePk = [706907, 706859, 706872, 706820, 706922, 707028, 707009, 707003, 706806, 706942, 706836, 706978, 706792, 706993]
    # print(scoring.score_games(sample_gamePk))
    gamePks = [706907, 706859, 706872, 706820, 706922, 707028, 707009, 707003, 706806, 706942, 706836, 706978, 706792, 706993] # [statsapi.last_game(id) for id in g.id_of_teams]
    scoring.score_games(gamePks)
