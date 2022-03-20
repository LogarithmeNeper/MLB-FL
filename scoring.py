import statsapi
import datetime
import csv

def check_date(data: dict):
    """
    This function checks if the current game is within a 24-hour span before the current run. It will be helpful for rest days.
    """
    gameref = data['gameId']
    # Format of gameref is 'YYYY/MM/DD/tm1mlb-tm2mlb-1' so we slice and cast into an integer
    year, month, day = int(gameref[:4]), int(gameref[5:7]), int(gameref[8:10])
    gameday = datetime.datetime(year, month, day)
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # Returning true if gameday is between yesterday and now.
    return now-datetime.timedelta(days=1) <= gameday <= now

def batter_score(player: dict):
    """
    This function computes the score for any batter statistics given as a dictionnary.
    Formula : 1.124 * (2*AB + 5*R + 2*H + 6*RBI + 2*BB - 2*K + 7*HR + 3*SB + 2*2B + 4*3B)
    """
    if player['personId']:
        player_name = player['name']
        ab, r, h, rbi, bb, k, hr, sb, doubles, triples = int(player['ab']), int(player['r']), int(player['h']), int(player['rbi']), int(player['bb']), int(player['k']), int(player['hr']), int(player['sb']), int(player['doubles']), int(player['triples'])
        score = 1.124 * (2*ab + 5*r + 2*h + 6*rbi + 2*bb - 2*k + 7*hr + 3*sb + 2*doubles + 4*triples)
        return [player_name, score]
    return None

def pitcher_score(player: dict):
    """
    This function computes the score for any pitcher statistics given as a dictionnary.
    Formula : W - L + IP - H - 2*R - BB + 4*K + 0.1*P + 0.1*S + (IP>5.3 ? 1 + (R==0 ? 4 : 0) + (H==0 ? 8 : 0) : 0)  
    """
    if player['personId']:
        player_name = player['name']
        w = int('W' in player['note'])
        l = int('L' in player['note'])
        ip, h, r, bb, k, p, s = float(player['ip']), int(player['h']), int(player['r']), int(player['bb']), int(player['k']), int(player['p']), int(player['s'])
        score = w - l + ip - h - 2*r - bb + 4*k + 0.1*p + 0.1*s
        if ip>5.3:
            score+=1
            if not r:
                score+=4
            if not h:
                score+=8
        return [player_name, score]
    return None

def score_game(gamePk: int, out: bool=True):
    """
    Computes the score for each player in the game given as the game id.
    """
    data = statsapi.boxscore_data(gamePk)
    date = data['gameId'][5:10]
    # Checking if the game was played yesterday.
    if check_date(data):
        game_score = [['Team', 'Player', 'Score']]
        # Home team
        home_team = data['teamInfo']['home']['abbreviation']
        # Pitching
        home_pitchers = data['homePitchers']
        for pitcher in home_pitchers:
            score = pitcher_score(pitcher)
            if score is not None:
                game_score.append([home_team] + score)
        # Batting
        home_batters = data['homeBatters']
        for batter in home_batters:
            score = batter_score(batter)
            if score is not None:
                game_score.append([home_team] + score)
        # Away team
        away_team = data['teamInfo']['away']['abbreviation']
        # Pitching
        away_pitchers = data['awayPitchers']
        for pitcher in away_pitchers:
            score = pitcher_score(pitcher)
            if score is not None:
                game_score.append([away_team] + score)
        # Batting
        away_batters = data['awayBatters']
        for batter in away_batters:
            score = batter_score(batter)
            if score is not None:
                game_score.append([away_team] + score)

        # Writing output
        if out:
            path = './output/'
            filename = away_team + '_' + home_team + '_' + date.replace('/', '_') + '.csv'
            with open(path+filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(game_score)

        # Returning as a variable
        return game_score
    return None

def score_games(lst_of_gamePk: list, out: bool=True):
    scores = []
    for gamePk in lst_of_gamePk:
        scores += score_game(gamePk, out)[1:]
    # Raw values game after game
    with open('./output/raw_output.csv', "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(scores)
    # Sorted values
    # Alphabetical on players name
    alphasorted_scores = sorted(scores, key=lambda x: x[1])
    with open('./output/alpha_output.csv', "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(alphasorted_scores)
    # By score
    scoresorted_scores = sorted(scores, key=lambda x: x[2], reverse=True)
    with open('./output/score_output.csv', "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(scoresorted_scores)
    return scores
