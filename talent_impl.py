#TODO: use functools.wraps for docstring preservation


import logging
from .util import get_opponent
import random

def auto(func):
    def wrapper(self):
        
        #SECTION: auto attack configs
        AOE = False

        #END

        talent = self.get_talent('auto')

        # record auto attack streak (decides the damage multiplier to use)
        # TODO: getting interrupted or using other talents should reset the streak.
        if self.auto.get('streak') is None:
            self.auto['streak'] = 0
        else:
            self.auto['streak'] += 1
        
        # pick the damange multiplier based on streak.
        #  (1-hit dmg, 2-hit dmg, etc.,)
        mulitplier_list = talent['DMG']
        i = self.auto['streak'] % len(mulitplier_list) 
        xer = mulitplier_list[i]
        logging.info(f"{self}: invoking auto {i} with dmg scale: {xer}")



        # TODO: apply remove/buffs debuffs on self and/or enemies, if any
        
        # calculate output dmg
        self.ability_dmg_out = self.stats.stats['ATK'] * xer
        self.bonus_dmg_out = self.ability_dmg_out * (self.stats.stats['Physical DMG Bonus'] + 1)


        crit = False
        if self.stats.stats['Crit Rate'].val > random.random(): crit = True
        self.crit_dmg_out = self.bonus_dmg_out * ((self.stats.stats['Crit DMG'] + 1) if crit else 1)


        # make changes as per required by character
        func(self)

        # hit the opponent(s)
        opponent_name = get_opponent(self.player_name)
        opponent = self.domain.players[opponent_name]
        chara = opponent['party'][opponent['on_chara']]
        bonk = {'element': 'physical', 'crit': crit, 'dmg': self.crit_dmg_out}
        chara.get_hit(bonk)
        pass
    return wrapper


import logging
from .util import get_opponent
import random

def charge(func):
    def wrapper(self):

        #SECTION: auto attack configs
        self.AOE = True

        #END

        
        talent = self.get_talent('charge')

        if self.current_stamina < talent['Stamina Cost']:
            # not enough stamina
            return

        self.current_stamina -= talent['Stamina Cost']

        logging.info(f"{self}: invoking charge attack with xer: {talent['DMG']}")




        # TODO: apply remove/buffs debuffs on self and/or enemies
        
        # calculate output dmg
        ability_dmg_out = self.stats.stats['ATK'] * talent['DMG']

        bonus_dmg_out = ability_dmg_out * (self.stats.stats['Physical DMG Bonus'] + 1)


        crit = False
        if self.stats.stats['Crit Rate'].val > random.random(): crit = True
        crit_dmg_out = bonus_dmg_out * ((self.stats.stats['Crit DMG'] + 1) if crit else 1)


        # configure as per character's wish
        func(self)

        # hit the opponent(s)
        opponent_name = get_opponent(self.player_name)
        opponent = self.domain.players[opponent_name]
        for chara in opponent['party']:
            bonk = {'element': 'physical', 'crit': crit, 'dmg': crit_dmg_out}
            chara.get_hit(bonk)
    return wrapper


def skill(func):
    def wrapper(self):
        pass
    return wrapper

def burst(func):
    def wrapper(self):
        pass
    return wrapper

def plunge(func):
    def wrapper(self):
        pass
    return wrapper