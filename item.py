from enum import Enum
import conf

class Slot(Enum):
    Primary = 0x00800
    Secondary = 0x04000
    
class Item(object):

    def __init__(self, item_name, rarity, description, consumable=None):
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
        data_dict[conf.ITEM_DSCRPT] = self._description
        return data_dict
    
    @staticmethod
    def from_dict(dct):
        name = dct[conf.ITEM_NAME]
        descript = dct[conf.ITEM_DSCRPT]
        rarity = dct[conf.ITEM_RARITY]
        return Item(name, rarity, descript)
    
class Potion(Item):

    def __init__(self, item_name, rarity, description, restore_value):
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
        return Potion(name, descript, restore)

class Equippable(Item):
    
    def __init__(self, item_name, rarity, description, slot_value, bonus):
        super(Equippable, self).__init__(item_name, rarity, description, False)
        self._slot_value = slot_value
        self._bonus = bonus

    def get_slot(self):
        return self._slot_value
    
    def get_bonus(self):
        return self._bonus

class PrimaryWeapon(Equippable):
    
    def __init__(self, item_name, rarity, description, power):
        super(PrimaryWeapon, self).__init__(item_name, rarity, description, 0x02000, power)

    def get_dict(self):
        data_dict = super(PrimaryWeapon, self).get_dict()
        data_dict[conf.POWER_DATA] = self.get_bonus()
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
        atk = dct[conf.POWER_DATA]
        return PrimaryWeapon(name, descript, atk)
