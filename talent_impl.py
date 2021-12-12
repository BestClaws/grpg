#TODO: use functools.wraps for docstring preservation

from .clock import clock

import logging
from .util import get_opponent
import random
from .compute import E

def auto(func):
    def wrapper(self):
        

        talent = self.get_talent('auto')
        data = self.talent_data['auto']


        # record auto attack streak (decides the damage multiplier to use)
        # TODO: getting interrupted or using other talents should reset the streak.
        if data.get('streak') is None:
            data['streak'] = 0
        else:
            data['streak'] += 1
        
        # pick the damange multiplier based on streak.
        #  (1-hit dmg, 2-hit dmg, etc.,)
        mulitplier_list = talent['DMG']
        i = data['streak'] % len(mulitplier_list) 
        xer = mulitplier_list[i] / 100 # normalize
        logging.info(f"{self}: invoking auto {i} with dmg scale: {xer}")





        # update damage multiplier
        self.fs.ability_xer.set(xer)

        # update dmg bonuses
        new_exp = self.fs.ability_dmg * (self.sm.stats['Physical DMG Bonus'] + 1)
        self.fs.dmg_post_bonus.equals(new_exp)


        # update whether hit was ciritical
        if self.sm.stats['Crit Rate'].val > random.random():
            self.fs.critical_hit.set(1)
        else:
            self.fs.critical_hit.set(0)

        # make changes as per required by character
        func(self, talent, data)



        # hit the opponent(s)
        opponent_name = get_opponent(self.player_name)
        opponent = self.domain.players[opponent_name]
        chara = opponent['party'][opponent['on_chara']]
        bonk = {
            'element': 'Pyro',
            'crit': self.fs.critical_hit,
            'dmg': self.fs.dmg_post_crit.val,
            'em': self.sm.stats['Elemental Mastery'].val
            }

        logging.info(f"{self} outgoing {'a crit ' if bonk['crit'] else ''} hit with {bonk['dmg']}, exp: {self.fs.dmg_post_crit.eq()}")
        
        chara.take_hit(bonk)
        pass
    return wrapper




def charge(func):
    def wrapper(self):

        talent = self.get_talent('charge')
        data = self.talent_data['charge']


        logging.info(f"{self}: invoking charge attack with xer: {talent['DMG']}")

        if self.current_stamina < talent['Stamina Cost']:
            # not enough stamina
            return
        self.current_stamina -= talent['Stamina Cost']


        
        # update ability multiplier
        xer = sum(talent['DMG']) / 100 # normalize
        self.fs.ability_xer.set(xer)

        # update dmg bonuses
        new_exp = self.fs.ability_dmg * (self.sm.stats['Physical DMG Bonus'] + 1)
        self.fs.dmg_post_bonus.equals(new_exp)


        # update whether hit was ciritical
        if self.sm.stats['Crit Rate'].val > random.random():
            self.fs.critical_hit.set(1)
        else:
            self.fs.critical_hit.set(0)


        # configure as per character's wish
        func(self, talent, data)

        # hit the opponent(s)
        opponent_name = get_opponent(self.player_name)
        opponent = self.domain.players[opponent_name]
        for chara in opponent['party']:
            bonk = {
                'element': 'Cryo',
                'crit': self.fs.critical_hit.val,
                'dmg': self.fs.dmg_post_crit.val,
                'em': self.sm.stats['Elemental Mastery'].val
            }
            
            logging.info(f"{self} outgoing {'a crit ' if bonk['crit'] else ''} hit with {bonk['dmg']}, exp: {self.fs.dmg_post_crit.eq()}")
            chara.take_hit(bonk)
 
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