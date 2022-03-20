import statsapi
import datetime
import global_vars as g

def get_id_last_games():
    last_games = [statsapi.last_game(id) for id in g.id_of_teams]
    return last_games

def check_date(data: dict):
    """
    This function checks if the current game is within a 24-hour span before the current run. It will be helpful for rest days.
    """
    gameref = data['gameId']
    # Format of gameref is 'YYYY/MM/DD/tm1mlb-tm2mlb-1' so we slice and cast into an integer
    year, month, day = int(gameref[:4]), int(gameref[5:7]), int(gameref[8:10])
    gameday = datetime.datetime(year, month, day)
    now = datetime.datetime.now()
    # Returning true if gameday is between yesterday and now.
    return now-datetime.timedelta(hours=24) <= gameday <= now

def batter_score(player: dict):
    """
    This function computes the score for any batter statistics given as a dictionnary.
    Formula : 1.124 * (2*AB + 5*R + 2*H + 6*RBI + 2*BB - 2*K + 7*HR + 3*SB + 2*2B + 4*3B)
    """
    if not player['id']:
        player_name = player['name']
        ab, r, h, rbi, bb, k, hr, sb, doubles, triples = player['ab'], player['r'], player['h'], player['rbi'], player['bb'], player['k'], player['hr'], player['sb'], player['doubles'], player['triples']
        score = 1.124 * (2*ab + 5*r + 2*h + 6*rbi + 2*bb - 2*k + 7*hr + 3*sb + 2*doubles + 4*triples)
        return [player_name, score]
    return None

def pitcher_score(player: dict):
    """
    This function computes the score for any pitcher statistics given as a dictionnary.
    Formula : W - L + IP - H - 2*R - BB + 4*K + 0.1*P + 0.1*S + (IP>5.3 ? 1 + (R==0 ? 4 : 0) + (H==0 ? 8 : 0) : 0)  
    """
    if not player['id']:
        player_name = player['name']
        w = int('W' in player['note'])
        l = int('L' in player['note'])
        ip, h, r, bb, k, p, s = player['ip'], player['h'], player['r'], player['bb'], player['k'], player['p'], player['s']
        score = w - l + ip - h - 2*r - bb + 4*k + 0.1*p + 0.1*s
        if ip>5.3:
            score+=1
            if not r:
                score+=4
            if not h:
                score+=8
        return [player_name, score]
    return None