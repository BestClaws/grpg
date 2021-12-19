# TODO: improve overall naming!!!!

import math
from copy import deepcopy

from .compute import E

class FormulaSheet:

    def __init__(self, chara):

        
        self.chara = chara
        self.element = 'Physical'

        ########################################################################
        # OUTGOING
        ########################################################################

        ## UPDATABLE PARAMS

        self.talent_xer = E(0)

        ## END UPDATABLE PARAMS
 


        self.talent_dmg = chara.sm.stats['ATK'] * self.talent_xer
        self.dmg_post_bonus = self.talent_dmg * 1 # no dmg bonuses applied. ( there should be some though.)
        self.critical_hit = E(0)
        self.dmg_post_crit = self.dmg_post_bonus * ((chara.sm.stats['Crit DMG'] * self.critical_hit) + 1)




        ########################################################################
        # INCOMING
        ########################################################################


        ## UPDATABLE PARAMS

        self.atkr_EM = self.chara.sm.stats['Elemental Mastery']
        self.atkr_lvl = self.chara.sm.inherent['Level']
        self.res = E(1) # the res for the given element, should be updated via `update()`

        ## END UPDATABLE PARAMS

        self.dmg_in = E(0)


        self.dmg_post_def = (self.dmg_in *   
            (E.sub(1, chara.sm.stats['DEF'] / (chara.sm.stats['DEF'] + self.atkr_lvl * 5 + 500))))

      
        self.dmg_post_res = E(0)



        self.a_factor = E(1)
        self.a_coeff = E(1)

        self.final_dmg = self.dmg_post_res * self.a_factor * self.a_coeff


        ### TRANSFORMATIVE REACTIONS ------------------------------------------

        # transformative constants.
        self.t_xer = E(0)
   

        EM_bonus = (self.atkr_EM * 16)/(self.atkr_EM + 2000) + 1

        self.t_dmg = self.t_xer * EM_bonus * ( # 60+ chara only.
             0.00194 * math.pow(self.atkr_lvl, 3)
           - 0.319 * math.pow(self.atkr_lvl, 2)
           + 30.7 * self.atkr_lvl - 868
        )

        self.t_dmg_post_res = E(0)

    

    # fuck this method. and fuck you.
    def refresh(self):
        """
        call when updating attributes that are used in split functions
        (Exhaustive list: res,)
        """

        # dmg after resistance (how tf do i write discountinous functions as expressions)
        if self.res.val < 0:
            self.dmg_post_res.equals(self.dmg_post_def * E.sub(1, self.res/2))
        elif 0 <= self.res.val < 0.75:
            self.dmg_post_res.equals(self.dmg_post_def * E.sub(1, self.res))
        elif self.res.val >= 0.75:
            self.dmg_post_res.equals(self.dmg_post_def * E.div(1, self.res * 4 + 1))

        # t dmg after resistance
        if self.res.val < 0:
            self.t_dmg_post_res.equals(self.t_dmg * E.sub(1, self.res/2))
        elif 0 <= self.res.val < 0.75:
            self.t_dmg_post_res.equals(self.t_dmg * E.sub(1, self.res))
        elif self.res.val >= 0.75:
            self.t_dmg_post_res.equals(self.t_dmg * E.div(1, self.res * 4 + 1))

        # math.exp made me come here. bummer
        a_coeff = (1 + 0.00189266831 * self.atkr_EM.val * math.exp(-0.000505 * self.atkr_EM.val)) or 1
        self.a_coeff.set(a_coeff)



    def __get__(self):
        """
        pepega moment
        why make the compute module/Expression class in the first place when you can use this
        """
        print('refreshing FS...')
        self.refresh()
        



    def copy(self):
        """
        gives a clean copy of sheet. that has not been modified.
        (will still reflect the stats.)
        """
        return FormulaSheet(self.chara)

    



    def clone(self):
        """
        creates a copy of the current state of the formula sheet.
        """
        new = self.get_copy()

        new.talent_xer.set(self.talent_xer.val)
        
        new.atr_EM.set(self.atr_EM.val)
        new.atkr_lvl.set(self.atkr_lvl.val)
        new.res.set(self.res.val)

        new.t_a.set(self.t_xer.val)

        return new




    def prepo(self, *, talent_xer):
        """
        prepares sheet for outgoing dmg
        """
        ...


    def prepi(self, * atr_EM, atkr_lvl):
        """
        prepares sheet for calculating incoming dmges
        """
        ...
    
    def prept(self, *, a, b, c, d, e, f):
        """
        Sets the transformative constants
        """
        self.t_a.set(a)
        self.t_b.set(b)
        self.t_c.set(c)
        self.t_d.set(d)
        self.t_e.set(e)
        self.t_f.set(f)