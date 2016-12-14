import game_prompts as game, json
from options import FightOptions, TownOptions, ItemOptions
from player import *
from worldmap import *
from decoder import *

#{USER: [HEALTH, MANA, POWER]}

def init_json_to_game(player, data_dict):
    """ Takes a json_file and attempts to instantiate
        the player's unit from the json values """
    
    if 'json_file' in data_dict and data_dict['json_file']:

        player_file = json.loads(data_dict['json_file'])
        player_data = player_file['Player']
        
        con = game.retrieve_con()
        cur = con.cursor()
       
        for index, item in enumerate(player_data[conf.INVENTORY_DATA]):
            
            cur.execute("""SELECT json_value FROM Items """ \
                        """WHERE Item_Name = ?""", (item,))

            item_data = json.loads(cur.fetchone()[0])
            player_data[conf.INVENTORY_DATA][index] = decode(item_data)

        con.close()
        player = decode(player_file)
    else:    
        player = Player(data_dict['name'])
    
    return player

def enter_story():
    player = None
    game.prompt_registration()
    print ""
    json_data = game.prompt_login()
    player = init_json_to_game(player, json_data)
    init_world(player)
    story(player)

def story(player):

    def exchange_attacks(player, monster):

        player.attack(monster)

        time.sleep(conf.DEFAULT_PAUSE)

        monster.attack(player)

        time.sleep(conf.DEFAULT_PAUSE)
       
    def item_menu_sequence(player):

        if not player.get_inventory():
            print "\nEmpty Inventory!\n"
            return

        player.display_inventory()
        
        utilized_item = str(raw_input("Type an item for more options, " \
                                      "or type 'Cancel' to exit out of " \
                                      "item selection\n"))

        while(utilized_item.lower() not in map(str.lower,(map(str, player.get_inventory())))):

            if(utilized_item.lower() == 'cancel'):
                return
                
            player.display_inventory()
            utilized_item = str(raw_input("Invalid item. Try Again\n"))
                
        utilized_item = player.get_from_inventory(utilized_item)      

        while True:
            ItemOptions.display()
                
            entered_option = str(raw_input())

            #uses or equips the item depending on whether
            #or not it is consumable
            if(entered_option == str(ItemOptions.Use_Equip.value)):

                if(utilized_item.is_consumable()):
                    
                    player.set_health(player.get_health() +
                                      utilized_item.get_restore_value())
                        
                    player.remove_from_inventory(utilized_item)

                    display_unit_stats([player])
                        
                else:
                    
                    player.equip(utilized_item)

                return
            
            #displays the item's description
            elif(entered_option == str(ItemOptions.Description.value)):
                print utilized_item.get_description()
    
                return

            elif(entered_option == str(ItemOptions.Cancel.value)):
                return

    def display_unit_stats(units):
        for unit in units:
            print str(unit)
        
    def fight_sequence(player, monster):
        """ Initiates a fight with a monster """

        display_unit_stats([player, monster])
        
        #the sequence continues while both units are alive
        while(monster.get_health() > 0 and player.get_health() > 0):
            
            FightOptions.display()
            
            entered_option = str(raw_input())

            #option 1 is the standard attack
            if(entered_option == str(FightOptions.Attack.value)):
                
                exchange_attacks(player, monster)
                
                display_unit_stats([player, monster])
                
            #option 2 is item query
            elif(entered_option == str(FightOptions.Use_Item.value)):

                item_menu_sequence(player)
                

        time.sleep(2*conf.DEFAULT_PAUSE)
        
        if(player.get_health() <= 0):
            print "Game Over. You have died."
            exit(0)

        else:
            print "You have slain the monster\n"
            time.sleep(2*conf.DEFAULT_PAUSE)

            item = decode(json.loads(cur.fetchone()[0]))

            print str(item) + " has dropped"

            pick_up_prompt = str(raw_input("Do you wish to pick it up? (Y/N)"))

            if(pick_up_prompt.lower() == 'y'):
                player.add_to_inventory(item)
                print "\nYou have picked up " + str(item) + "\n"

    def prompt_move(player):
        
        #Prompts the player, asking whether they want to enter a town sequence
        if(isinstance(player.get_position(), Town)):
            
            town_prompt = "You are at the entrance of " + \
                          str(player.get_position()) + \
                          ". Do you wish to enter? (Y/N)"

            entered_answer = str(raw_input(town_prompt))

            if(entered_answer.lower() == 'y'):

                #Infinite loop of options broken by exit choice
                while(True):
                    
                    TownOptions.display()
                    
                    entered_option = str(raw_input())
                    
                    if(entered_option == str(TownOptions.Save.value)):
                        player.set_home_town(str(player.get_position()))
                        save(player)

                    elif(entered_option == str(TownOptions.Display_Stats.value)):
                        for key, value in player.get_dict().iteritems():
                            print key, ": ", str(value)
                            
                    elif(entered_option == str(TownOptions.Exit_Town.value)):
                        break

        #Prompts the player, asking whether they want to enter the dungeon node        
        elif(isinstance(player.get_position(), Dungeon)):
            dungeon_prompt = "You are at the entrance of " + \
                             str(player.get_position()) + \
                             ". Do you wish to enter? (Y/N)"
            
            entered_answer = str(raw_input(dungeon_prompt))
    
            if(entered_answer.lower() == 'y'):
                player.enter_map(player.get_position(),
                                 player.get_position().get_start())

        #Checks if the player is in the room, then
        #starts/continues the room sequence
        elif(isinstance(player.get_position(), Room)):
            
            while(player.get_position().has_monsters()):
                monster = player.get_position().next_monster()
                if monster.get_name():
                    print str(monster)
                else:
                    print "You have encountered a Goblin"

                print ""                    
                fight_sequence(player, monster)

            if(player.get_position().exitable()):

                room_prompt = "There is an exit to outside this dungeon.\n\n" \
                              + "Do you wish to take it? (Y/N)"
                entered_answer = str(raw_input(room_prompt))
                
                if(entered_answer.lower() == 'y'):
                    player.exit_map()
                    
        #displays the nodes adjacent to the player
        print "\nNearby Locations\n", conf.LINE_SEPARATOR, \
              player.get_current_map(). \
              display_adjacent(player.get_position()), \
              "\n", conf.LINE_SEPARATOR, \
              "Type the nearby location you wish to travel to"
        
        #TODO make string constants for prompts
        entered_node = str(raw_input())

        #checks if the entered_node is adjacent or valid
        for node in player.get_current_map(). \
            get_adjacent_vertices(player.get_position()):
            
            if entered_node.lower() == str(node).lower():

                player.set_position(node)
                
            elif isinstance(node, Room) and \
                 entered_node.lower() == str(node.get_id()):

                player.set_position(node)

    while(True):

        time.sleep(conf.DEFAULT_PAUSE)

        prompt_move(player)
        
        print conf.LINE_SEPARATOR, "\nCurrent Position:", player.get_position()
        
        
def save(player):
    """ Wrapper function that calls on the
        game prompts save function """
            
    data = player.encode()
    game.save("data.json", data)

enter_story()
