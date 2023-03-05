import requests # request API 
import json # read from API
from steam import game_servers as gs # so we can make A2S requests

url = 'https://nanny.cfcservers.org/cfc3-status'

def get_a2s_info(server): 
    try: # this can fail, completely up to the server
        players = gs.a2s_players(server)
        scores = {}
        for ply in players:
            scores[ply['name']] = ply['score']
        return scores
    except:
        print("Server A2S error, i'm sure it's fine") 
        pass # We can pass here, if this doesn't return, Score is simply excluded from the formatted list.
         

def get_player_info():
    r = requests.get(url)
    if r.ok:
        return json.loads(r.text)
    #error handling is for loosers. jk tho if this is down we're screwed

def format_player_info(info):
    status = info['status']
    players = [player for player in status['players']]
    pvpinfo = info['pvpstatus'] 
    server = (status['ip'],int(status['port'])) # this will be accurate, even if if you change `url` to the darkrp, TTT, dev server, etc.
    a2s = get_a2s_info(server) or None
    
    for ply in players:
        connecting = ""
        score = ""
        steamid = ply['steam_id']
        name = ply['name']
        in_pvp = ""

        if ply['state'] == "spawning":
            connecting = " [SPAWNING] "
        else: # If they're spawning, their pvp status doesn't exist and nor does their name in the a2s record
            if pvpinfo[steamid]:
                in_pvp = " | in PVP"
            if a2s:
                score = " | Score: "+str(a2s[ply['name']])

        print(name+\
              in_pvp+\
              score+\
              " | "+ply['time_connected']+\
              connecting+\
              "\n"+steamid+\
              "\n"
              )
    # [CFC] Build/Kill: 8/32 playing on gm_bigcity_improved_lite
    print(status['hostname']+": "+status['player_count']+"/"+status['max_player_count'] + " playing on "+status['map'])

format_player_info(get_player_info())
