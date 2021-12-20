from copy import deepcopy
from .clock import clock

from importlib import import_module

from thefuzz import process as fuzz_process

from .GrpgCharacter import get_chara

class Domain:
    """
    Reprsents a Domain as defined by Genshin.
    Acts as an Environment/Stage where parties join and fight.
    Influences the battle by buffing/debuffing characters.
    """
    def __init__(self, game):

        self.game = game

       
        self.fbuffs = self.fbuffs or None
        self.pbuffs = self.pbuffs or None



        

        
        # stores party charas and party meta data.
        # this should have been self.parties instead and only store the party info
        # while other info should have been handled by the game but meh, works
        # for now
        player_data = {
            "party": [],
            "on_chara": 0,
            # "uses": {
            #     "auto": 0,
            #     "charge": 0,
            #     "skill": 0,
            #     "burst": 0
            # }
        }
        self.players = {
            "A": deepcopy(player_data),
            "B": deepcopy(player_data)
        }
    



    def add_player(self, player_name, *party):
        """adds a player with given party of characters"""

        if player_name not in ['A', 'B']:
            raise Exception("invalid party_name name")



        for chara_name in party:
            # validate team member
            
            Chara = get_chara(chara_name)
            
            chara = Chara(level=90)
            chara.set_domain(self)
            chara.set_player(player_name)
            chara.equip_weapon('aquila', 90)
            chara.prepare()

            # apply domain buffs. (maybe do it somewhere else)
            chara.sm.apply_fbuffs(self.fbuffs)
            chara.sm.apply_pbuffs(self.pbuffs)

            self.players[player_name]['party'].append(chara)
    
    

def get_domain(domain_name):
    
    # fetch names from domains/ dir instead?
    valid_names = ['Zhou']

    domain_name, _certainity = fuzz_process.extractOne(domain_name, valid_names)
    # make sure certainity is high.

    domain_mod = import_module(f".domains.{domain_name}",  __package__)
    domain_class = getattr(domain_mod, domain_name)
    return domain_class