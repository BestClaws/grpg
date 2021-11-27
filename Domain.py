import json
import logging

from Kaeya import Kaeya

class Domain:
    """
    Reprsents a Domain as defined by Genshin.
    Acts as an Environment/Stage where parties join and fight.
    Influences the battle by buffing/debuffing characters.
    """

    def __init__(self, game, name="Zhou"):
        self.game = game

        # load all domains' data
        with open('assets/domains.json') as f:
            self.data = json.load(f)[name]


        self.buffs = self.data['buffs']

        logging.info(f"picked {self.data['fullname']} domain")
        logging.info(f'domain buffs: {self.buffs}')


        # stores party charas and party meta data.
        self.parties = {
            "A": {
                "charas": [],
                "onfield": 0
            },
            "B": {
                "charas": [],
                "onfield": 0
            }
        }


    def add_party(self, party_name, *charas):
        """creates a party of characters for the specified team [A/B]"""

        if party_name not in ["A", "B"]:
            raise Exception("invalid team name")

        if len(charas) != 2:
            raise("team supports exactly two characters")


        for chara in charas:
            # validate team member
            logging.info(self.buffs)
            chara = Kaeya(domain=self, party_name=party_name)
            self.parties[party_name]["charas"].append(chara)


    def influence(self):
        """
        Applies all buffs/debuffs to all party members
        Influences in other ways (hp bleed etc., Not yet implemented)
        """
        logging.info('influencing')
        charasA = self.parties["A"]["charas"]
        charasB = self.parties["B"]["charas"]

        for chara in charasA + charasB:
            chara.apply_buffs(self.buffs)



# test code only.
if __name__ == "__main__":
    d = Domain("Zhou")
