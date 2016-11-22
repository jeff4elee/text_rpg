import game_prompts as game
import simplejson as json
from conf import DEFAULT_HEALTH, DEFAULT_MANA, DEFAULT_POWER
from player import Unit

player = None

#{USER: [HEALTH, MANA, POWER]}

def save():
    """ Wrapper function that calls on the
        game prompts save function """
    
    data = player.getData()
    game.save("data.json", data)
    
def init_json_to_game(json_file):
    """ Takes a json_file and attempts to instantiate
        the player's unit from the json values """
    
    global player
    
    if not json_file:
        player = Unit()
    else:
        data = json.loads(json_file)
        player = Unit(data)
    return

def enter_story():
    game.prompt_registration()
    try:
        json_data = game.prompt_login()
        init_json_to_game(json_data)
    except:
        print "Error"
        

enter_story()

