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

        #opens up a connection to the database where the item table lies
        con = game.retrieve_con()
        cur = con.cursor()

        #decodes each item in the inventory and equipped lists
        for index, item in enumerate(player_data[conf.INVENTORY_DATA]):
            
            #queries the json_value of the item by its name
            cur.execute("""SELECT json_value FROM Items """ \
                        """WHERE Item_Name = ?""", (item,))

            #loads the item dictionary from the json string
            item_data = json.loads(cur.fetchone()[0])
            
            player_data[conf.INVENTORY_DATA][index] = decode(item_data)

        for index, item in enumerate(player_data[conf.EQUIP_DATA]):
            
            cur.execute("""SELECT json_value FROM Items """ \
                        """WHERE Item_Name = ?""", (item,))

            item_data = json.loads(cur.fetchone()[0])
            player_data[conf.EQUIP_DATA][index] = decode(item_data)

        #closes connection as the database is not needed anymore    
        con.close()
        
        player = decode(player_file)
    else:    
        player = Player(data_dict['name'])
    
    return player

def enter_story():
    player = None

    while(True):
        
        user_input = int(raw_input("1. Register 2. Login\n"))

        if(user_input == 1):
            game.prompt_registration()
            print ""
            
        elif(user_input ==2):
            try:
                json_data = game.prompt_login()
                player = init_json_to_game(player, json_data)
                init_world(player)
                story(player)
            except:
                continue

def story(player):

    def exchange_attacks(unit_one, unit_two):

        #calculates which unit attacks faster
        fastest_speed = min(unit_one.get_cspeed(), unit_two.get_cspeed())

        #decreases the time each unit has to take to attack
        unit_one.set_cspeed(unit_one.get_cspeed() - fastest_speed)
        unit_two.set_cspeed(unit_two.get_cspeed() - fastest_speed)

        #unit with 0 attack time will attack the other unit
        #returns True if unit one attacks first, False if unit two
        if(unit_one.get_cspeed() == 0):
            
            unit_one.attack(unit_two)

            print unit_one.get_name() + " attacks " + str(unit_two.get_name()) + \
                  " for " + str(unit_one.get_power()) + " damage\n"

            time.sleep(2*conf.DEFAULT_PAUSE)

            return True
        
        if(unit_two.get_health() > 0 and unit_two.get_cspeed() == 0):
            
            unit_two.attack(unit_one)

            print unit_two.get_name() + " attacks " + str(unit_one.get_name()) + \
                  " for " + str(unit_two.get_power()) + " damage\n"
        
            time.sleep(2*conf.DEFAULT_PAUSE)

            return False

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

                if(isinstance(utilized_item, Coins)):
                    print "Coins can't be used in this context"
                    continue
                
                if(utilized_item.is_consumable()):

                    print player.get_name() + " healed for " + \
                          str(utilized_item.get_restore_value())
                    
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
    
            elif(entered_option == str(ItemOptions.Cancel.value)):
                return

    def display_unit_stats(units):
        for unit in units:
            print str(unit) + "\n"
        
    def fight_sequence(player, monster):
        """ Initiates a fight with a monster fight_sequence(player, monster)"""

        display_unit_stats([player, monster])
        
        #the sequence continues while both units are alive
        while(monster.get_health() > 0 and player.get_health() > 0):
            
            FightOptions.display()            
            entered_option = str(raw_input())

            #option 1 is the standard attack
            if(entered_option == str(FightOptions.Attack.value)):

                while(player.get_health()):
                    if exchange_attacks(player, monster):
                        break
                display_unit_stats([player, monster])
                                
            #option 2 is item query
            elif(entered_option == str(FightOptions.Use_Item.value)):

                item_menu_sequence(player)
                print ""
                display_unit_stats([player, monster])

            elif(entered_option == str(FightOptions.Stats.value)):

                player.display_stats()
                print ""
                player.display_equipped()
                print ""
                
        time.sleep(conf.DEFAULT_PAUSE)
        
        if(player.get_health() <= 0):
            print "Game Over. You have died."
            exit(0)

        else:
            print "You have slain the monster\n"

            player.set_cspeed(player.get_speed())
            
            time.sleep(2*conf.DEFAULT_PAUSE)

            items = monster.get_loot()

            while items:

                item = decode(items.pop())

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

                    print
                    TownOptions.display()
                    
                    entered_option = str(raw_input())
                    
                    if(entered_option == str(TownOptions.Save.value)):
                        player.set_home_town(str(player.get_position()))
                        player.set_health(player.get_max_health())
                        player.set_mana(player.get_max_mana())
                        save(player)

                    elif(entered_option == str(TownOptions.Stats.value)):
                        player.display_stats()
                        
                    elif(entered_option == str(TownOptions.Equipment.value)):
                        player.display_equipped()

                    elif(entered_option == str(TownOptions.Use_Equip.value)):
                        item_menu_sequence(player)
                        
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
                    print "You have encountered a", monster.get_name()
                else:
                    print "You have encountered a STUB"

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
