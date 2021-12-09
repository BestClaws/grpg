from .compute import E

class FormulaeStore:

    def __init__(self, chara):


        # OUTGOING

        self.chara = chara

        self.ability_xer = E(0) # SHOULD BE UPDATED WHEN USING ABILITIES. FIND A WAY TO ENFORCE THIS.
        self.ability_dmg = chara.sm.stats['ATK'] * self.ability_xer
        self.dmg_post_bonus = self.ability_dmg * 1 # no dmg bonuses applied. ( there should be some though.)
        self.critical_hit = E(0)
        self.dmg_post_crit = self.dmg_post_bonus * ((chara.sm.stats['Crit DMG'] * self.critical_hit) + 1)

        # INCOMING

        self.dmg_in = E(0)

        self.final_res = E(1) #  SHOULD BE UPDATED WHEN TAKING A HIT. FIND A WAY TO ENFORCE THIS.


        if self.final_res.val < 0:
            self.post_res_dmg = self.dmg_in * (-(self.final_res/2) + 1)
        elif 0 <= self.final_res.val < 0.75:
            self.post_res_dmg = self.dmg_in * (E.sub(0, self.final_res) + 1)
        elif self.final_res.val >= 0.75:
            self.post_res_dmg = self.dmg_in * E.div(1, (self.final_res * 4)+1)

        self.amplification = E(1) # MAY BE UPDATED WITH REACTOR.
        
        self.final_dmg = self.post_res_dmg * self.amplification