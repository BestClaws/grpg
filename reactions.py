import math

import logging

from .clock import Token, clock

class Reactor:
    def __init__(self, chara):
        self.chara = chara
        self.applied_elements = []
        self.do_reactions.inject(self)

        pass

    def apply(self,  elem_type: str, em):
        self.remove_expired_elems()

        if elem_type == 'Physical':
            logging.info('not applying physical - not an element')
            return
        
        elif elem_type not in [
            'Electro', 'Pyro', 'Hydro', 'Cryo', 'Anemo', 'Geo', 'Dendro'
        ]:
            raise Exception("Invalid element applied")
        
        # remove element if already applied. to apply same elem, but with full life.
        if self.applied_elements and self.applied_elements[-1].type == elem_type:
            del self.applied_elements[-1]

        self.applied_elements.append(Element(elem_type, em))


        self.do_reactions()



    def remove_expired_elems(self):
        # remove expired elements first.
        for elem in self.applied_elements:
            if elem.expired:
                logging.info(f"removing expired item: {elem}")
                self.applied_elements.remove(elem)

    
    @clock.ticker(interval=1) 
    def do_reactions(self):
        """
        performs reactions and outputs 
        
        """

        self.remove_expired_elems()

        




        logging.info(f"{self.chara}: doing reactions")
     
        # amplifying reactions

        if not self.applied_elements: return

        elem_types = [elem.type for elem in self.applied_elements]
        EM = self.applied_elements[-1].EM

        if elem_types[-2:] == ['Hydro', 'Pyro']:
            # vap
            self.chara.fs.amplification.set(1.5 * (1 + 0.00189266831 * EM * math.exp(-0.000505 * EM)))
            self.applied_elements[-2:] = []
            pass

        if elem_types[-2:] == ['Pyro', 'Hydro']:
            # reverse vap
            self.chara.fs.amplification.set(2.0 * (1 + 0.00189266831 * EM * math.exp(-0.000505 * EM)))
            self.applied_elements[-2:] = []
            pass

        if elem_types[-2:] == ['Cryo', 'Pyro']:
            # melt
            self.chara.fs.amplification.set(2.0 * (1 + 0.00189266831 * EM * math.exp(-0.000505 * EM)))
            self.applied_elements[-2:] = []
            pass

        if elem_types[-2:] == ['Pyro', 'Cryo']:
            # rev melt
            self.chara.fs.amplification.set(1.5 * (1 + 0.00189266831 * EM * math.exp(-0.000505 * EM)))
            self.applied_elements[-2:] = []
            pass



        if set(self.applied_elements[-2:]) == set(['Hydro', 'Electro']):
            # Electro-charged
            pass

        if set(self.applied_elements[-2:]) == set(['Electro', 'Pyro']):
            # overload
            pass

        if self.applied_elements[-2:] == set(['Cryo', 'Electro']):
            # superconduct
            # reduce res
            pass

        if self.applied_elements[-2:] == set(['Cryo', 'Hydro']):
            # frozen
            # reapply Cryo
            pass


        
        

class Element:

    def __init__(self, type, EM=0):
        self.type = type
        self.EM = EM
        
        _life_table = {
            'Pyro': 4,
            'Hydro': 0,
            'Cryo': 0,
            'Anemo': 0,
            'Geo': 0,
            'Electro': 0,
            'Dendro': 0,
        }

        self.life = Token(_life_table.get(type))

    def __str__(self):
        return f"{self.type}"

        
    def __repr__(self):
        return f"{self.type}"

        

    @property
    def expired(self):
        return self.life.expired