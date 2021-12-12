# core
import math
import logging

# 1st party
from .clock import Token, clock

# 3rd party

# type imports
from typing import List


class Reactor:
    def __init__(self, chara):
        self.chara = chara
        self.applied_elements: List[Element] = []
        self.do_reactions.inject(self)

        pass

    def apply(self,  elem_type: str, em):

        # clean up expired elements
        self.remove_expired_elems()

        
        if elem_type not in [
            'Electro', 'Pyro', 'Hydro', 'Cryo', 'Anemo', 'Geo', 'Dendro'
        ]:
            raise Exception("Invalid element applied")
        
        # refresh element life, if current applying element is same as last applied element
        if self.applied_elements and self.applied_elements[-1].type == elem_type:
            self.applied_elements[-1].life.refresh()
        else:
            self.applied_elements.append(Element(elem_type, em))


        self.do_reactions()



    def remove_expired_elems(self):
        # remove expired elements first.
        unexpired_elems = [elem for elem in self.applied_elements if not elem.expired]
        self.applied_elements = unexpired_elems
    
    @clock.ticker(interval=1) 
    def do_reactions(self):
        """
        performs reactions and outputs 
        
        """
        # remove expired elements first.
        self.remove_expired_elems()

        # walk through each element from left to right and try reacting that element
        # with all the elements to its left.
        for i, procing in enumerate(self.applied_elements):

            # ignore elements that might have expired in previous iterations of this loop
            # ignoring them instead of removing, cuz that'll mess up iteration
            # (never mutate a list while iterating)
            procables = [elem for elem in self.applied_elements[:i] if not elem.expired]

            for procable in procables:
                reaction = Element.data[procing.type]['procs'].get(procable.type)
                if reaction is None: continue
                self.deal_reactions(procing, procable, reaction)    


        # clean up again.
        self.remove_expired_elems()



    def deal_reactions(self, procer, procable, reaction):
        
        logging.info('dealing with found reactions')

        if reaction == 'vaporize':
            logging.info('setting vap dmg modifiers.')
            self.chara.fs.amplification.set(1.5 * (1 + 0.00189266831 * procer.EM * math.exp(-0.000505 * procer.EM)))
            procer.life.expire()
            procable.life.expire()

        elif reaction == 'rev vaporize':
            logging.info('setting rev vap dmg modifiers.')
            self.chara.fs.amplification.set(2.0 * (1 + 0.00189266831 * procer.EM * math.exp(-0.000505 * procer.EM)))

            procer.life.expire()
            procable.life.expire()

        if reaction == 'melt':
            logging.info('setting melt dmg modifiers.')
            self.chara.fs.amplification.set(2.0 * (1 + 0.00189266831 * procer.EM * math.exp(-0.000505 * procer.EM)))
            procer.life.expire()
            procable.life.expire()


        if reaction == 'rev melt':
            logging.info('setting rev melt dmg modifiers.')
            self.chara.fs.amplification.set(1.5 * (1 + 0.00189266831 * procer.EM * math.exp(-0.000505 * procer.EM)))
            procer.life.expire()
            procable.life.expire()

        # implement other reactions here.


class Element:

    data = {
        'Pyro': {
            'life': 4,
            'procs': {'Hydro': 'vaporize', 'Cryo': 'melt',  'Anemo': 'swirl', 'Electro': 'overload'},
        },
        'Hydro': {
            'life': 4,
            'procs': {'Pyro': 'rev vaporize', 'Cryo': 'freeze', 'Anemo': 'swirl'},
        },
        'Cryo': {
            'life': 4,
            'procs': {'Hydro': 'freeze', 'Pyro': 'rev melt', 'Anemo': 'swirl'},
        },
        'Anemo': {
            'life': 4,
            'procs': {'Pyro': 'swirl', 'Hydro': 'swirl', 'Cryo': 'swirl', 'Electro': 'swirl'},
        },
        'Geo':{
            'life': 4,
            'procs': {'Pyro': 'crystallize', 'Hydro': 'crystallize', 'Cryo': 'crystallize', 'Electro': 'crystallize'},
        },
        'Electro': {
            'life': 4,
            'procs': {'Pryo': 'overload', 'Hydro': 'electrocharged', 'Cryo': 'superconduct'},
        },
        'Dendro': {
            # DENDRO WHEN :peepoSad:
        }
    }



    def __init__(self, type, EM=0):
        self.type = type
        self.EM = EM

        self.life = Token(self.__class__.data[type]['life'])

    def __str__(self):
        return f"{self.type}-{self.life.expires_in}"

        
    def __repr__(self):
        return f"{self.type}-{self.life.expires_in}"

        

    @property
    def expired(self):
        return self.life.expired