from enum import Enum
import conf

class Slot(Enum):
    Primary = 0x0001
    Secondary = 0x0002
    Two_Hand = 0x0003
    Body = 0x0004
    Head = 0x0008

        
class Item(object):

    def __init__(self, item_name, rarity, description, consumable=None):
        """ Barebones parent class that provides item descriptions """
        self._name = item_name
        self._rarity = rarity
        self._description = description
        self._consumable = consumable if consumable else False

    def get_rarity(self):
        return self._rarity
    
    def is_consumable(self):
        return self._consumable
    
    def get_name(self):
        return self._name

    def get_description(self):
        return self._description
    
    def __str__(self):
        return self._name

    def encode(self):
        return {self.__class__.__name__: self.get_dict()}

    def get_dict(self):
        data_dict = dict()
        data_dict[conf.ITEM_NAME] = self._name
        data_dict[conf.ITEM_RARITY] = self._rarity
        data_dict[conf.ITEM_DSCRPT] = self._description
        return data_dict
    
    @staticmethod
    def from_dict(dct):
        name = dct[conf.ITEM_NAME]
        rarity = dct[conf.ITEM_RARITY]
        descript = dct[conf.ITEM_DSCRPT]
        return Item(name, rarity, descript)
    
class Potion(Item):

    def __init__(self, item_name, rarity, description, restore_value):
        """ Consumable item that provides some form of restore value """
        super(Potion, self).__init__(item_name, rarity, description, True)
        self._restore_value = restore_value

    def get_restore_value(self):
        return self._restore_value

    def encode(self):
        """ Returns a dictionary filled with the potion data """
        data_dict = super(Potion, self).get_dict()
        data_dict[conf.POTION_HEAL_DATA] = self._restore_value
        return {self.__class__.__name__: data_dict}

    @staticmethod
    def from_dict(dct):
        name = dct[conf.ITEM_NAME]
        rarity = dct[conf.ITEM_RARITY]
        descript = dct[conf.ITEM_DSCRPT]
        restore = dct[conf.POTION_HEAL_DATA]
        return Potion(name, rarity, descript, restore)

class Equippable(Item):
    
    def __init__(self, item_name, rarity, description, slot_value, bonuses):
        """ Abstract item class that includes abstract equip slot usage
            and stat bonuses """
        super(Equippable, self).__init__(item_name, rarity, description, False)
        self._slot_value = slot_value
        self._bonuses = bonuses

    def get_slot(self):
        return self._slot_value
    
    def get_bonuses(self):
        return self._bonuses

    def get_dict(self):
        data_dict = super(Equippable, self).get_dict()
        data_dict[conf.SLOT_VALUE] = self._slot_value
        
        for stat in conf.STATS:
            if stat in self.get_bonuses():
                data_dict[stat] = self.get_bonuses()[stat] 

        return data_dict
        
    def encode(self):
        """ Returns a dictionary filled with the weapon data """
        data_dict = self.get_dict()
        return {self.__class__.__name__: data_dict}

    @staticmethod
    def from_dict(dct):
        name = dct[conf.ITEM_NAME]
        rarity = dct[conf.ITEM_RARITY]
        descript = dct[conf.ITEM_DSCRPT]
        slot = dct[conf.SLOT_VALUE]
        
        weapon_stats = {}
        for stat in conf.STATS:
            if stat in dct.keys():
                weapon_stats[stat] = dct[stat]
        return Equippable(name, rarity, descript, slot, weapon_stats)

class Coins(Item):
    def __init__(self, amount=None):
        super(Coins, self).__init__("Coins", 0, "A form of currency")
        self._amount = amount if amount else 0

    def use(self, amount):
        if(amount <= self._amount):
            self._amount -= amount
            return
        print "Insufficient funds!"

    def add(self, amount):
        self._amount += amount

    def get_amount(self):
        return self._amount
    
    def encode(self):
        data_dict = {conf.COIN_AMOUNT: self._amount}
        return {self.__class__.__name__: data_dict}

    @staticmethod
    def from_dict(dct):
        amount = dct[conf.COIN_AMOUNT]
        return Coins(amount)
