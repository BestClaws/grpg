import json
from GrpgCharacter import GrpgCharacter
from collections import deque
from event import Event
from logger import log
from Domain import Domain

class Game:
    """Represents and holds the entire state of the game."""
    
    def __init__(self):
        log.info("starting game")
        self.turn = "A"
        self.idle = "B"

        self.domain = Domain("Zhou")
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

    def main_loop(self):
        self.domain.influence()
        self.handle_events()
        yield


    def handle_events(self):
        """handle all game events"""
        while len(self.events) != 0:
            e = self.events.popleft()

            active_chara: GrpgCharacter = self.domain.parties[self.turn]['charas'][0]
                

            if e.type == Event.ACTION_AUTO:
                active_chara.invoke_auto()
                self.swap_turn()

            elif e.type == Event.ACTION_CHARGE:
                active_chara.invoke_charge()
                self.swap_turn()


            elif e.type == Event.ACTION_SKILL:
                active_chara.invoke_skill()
                self.swap_turn()

            elif e.type == Event.ACTION_BURST:
                active_chara.invoke_burst()
                self.swap_turn()

            elif e.type == Event.ACTION_SWITCH:
                switch_target = e.val
                charas = self.domain.parties[self.turn]['charas']
                
                for i in range(len(charas)):
                    if i == switch_target:
                        self.events.append(Event(Event.CHARA_FOCUS, i))
                    else:
                        self.events.append(Event(Event.CHARA_BLUR, i))

            elif e.type == Event.CHARA_FOCUS:
                active_chara.focus()
            elif e.type == Event.CHARA_BLUR:
                active_chara.blur()


g = None

if __name__ == "__main__":
    
    # setup game
    game = Game()
    game.pick_domain("Zhou")
    game.domain.add_party("A", "kaeya", "kaeya")
    game.domain.add_party("B", "kaeya", "kaeya")
    
    # handle input.
    game.events.append(Event(Event.ACTION_AUTO))


    game.events.append(Event(Event.ACTION_SWITCH, 1))
    game.main_loop().__next__()

    g = game