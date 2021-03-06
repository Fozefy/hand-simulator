import numpy as np
from hand import Hand
from mulliganTester import MulliganTester

class KarnTronMullTester(MulliganTester):

    hand_types = ["T3KarnGG", "Tron+payoff", "Tron", "solid_keep"]
    hand = Hand("decklists/karn_tron.txt")
    output_file_header = "karntron"
    land_value_list = ["Wastes", "Forest", "Urza's Power Plant", "Urza's Tower", "Urza's Mine"]

    def __init__(self):
        MulliganTester.__init__(self)
        self.green_source = ["Forest", "Chromatic Sphere", "Chromatic Star"]
        self.tron1 = ["Urza's Power Plant"]
        self.tron2 = ["Urza's Tower"]
        self.tron3 = ["Urza's Mine"]
        self.stir = ["Ancient Stirrings"]
        self.sylv = ["Sylvan Scrying"]
        self.exmap = ["Expedition Map"]
        self.payoff = ["Walking Ballista", "Karn Liberated", "Wurmcoil Engine", "Ugin, the Spirit Dragon"]
        self.karn = ["Karn Liberated"]
        self.cantrips = ["Chromatic Sphere", "Chromatic Star", "Relic of Progenitus"]
        self.ostone = ["Oblivion Stone"]

    def CheckHand(self):
        #print("")
        #print (hand.hand_as_str())

        hand = self.hand

        numTron = hand.contains(self.tron1) + hand.contains(self.tron2) + hand.contains(self.tron3)
        hasGreen = hand.contains(self.green_source)
        numStir = hand.count_of(self.stir) if hasGreen else 0
        numPayoff = hand.count_of(self.payoff)
        hasKarn = hand.contains(self.karn)
        tronFinders = hand.count_of(self.exmap) + hand.count_of(self.sylv) if hasGreen else 0
        numLand = hand.count_of(self.land_value_list)
        numCantrips = hand.count_of(self.cantrips) + numStir
        hasOStone = hand.contains(self.ostone)

        t3karnGG = False
        tronWPayoff = False
        justTron = False
        keepable = False

        if numTron >= 1 and numLand >= 2 and numTron + tronFinders >= 3:
            if hasKarn:
                t3karnGG = True
            elif numPayoff > 0:
                tronWPayoff = True
            else:
                justTron = True
        elif numLand >= 2 and numCantrips >= 2 and (numPayoff >= 1 or hasOStone):
            keepable = True
        elif numLand >= 1 and (numCantrips > 2 or (numCantrips >= 1 and numTron + tronFinders >= 3)):
            keepable = True

        results = np.array([t3karnGG, tronWPayoff, justTron, keepable])
        #print(str (results))
        return results

if __name__ == "__main__":
    karnTester = KarnTronMullTester()
    karnTester.run() 