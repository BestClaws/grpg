#TODO: use functools.wraps for docstring preservation

from .clock import clock

import logging
from .util import get_opponent
import random
from .compute import E

def auto(func):
    def wrapper(self):

        # get a new formula sheet
        fs = self.fs.copy()
        
        # load talent info and data/state
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
        logging.info(f"{self}: invoking auto {i} with dmg multiplier: {xer}")



        # update damage multiplier
        fs.talent_xer.set(xer)


        # update whether hit was ciritical
        if self.sm.stats['Crit Rate'].val > random.random():
            fs.critical_hit.set(1)
        else:
            fs.critical_hit.set(0)

        # make changes as required by character
        func(self, talent, data, fs)



        # hit the opponent(s)
        opponent_name = get_opponent(self.player_name)
        opponent = self.domain.players[opponent_name]
        opp_chara = opponent['party'][opponent['on_chara']]
        opp_chara.take_hit(fs)

        logging.info(f"{self} outgoing {'a crit ' if fs.critical_hit.val else ''} hit with {fs.dmg_post_crit.val}, exp: {fs.dmg_post_crit.eq()}")


    return wrapper




def charge(func):
    def wrapper(self):

        
        fs = self.fs.copy()

        talent = self.get_talent('charge')
        data = self.talent_data['charge']


        logging.info(f"{self}: invoking charge attack with xer: {talent['DMG']}")

        if self.current_stamina < talent['Stamina Cost']:
            # not enough stamina
            return
        self.current_stamina -= talent['Stamina Cost']


        
        # update ability multiplier
        xer = sum(talent['DMG']) / 100 # normalize
        fs.talent_xer.set(xer)


        # update whether hit was ciritical
        if self.sm.stats['Crit Rate'].val > random.random():
            fs.critical_hit.set(1)
        else:
            fs.critical_hit.set(0)

        # make changes as required by character
        func(self, talent, data, fs)

        # hit the opponent(s)
        opponent_name = get_opponent(self.player_name)
        opponent = self.domain.players[opponent_name]
       
        for opp_chara in opponent['party']:       
            opp_chara.take_hit(fs)
            
            logging.info(f"{self} outgoing {'a crit ' if fs.critical_hit.val else ''} hit with {fs.dmg_post_crit.val}, exp: {fs.dmg_post_crit.eq()}")     

 
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