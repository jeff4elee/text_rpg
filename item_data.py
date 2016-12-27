from decoder import *
from item import *
from dungeon import *
import conf
import sqlite3
import simplejson as json

pot = Potion("Basic Potion", 1, "Basic potion [heals 6]", 6)
wep = Equippable("Sword", 1, "Basic sword [1 atk, 1 speed]",
                 Slot.Primary.value, {conf.POWER_DATA: 1, conf.SPEED_DATA: 1})
wep2 = Equippable("Dagger", 1, "Basic dagger [4 speed]",
                  Slot.Secondary.value, {conf.SPEED_DATA: 4})
wep3 = Equippable("Hammer", 1, "Basic hammer [3 atk, -10 speed]",
                  Slot.Two_Hand.value, {conf.POWER_DATA: 3, conf.SPEED_DATA: -10})
body1 = Equippable("Leather Tunic", 1, "Basic tunic [2 health, 1 speed]",
                   Slot.Body.value, {conf.MAX_HEALTH_DATA: 2, conf.SPEED_DATA: 1})
head1 = Equippable("Helmet", 1, "Basic helmet [5 health, -2 speed]",
                   Slot.Head.value, {conf.MAX_HEALTH_DATA: 5, conf.SPEED_DATA: -2})

"""dun1 = Dungeon(name="Dick Dungeon", monster_type='Cave',
               num_rooms=3, difficulty=1, drop_rate=1.0)
    
dun2 = Dungeon(name="Rick Dungeon", monster_type='Cave',
               num_rooms=5, difficulty=1, drop_rate=1.0)
    
dun3 = Dungeon(name="Sick Dungeon", monster_type='Cave',
               num_rooms=3, difficulty=2, drop_rate=1.0)
    
dun4 = Dungeon(name="Lick Dungeon", monster_type='Cave',
               num_rooms=5, difficulty=2, drop_rate=1.0)"""
    

def reset_dungeon_table():
    con = sqlite3.connect('data.db')
    
    cur = con.cursor()

    try:
        cur.execute('''DROP TABLE Dungeons''')
        cur.execute('''CREATE TABLE Dungeons(Dungeon_Id INTEGER PRIMARY KEY, '''
                    '''Dungeon_Name TEXT UNIQUE, json_value TEXT)''')

    except:
        cur.execute('''CREATE TABLE Dungeons(Dungeon_Id INTEGER PRIMARY KEY, '''
                    '''Dungeon_Name TEXT UNIQUE, json_value TEXT)''')

    con.commit()
    con.close()
    
    
def reset_item_table():

    con = sqlite3.connect('data.db')
    
    cur = con.cursor()

    try:
        cur.execute('''DROP TABLE Items''')
        cur.execute('''CREATE TABLE Items(Item_Id INTEGER PRIMARY KEY, '''
                    '''Item_Name TEXT UNIQUE, Rarity INTEGER, json_value TEXT)''')

    except:
        cur.execute('''CREATE TABLE Items(Item_Id INTEGER PRIMARY KEY, '''
                    '''Item_Name TEXT UNIQUE, Rarity INTEGER, json_value TEXT)''')

    con.commit()
    con.close()
    
def add_item(item):

    con = sqlite3.connect('data.db')

    cur = con.cursor()

    with open('items.json', 'w') as fp:
        saved_file = json.dumps(item.encode(), fp)
        cur.execute('''INSERT INTO Items(Item_Name, Rarity, json_value) VALUES(?,?,?)''', (str(item), item.get_rarity(), saved_file))
        fp.close()
    con.commit()
    con.close()
    
def add_dungeon(dun):

    con = sqlite3.connect('data.db')

    cur = con.cursor()

    with open('dungeons.json', 'w') as fp:
        saved_file = json.dumps(dun.encode(), fp)
        cur.execute('''INSERT INTO Dungeons(Dungeon_Name, json_value) VALUES(?,?,)''', (str(dun), dun.get_dict(), saved_file))
        fp.close()
        
    con.commit()
    con.close()

def display():
    con = sqlite3.connect('data.db')

    cur = con.cursor()
    cur.execute('''SELECT * FROM Items''')
#cur.execute("""SELECT Item_Name FROM Items WHERE Item_Name = ?""", ('Ring LOL',))

    data = cur.fetchall()
    for row in data:
        for col in row:
            print col,
        print '\n'

    print conf.LINE_SEPARATOR
    
    cur.execute('''SELECT * FROM Dungeons''')
#cur.execute("""SELECT Item_Name FROM Items WHERE Item_Name = ?""", ('Ring LOL',))

    data = cur.fetchall()
    for row in data:
        for col in row:
            print col,
        print '\n'

    con.close()
