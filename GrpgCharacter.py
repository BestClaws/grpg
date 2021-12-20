import logging

from grpg.util import get_opponent

from .clock import clock

from .reactions import Reactor

from .compute import E
from .formulae import FormulaSheet

from .weapon import Weapon
from .stats import StatsManager
from .event import Event

from .GrpgCharacterBase import GrpgCharacterBase
from .talent_impl import auto, charge, skill, burst, plunge


from thefuzz import process as fuzz_process
from importlib import import_module


class GrpgCharacter(GrpgCharacterBase):

    def __init__(self, inherent):
        super().__init__()
        
        # character's state in the game.
        self.weapon: Weapon = None
        self.domain = None
        self.player_name = None
        self.current_hp = None
        self.current_stamina = 225
        self.alive = True
        self.name = self.name or "??"

        self.sm = StatsManager(self, inherent)
        self.fs = FormulaSheet(self)
        self.reactor = Reactor(self)

        self.damages = []

        
        # player talents' action data.
        self.talent_data = {
            'auto': {},
            'charge': {},
            'skill': {},
            'burst': {},
            'plunge': {}
        } 

    

    def get_party(self):
        party = self.domain.players[self.player_name]['party']
        on_chara = self.domain.players[self.player_name]['on_chara']
        return party, on_chara

    def get_opponent_party(self):
        party = self.domain.players[get_opponent(self.player_name)]['party']
        on_chara = self.domain.players[self.player_name]['on_chara']
        return party, on_chara

    def set_player(self, party_name: str):
        """set which party the character belongs to"""
        self.player_name = party_name

    def set_domain(self, domain):
        """set the domain the character is in."""
        self.domain = domain

    def set_weapon(self, weapon: dict):
        """Set's the character's weapon"""
        self.weapon = weapon

    def __str__(self):
        """provides a meaningful name for logging."""
        return f'({self.party_pos}{self.player_name} {self.name})' 



    def prepare(self):
        """prepare before entering the domain"""
        logging.info(f"{self}: preparing")
        self.sm.prepare()
        self.reset_hp()

        # inject all tickers.
        self.tick.inject(self)
        self.take_dmg.inject(self)
        



   

    def reset_hp(self):
        """restore character's full hp"""
        logging.info(f"{self}: resetting hp to {self.sm.stats['Max HP']}")
        self.current_hp = self.sm.stats['Max HP'].val


 


    
     

    @property
    def party_pos(self):
        """gives the character's position in party. (int)"""
        for pos, chara in enumerate(self.domain.players[self.player_name]['party']):
            if chara is self:
                return pos
        return '?'

    def take_field(self):
        "do stuff where chara takes the field here"
        logging.info(f'{self}: taking field')



    def leave_field(self):
        "do stuff when chara leaves field here"
        logging.info(f'{self}: leaving field')
        pass


    def get_hp(self):
        """
        get's the current hp
        NOTE: why's this even a function
        """
        return self.current_hp




    def take_hit(self, fs):
        """get hit by a bonk """

    
        # set incoming dmg
        fs.dmg_in.set(fs.dmg_post_crit.val)

   
        # update res for incoming element
        elem = fs.element or 'Physical'
        fs.res.equals(
            self.sm.stats[elem + ' RES']
        )
        fs.refresh()

        # add damage to list of damages.        
        self.damages = [(elem, fs.final_dmg.val)]


        #TODO: do elemental reaction stuff
        if fs.element is not None: self.reactor.apply(fs.element, fs)


        self.take_dmg()

    @clock.ticker(interval=1, when='end')
    def take_dmg(self):
        logging.info(f"{self}: taking damages...")

        for type, dmg in self.damages:
            

            # damage taken is above hp, so character dies. also emit event.
            if dmg >= self.current_hp:
                self.alive = False
                self.domain.game.events.append(Event(Event.CHARA_FALL, self.party_pos))
                self.current_hp = 0

                # see if all party members died and emit game over event
                game_over = True
                for chara in self.domain.players[self.player_name]['party']:
                    if chara.alive:
                        game_over = False
                        break
                if game_over:
                    self.domain.game.events.append(Event(Event.GAME_OVER, self.player_name))
            
            else:
                # reduce hp with final dmg
                self.current_hp = self.current_hp -  dmg
                logging.info(f"{self}: took dmg: {dmg}, of type: {type}")


        self.damages.clear()

    def equip_weapon(self, name, level):
        """equips a weapon of given name and level"""
        logging.info(f"{self}: equipping wep: {name}, level: {level}")
        self.weapon = Weapon(name, level)

        # inherit its buffs
        self.sm.apply_pbuffs(self.weapon.pbuffs)


    def is_onfield(self):
        """checks whether player is on field"""
        player = self.domain.players[self.player_name]
        if self.party_pos == player['on_chara']:
            return True
        return False

    @clock.ticker(interval=2, times=5)
    def tick(self):
        """update character state every turn here"""
        logging.info(f"{self}: ticking")
        self.current_stamina += 10


    def get_stats(self):
        """returns all the necessary character's state for debugging"""
        return f"""{self}>> hp: {self.get_hp()}/{self.sm.stats['Max HP']}, stamina: {self.current_stamina}/ {self.sm.stats['Max Stamina']} """
        


    def get_talent(self, talent_name: str):
        
        if talent_name not in ['auto', 'charge', 'skill', 'burst']:
            raise Exception('Invalid talent_name')

        level = self.sm.inherent['Talents'][talent_name]['Level']
        talent_with_lvls = self.sm.inherent['Talents'][talent_name]

        talent = dict()
        for k, v in talent_with_lvls.items():
            if isinstance(v, dict):
                talent[k] = v[level]
            elif isinstance(v, (int, float, str)):
                talent[k] = v

        return talent
        
    
    #SECTION: ABILITIES

    @auto
    def invoke_auto(self, talent, data, fs):
        pass
        
    @charge
    def invoke_charge(self, talent, data, fs):
        pass
        
        # data = self.talent_data['auto']

        # if data.get('dot') is not None:
        #     logging.info('removing old dot')
        #     data.get('dot').expired = True
        #     del data['dot'] 

        # else:

        #     @clock.ticker(interval=1, times=3)
        #     def dot():
        #         logging.info('DOT!!!!')
            
        #     dot()

        #     data['dot'] = dot
      

    @skill
    def invoke_skill(self, talent, data):
        pass

    @burst
    def invoke_burst(self, talent, data):
        pass
    
    @plunge
    def invoke_plunge(self, talent, data):
        pass
  


def get_chara(chara_name):
    
    # fetch names from characters/ dir instead?
    valid_names = ['Klee', 'Kaeya']

    chara_name, _certainity = fuzz_process.extractOne(chara_name, valid_names)
    # make sure certainity is high.

    chara_mod = import_module(f".characters.{chara_name}",  __package__)
    chara_class = getattr(chara_mod, chara_name)
    return chara_class