import requests
import json
from steam import game_servers as gs

url = 'https://nanny.cfcservers.org/cfc3-status'
"""
# There are 12 players connected
# -------------
# Name: POLY | Time Connnected: 1:24:01 | [SPAWNING]
"""
def get_a2s_info(server): 
    try: # this can fail, completely up to the server
        players = gs.a2s_players(server)
        scores = {}
        for ply in players:
            scores[ply['name']] = ply['score']
        return scores
    except:
        print("Server A2S error, i'm sure it's fine")
        pass
         

def get_player_info():
    r = requests.get(url)
    if r.ok:
        return json.loads(r.text)

def format_player_info(info):
    players = [v for v in info['status']['players']]
    pvpinfo = info['pvpstatus'] 
    server = (info['status']['ip'],int(info['status']['port'])) # incase cfc changes ip.. i guess? (instead of hardcoded ip)
    a2s = get_a2s_info(server) or None
    
    for ply in players:
        connecting = ""
        score = ""
        steamid = ply['steam_id']
        name = ply['name']+" ("+steamid+") "
        in_pvp = ""

        if ply['state'] == "spawning":
            connecting = "\n\t[SPAWNING]"
        else: # If they're spawning, their pvp status doesn't exist and nor does their name in the a2s record
            if pvpinfo[steamid]:
                in_pvp = "\n\tin PVP: Yes"
            if a2s:
                score = "\n\tScore: "+str(a2s[ply['name']])
        print(name+score+in_pvp+"\n\tTime Connected: "+ply['time_connected']+connecting+"\n")

format_player_info(get_player_info())
