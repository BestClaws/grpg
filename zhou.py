import logging
from typing import List
from .GrpgCharacter import GrpgCharacter

from .domain import Domain
from .clock import clock

class Zhou(Domain):

    def __init__(self, game):

       
        self.fullname = "Hidden Palace of Zhou Formula"
        self.description = "favourite but also cursed domain."
        self.fbuffs = {'ATK': 3000}
        self.pbuffs = {}

        # register with clock so @clock.ticker works here
        clock.register(self)

        super().__init__(game)


    @clock.ticker(interval=2, times=3)
    def influence(self):
        """
        update domain state every turn here
        """
        
        logging.info('ticking')
        # current_party: List[GrpgCharacter] = self.players[self.game.player]['party']

        # for chara in current_party:
        #     chara.tick()





