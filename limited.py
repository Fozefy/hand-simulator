import numpy as np
from hand import Hand
from mulliganTester import MulliganTester

class LimitedMullTester(MulliganTester):

    hand_types = ["PerfectCurve", "GoodCurve","keepable"]
    hand = Hand("decklists/limited.txt")
    output_file_header = "limited"
    land_value_list = ["primaryland", "secondaryland"]
    
    def __init__(self):
        MulliganTester.__init__(self)
        self.cheapPrimarySpells = ["primary12cc", "primary3cc", "primary4cc"]
        self.cheapSecondarySpells = ["secondary12cc", "secondary3cc", "secondary4cc"]
        self.primaryland = ["primaryland"]
        self.secondaryland = ["secondaryland"]
        self.twoDrop = ["primary12cc", "secondary12cc"]
        self.threeDrop = ["primary3cc", "secondary3cc"]
        self.playByThree = ["primary12cc", "secondary12cc", "primary3cc", "secondary3cc"]

    def CheckHand(self):
        numPrimaryLand = self.hand.count_of(self.primaryland)
        numSecondaryland = self.hand.count_of(self.secondaryland)
        numLands = numPrimaryLand + numSecondaryland
        bothColours = numPrimaryLand > 0 and numSecondaryland > 0
        numTwoDrop = self.hand.count_of(self.twoDrop)
        numThreeDrop = self.hand.count_of(self.threeDrop)
        numEarlyPlay = numTwoDrop + numThreeDrop
        numCheapPrimary = self.hand.count_of(self.cheapPrimarySpells)
        numCheapSecondary = self.hand.count_of(self.cheapSecondarySpells)

        numSpells = self.hand.handsize() - numLands

        PerfectCurve = False
        GoodCurve = False
        keepable = False

        if numSpells >= 4 and bothColours and numTwoDrop > 0 and numEarlyPlay > 1:
            PerfectCurve = True
        elif numSpells - numLands >= 3 and bothColours and self.playByThree:
            if numLands == 2 and numTwoDrop == 0:
                keepable = True
            else:
                GoodCurve = True
        elif numSpells - numLands >= 2 and self.playByThree and ((numPrimaryLand > 0 and numCheapPrimary > 0) or (numSecondaryland > 0 and numCheapSecondary > 0)) :
            keepable = True

        results = np.array([PerfectCurve, GoodCurve, keepable])

        return results

if __name__ == "__main__":
    limitedTester = LimitedMullTester()
    limitedTester.run() 