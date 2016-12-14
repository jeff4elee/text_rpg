from decoder import *
from item import *
import sqlite3
import simplejson as json

pot = Potion("Basic Potion", 1, "Basic Bitches BRO [heals 10]", 10)
wep = PrimaryWeapon("Sword", 1, "BASIC BITCH SWORD [+4 dmg]", 4)

def add_item(item):

    con = sqlite3.connect('data.db')

    cur = con.cursor()

    with open('items.json', 'w') as fp:
        saved_file = json.dumps(item.encode(), fp)
        cur.execute('''INSERT INTO Items(Item_Name, Rarity, json_value) VALUES(?,?,?)''', (str(item), item.get_rarity(), saved_file))
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
    con.close()