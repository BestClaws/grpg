# TODO: improve overall naming!!!!


from .compute import E

class FormulaeStore:

    def __init__(self, chara):


        ############ OUTGOING



        self.chara = chara

        self.ability_xer = E(0) # SHOULD BE UPDATED WHEN USING ABILITIES. FIND A WAY TO ENFORCE THIS.
        self.ability_dmg = chara.sm.stats['ATK'] * self.ability_xer
        self.dmg_post_bonus = self.ability_dmg * 1 # no dmg bonuses applied. ( there should be some though.)
        self.critical_hit = E(0)
        self.dmg_post_crit = self.dmg_post_bonus * ((chara.sm.stats['Crit DMG'] * self.critical_hit) + 1)




        ########### INCOMING

        self.dmg_in = E(0)
        self.attacker_level = E(0)
        
        # self.defense_reduction = E(0)
        # self.def_post_reduction = chara.sm.stats['DEF'] * E.sub(1, self.defense_reduction)

        self.dmg_post_def = self.dmg_in * (  
            E.sub(1, chara.sm.stats['DEF'] / (chara.sm.stats['DEF'] + self.attacker_level * 5 + 500))  
        )

        # the effective_res for the given element
        self.effective_res = E(1) #  SHOULD BE UPDATED WHEN TAKING A HIT. FIND A WAY TO ENFORCE THIS.


        if self.effective_res.val < 0:
            self.dmg_post_res = self.dmg_post_def * E.sub(1, self.effective_res/2) 
        elif 0 <= self.effective_res.val < 0.75:
            self.dmg_post_res = self.dmg_post_def * E.sub(1, self.effective_res)
        elif self.effective_res.val >= 0.75:
            self.dmg_post_res = self.dmg_post_def * E.div(1, self.effective_res * 4 + 1)

        self.amplification = E(1) # MAY BE UPDATED WITH REACTOR.
        
        self.final_dmg = self.dmg_post_res * self.amplification