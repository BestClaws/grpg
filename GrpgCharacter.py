from util import get_stat
from logger import log

from GrpgCharacterBase import GrpgCharacterBase


class GrpgCharacter(GrpgCharacterBase):

    def __init__(self, domain, party_name, level):
        super().__init__()

        # character's volatile stats and game stats.
        self.level = level
        self.alive = True
        self.party_name = party_name
        self.domain = domain

        # calculate all stats
        self.infer_base_stats()

        # prepare before entering domain
        self.prepare()
        
        self.wep = {"BASE_ATK": 12}


    def prepare(self):
        self.reset_hp()
        log.info(f"I {self.get_position()} from {self.party_name} have {self.stats['HP']} remaining out of {self.stats['MAX_HP']}")


    def infer_base_stats(self):
        """infers all the base stats using provided level and stats tables"""
        if not self.level:
            raise Exception("set a character level first!")

        self.stats['BASE_ATK'] = get_stat(self.stats["base_atk_table"], self.level)
        self.stats['MAX_HP'] = get_stat(self.stats["base_hp_table"], self.level)

   

    def reset_hp(self):
        """restore character's full hp"""
        self.stats['HP'] = self.stats['MAX_HP']


 


    def buff(self, buffs):
        self.stats


    def get_position(self):
        for i, chara in enumerate(self.domain.parties[self.party_name]['charas']):
            if chara is self:
                return i


    def focus(self):
        log.info(f'I {self.get_position()} from {self.party_name} became active.')



    def blur(self):
        log.info(f'I {self.get_position()} from {self.party_name} switched off-field.')
        pass

    def get_hp(self):
        return self.stats['HP']