import logging as log
from util import get_opponents
from GrpgCharacter import GrpgCharacter

class Kaeya(GrpgCharacter):
    
    def __init__(self, *, domain, party_name, level=1):
        
        self.stats = {"element": "cryo"}
        

        # dmg output multiplies
        self.stats['dmg_xer'] = {
            'auto': 0.5,
            'charge': 0.7,
            'skill': 1.5,
            'burst': 3.0
        }

        # x.5 denotes ascension, while x is unascended
        self.stats["base_hp_table"] = {
            1: 793,
            20: 2038,
            20.5: 2630,
            40: 3940,
            40.5: 4361,
            50: 5016,
            50.5: 5578,
            60: 6233,
            60.5: 6654,
            70: 7309,
            70.5: 7730,
            80: 8385,
            80.5: 8805,
            90: 9461
        }

        self.stats["base_atk_table"] = {
            1: 19,
            20: 48,
            20.5: 62,
            40: 93,
            40.5: 103,
            50: 118,
            50.5: 131,
            60: 147,
            60.5: 157,
            70: 172,
            70.5: 182,
            80: 198,
            80.5: 208,
            90: 223
        }

        self.stats['CRIT_RATE'] = 0.05
        self.stats['CRIT_DMG'] = 0.50

        super().__init__(domain, party_name, level)



    def invoke_auto(self):

        log.info(f"I {self.get_position()} from {self.party_name} am  invoking auto attack")

        # auto attack configs
        AOE = False


        # TODO: apply remove/buffs debuffs on self and/or enemies
        
        # calculate output dmg
        base_atk = self.stats['BASE_ATK'] + self.wep["BASE_ATK"]
        atk = base_atk * 1 # any base atk buffs would go here.
        auto_dmg_out = atk * self.stats["dmg_xer"]['auto']
        final_dmg_out = auto_dmg_out * 1 # any final dmg output buffs go here.

        # hit the opponent(s)
        opponent_party = get_opponents(self.party_name)
        opponents = self.domain.parties[opponent_party]
        for chara in opponents['charas']:
            bonk = {"element": self.stats['element'], 'dmg': final_dmg_out}
            chara.hit(bonk)
            if not AOE: break


        

    def hit(self, bonk):
        log.info(f'gaah I {self.get_position()} from {self.party_name} got hit')
        self.stats['HP'] -= bonk['dmg']
        log.info(f"after taking a bonk of dmg {bonk['dmg']}, i have {self.stats['HP']} remaining out of {self.stats['MAX_HP']}")


    def invoke_charge(self):
        pass

    def invoke_skill(self):
        pass

    def invoke_burst(self):
        pass

  

