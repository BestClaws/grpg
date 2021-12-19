# core
import math
import logging

# 1st party
from .clock import Token, clock

# 3rd party

# types
from typing import List


class Reactor:

    def __init__(self, chara):
        self.chara = chara
        self.applied_elements: List[Element] = []
        self.do_reactions.inject(self)


    def apply(self,  elem_type: str, fs):
        # TODO: accept an element instead of elem_type
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
            self.applied_elements.append(Element(elem_type, fs))


        self.do_reactions()



    def remove_expired_elems(self):
        # remove expired elements first.
        unexpired_elems = []
        for elem in self.applied_elements:
            if not elem.expired: unexpired_elems.append(elem)
            else: logging.info(f"{elem} expired")

        self.applied_elements = unexpired_elems
    
    @clock.ticker(interval=1) 
    def do_reactions(self):
        """
        performs reactions and outputs 
        
        """

        logging.info(f"{self.chara} doing reactions")
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

        # TODO: fs might be empty. or rather make sure its not empty.
        # when swirl spreads elements, it apply element on others. then the character
        # spreading the element becomes the attacker. so `self.chara`'s formula sheet should be used.
        
        logging.info('dealing with found reactions')

        if reaction == 'vaporize':
            logging.info('setting vap dmg modifiers.')

            procer.fs.a_factor.set(1.5)
            procer.life.expire()
            procable.life.expire()

            self.chara.damages[0] = (
                'vaporize',
                procer.fs.t_dmg_post_res.val
            )
        

        elif reaction == 'reverse vaporize':
            logging.info('setting rev vap dmg modifiers.')
           
            procer.fs.a_factor.set(2.0)
            procer.life.expire()
            procable.life.expire()

            self.chara.damages[0] = (
                'vaporize',
                procer.fs.t_dmg_post_res.val
            )
        

        if reaction == 'melt':
            logging.info('setting melt dmg modifiers.')

            procer.fs.a_factor.set(2.0)
            procer.life.expire()
            procable.life.expire()

            self.chara.damages[0] = (
                'melt',
                procer.fs.dmg_post_res.val
            )
        


        if reaction == 'reverse melt':
            logging.info('setting rev melt dmg modifiers.')

            procer.fs.a_factor.set(1.5)        
            procer.life.expire()
            procable.life.expire()

            self.chara.damages[0] = (
                'melt',
                procer.fs.t_dmg_post_res.val
            )

        
        
        if reaction == 'swirl':
            logging.info('settings swirling')

            procer.life.expire() # anemo goes away.

            procer.fs.t_xer.set(1.2)

            self.chara.damages.append((
                'swirl',
                procer.fs.t_dmg_post_res.val
            ))
        



        # implement other reactions here.


class Element:

    data = {
        'Pyro': {
            'life': 4,
            'procs': {'Hydro': 'vaporize', 'Cryo': 'melt', 'Electro': 'overload'},
        },
        'Hydro': {
            'life': 4,
            'procs': {'Pyro': 'reverse vaporize', 'Cryo': 'freeze'},
        },
        'Cryo': {
            'life': 4,
            'procs': {'Hydro': 'freeze', 'Pyro': 'reverse melt',},
        },
        'Anemo': {
            # 0 as life wont work as 0 as life means its the created token is expired instantly when its created.

            # assuming self.applied_elements is not being externally modified. anemo and geo lifes as 1 makes sense
            # since as as soon as adding them to applied_elements. via apply(), they're sent to do_reactions()
            # for procesing and immediately to deal_reactions() which deals with geo/anemo. and immediately expires it
            # so hopefully. these elements dont linger around (as they are'nt supposed to stay applied on player aka. "aura")

            # no matter if loads of elements are applied to a character from multiple places. they all have to go through
            # apply() which makes sure anemo/geo are expired. immediately after processing them. and then these expired
            # items are subsequently removed.

            # and in worst case scenario (will probably never happen, but fix it, if it does.)
            # the element(geo/anemo) does manage to linger (meaning remains in self.applied_elements)
            # it will be removed at the next tick. so if player turns swaps the lingered elem wont show in ui

            # but if player switches character, the ui updates which will show anemo/geo as lingering element, since
            # switching character wont tick the clock

            'life': 1,
           
            
            'procs': {'Pyro': 'swirl', 'Hydro': 'swirl', 'Cryo': 'swirl', 'Electro': 'swirl'},
        },
        'Geo':{
            'life': 1,
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



    def __init__(self, type, fs=None):
        
        self.type = type
        self.fs = fs
        

        self.life = Token(self.__class__.data[type]['life'])

    def __str__(self):
        return f"{self.type}-{self.life.expires_in}"

        
    def __repr__(self):
        return f"{self.type}-{self.life.expires_in}"

        

    @property
    def expired(self):
        return self.life.expired

        

