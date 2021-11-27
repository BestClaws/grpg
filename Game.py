import json
import time
import logging


import log_config

from GrpgCharacter import GrpgCharacter
from collections import deque
from event import Event

from Domain import Domain

class Game:
    """Represents and holds the entire state of the game."""
    
    def __init__(self):
        logging.info("starting game")
        self.turn = "A"
        self.idle = "B"

        self.domain = None
        self.swap = False
        self.events = deque([])


    def pick_domain(self, name):
        """select a domain (arena) for the game"""
        self.domain = Domain(name)

    def swap_turn(self):
        """swap player turns"""
        if self.turn == "A":
            self.turn = "B"
            self.idle = "A"
        else:
            self.turn = "A"
            self.idle = "B"

        logging.info(f"it's {self.turn}'s turn now, {self.idle} is idle.")

    def main_loop(self):
        self.domain.influence()
        self.handle_events()
        

        # clear all buffs
        for chara in self.domain.parties['A']['charas']:
            chara.clear_buffs()
        for chara in self.domain.parties['B']['charas']:
            chara.clear_buffs()
        
        # swap turn if necessary.
        if self.swap:
            self.swap_turn()
            self.swap = not self.swap

        yield


    def handle_events(self):
        """handle all game events"""

        
        # process all events until queue is empty.
        while len(self.events) != 0:
            e = self.events.popleft()


            party = self.domain.parties[self.turn]
            active_chara: GrpgCharacter = party['charas'][party['onfield']]
                

            ## HANDLE INPUTS            
            # handle auto attack input
            if e.type == Event.ACTION_AUTO:
                active_chara.invoke_auto()
                self.swap = True
                

            # handle charge attack input 
            elif e.type == Event.ACTION_CHARGE:
                active_chara.invoke_charge()
                self.swap = True

            # handle elemental skill input
            elif e.type == Event.ACTION_SKILL:
                active_chara.invoke_skill()
                self.swap = True

            # handle elemental burst input
            elif e.type == Event.ACTION_BURST:
                active_chara.invoke_burst()
                self.swap = True

            # handle character switch input 
            # (change onfield character)
            elif e.type == Event.ACTION_SWITCH:
                party['onfield'] = e.val
                # logging.info(f"I {party['onfield']} from {self.turn} take the field")
                
                # emit focus and blur events for all characters in party.
                for i in range(len(party['charas'])):
                    if i == party['onfield']:
                        self.events.append(Event(Event.CHARA_TAKES_FIELD, i))
                    else:
                        self.events.append(Event(Event.CHARA_LEAVES_FIELD, i))


            elif e.type == Event.CHARA_TAKES_FIELD:
                focus_target = e.val
                party['charas'][focus_target].take_field()

            elif e.type == Event.CHARA_LEAVES_FIELD:
                blur_target = e.val
                party['charas'][blur_target].leave_field()
        
        


if __name__ == "__main__":
    
    # setup game
    game = Game()
    game.pick_domain("Zhou")
    game.domain.add_party("A", "kaeya", "kaeya")
    game.domain.add_party("B", "kaeya", "kaeya")
    
    game.main_loop().__next__()

  

    
    while True:
        key = input("enter value:")
        if key == 'a':
            game.events.append(Event(Event.ACTION_AUTO))
        elif key == 'c':
            game.events.append(Event(Event.ACTION_CHARGE))
        elif key == '1':
            game.events.append(Event(Event.ACTION_SWITCH, 1))
        elif key == '2':
            game.events.append(Event(Event.ACTION_SWITCH, 1))


        game.main_loop().__next__()

        logging.info("...................")
        logging.info(game.turn)
        logging.info("...................")
