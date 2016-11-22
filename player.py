from conf import DEFAULT_HEALTH, DEFAULT_MANA, DEFAULT_POWER

class Unit():
    def __init__(self, data=None):
                 
        self._health = DEFAULT_HEALTH
        self._maxHealth = DEFAULT_HEALTH
        self._mana = DEFAULT_MANA
        self._maxMana = DEFAULT_MANA
        self._power = DEFAULT_POWER

        if(data):
            self.setData(data)
            
    def getHealth(self):
        return self._health

    def setHealth(self, health):
        if(health > self._maxHealth):
            self._health = self._maxHealth
        else:
            self._health = health

    def getMaxHealth(self):
        return self._maxHealth

    def setMaxHealth(self, maxHealth):
        self._maxHealth = maxHealth
        
    def getMana(self):
        return self._mana

    def setMana(self, mana):
        if(mana > self._maxMana):
            self._mana = self._maxMana
        else:
            self._mana = mana

    def getMaxMana(self):
        return self._maxMana
    
    def setMaxMana(self, maxMana):
        self._maxMana = maxMana
        
    def getPower(self):
        return self._power

    def setPower(self, power):
        self._power = power

    def attack(self, unit):
        unit.setHealth(unit.getHeath() - self.power)

    def getData(self):
        return {'health': self._health,
                'maxHealth': self._maxHealth,
                'mana': self._mana,
                'maxMana': self._maxMana,
                'power': self._power}

    def setData(self, data):        
        self._health = data['health']
        self._maxHealth = data['maxHealth']
        self._mana = data['mana']
        self._maxMana = data['maxMana']
        self._power = data['power']

def generateUnit(health, mana, power):
    return Unit({'health': health,
                'maxHealth': health,
                'mana': mana,
                'maxMana': mana,
                'power': power})
       
class Player():

    def __init__(self, name, status = None, money = None, inventory = None, allies = None):
        """ Takes in a string name, a Status enum, an int money,
            a dict inventory, and a list for allies """
        self._status = status
        self._money = money
        self._inventory = inventory
        self._allies = allies
        self.name = name

    def getMoney(self):
        """ Retrieves the current amount of money """
        return self._money

    def setMoney(self, money):
        """ Adjusts the current amount of money to the new amount """
        self._money = money
        
    def getStatus(self):
        """ Retrieves the current status """
        return self._status

    def setStatus(self, status):
        """ Mutator to change the instance's status """
        self._status = status
        
    def displayStatus(self):
        """ Returns the status name and description """
        return self._status.name + ":", self._status.value

    def getAllies(self):
        """ Returns a list of allies """
        return self._allies

    def addAlly(self, ally):
        """ Appends the new ally into the ally list
            This action adds the player into the ally's
            ally list as well """
        self._allies.append(ally)
        ally._allies.append(self)

    def removeAlly(self, ally):
        """ Removes an ally from the ally list, but doing so
            removes the player from the ally's ally list as well"""
        self._allies.remove(self._allies.index(ally))
        ally._allies.remove(ally._allies.index(self))
        
    def getInventory(self):
        return self._inventory

    def addToInventory(self, item):
        if self._inventory[item]:
            self._inventory[item] += 1
        else:
            self._inventory[item] = 0

    def removeFromInventory(self, item):
        try:
            self._inventory[item] -= 1
        except:
            print "Item does not exist"
        
    def getName(self):
        """ Returns the name of the player """
        return self.name;

    def __str__(self):
        return self.name;

