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
    players = [v for v in info['status']['players']]
    pvpinfo = info['pvpstatus'] 
    server = (info['status']['ip'],int(info['status']['port'])) # incase cfc changes ip.. i guess? (instead of hardcoded ip)
    a2s = get_a2s_info(server) or None
    
    #print("There is currently "+str(len(players))+" players connected.") if there's one player it'll look stupid like "there is currently one players connected" and I can't deal with that internally (using player(s) is stupid)
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
                sid = "("+steamid+")"
                score = " | Score: "+str(a2s[ply['name']])

        print(name+score+in_pvp+" | "+ply['time_connected']+connecting+"\n"+sid+"\n")

format_player_info(get_player_info())
