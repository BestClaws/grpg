import logging

from util import interpolate_stat
from GrpgCharacterBase import GrpgCharacterBase


class GrpgCharacter(GrpgCharacterBase):

    def __init__(self, domain, party_name, level):
        super().__init__()

        # non chara specific parameters.

        self.stats['level'] = level
        self.stats['stamina'] = 225
        self.stats['energy'] = 0


        # character's state in the game.
        self.alive = True
        self.party_name = party_name
        self.domain = domain
        self.stats_buffs = {} # contains all the places a character can get a buff.
        
        # calculate all stats
        self.infer_base_stats()

        # prepare before entering domain
        self.prepare()
        

        # weapon info.
        self.wep = {"BASE_ATK": 12}




    @property
    def me(self):
        """provides a meaningful name for logging."""
        return f'({self.party_pos}{self.party_name})' 



    def prepare(self):
        logging.info(f"{self.me}: preparing")
        self.reset_hp()
        self.clear_buffs()


    def infer_base_stats(self):
        """infers all the base stats using provided level and stats tables"""

        if not self.stats['level']:
            raise Exception("set a character level first!")

        self.stats['BASE_ATK'] = interpolate_stat(self.base_atk_table, self.stats['level'])
        self.stats['MAX_HP'] = interpolate_stat(self.base_hp_table, self.stats['level'])

   

    def reset_hp(self):
        """restore character's full hp"""
        logging.info(f"{self.me}: resetting hp to MAX_HP")
        self.stats['HP'] = self.stats['MAX_HP']


 


    def apply_buffs(self, buffs):
        """
        adds given buffs to buff list.
        negative value represents a debuff.
        """
        logging.info(f"{self.me}: buffing myself")
        for stat_name in buffs.keys():
            stat_val = self.stats_buffs.get(stat_name, None)
            if stat_val is not None:
                self.stats_buffs[stat_name] +=  buffs[stat_name]


    def clear_buffs(self):
        self.stats_buffs = {
                'ATK': 0.0,
                'HP': 0.0,
                'DMG': 0.0,
                'PYRO_DMG': 0.0,
                'CRYO_DMG': 0.0,
                'ANEMO_DMG': 0.0,
                'ELECTRO_DMG': 0.0,
                'HYDRO_DMG': 0.0,
                'GEO_DMG': 0.0,
                'ER': 0.0,
                'CR': 0.0,
                'CD': 0.0
            }        

    @property
    def party_pos(self):
        """gives the character's position in party. (int)"""
        for pos, chara in enumerate(self.domain.parties[self.party_name]['charas']):
            if chara is self:
                return pos
        return '?'

    def take_field(self):
        logging.info(f'{self.me}: taking field')



    def leave_field(self):
        logging.info(f'{self.me}: leaving field')
        pass

    def get_hp(self):
        return self.stats['HP']