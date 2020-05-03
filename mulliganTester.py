from abc import ABC, abstractmethod
import numpy as np

class MulliganTester(ABC):
    def __init__(self):
        self.iterations = 100000
        self.starting_size = 7
        self.mullto = 4
        self.resetCounters()

    @property
    @abstractmethod
    def output_file_header(self):
        pass

    @property
    @abstractmethod
    def hand(self):
        pass

    @property
    @abstractmethod
    def hand_types(self):
        pass

    @property
    def land_value_list(self):
        pass

    @abstractmethod
    def CheckHand(self):
        pass

    def run(self):
        self.runLondon()
        self.printResults("London")
        self.runParis()
        self.printResults("Paris")
        self.runVancouver()
        self.printResults("Vancouver")

    def resetCounters(self):
        self.success = 0.0
        self.tsBreaksKeeper = 0
        self.successAfterDraw = 0

        self.good_counts = np.zeros((self.starting_size + 1) - self.mullto)
        self.hand_counts = np.zeros(((self.starting_size + 1) - self.mullto, len(self.hand_types)))
        self.totals = np.zeros((self.starting_size + 1) - self.mullto)

        self.improvement_after_draw_keeper = np.zeros((self.starting_size + 1) - self.mullto)
        self.improvement_after_draw = [0] * (self.starting_size - self.mullto +1)
        self.good_counts_afterdraw = np.zeros((self.starting_size + 1) - self.mullto)
        self.hand_counts_afterdraw = np.zeros(((self.starting_size + 1) - self.mullto, len(self.hand_types)))

        self.ts_hurt_hand = [0] * (self.starting_size - self.mullto +1)
        self.ts_broke_hand = [0] * (self.starting_size - self.mullto +1)
        self.good_counts_afterTSDraw = np.zeros((self.starting_size + 1) - self.mullto)
        self.hand_counts_afterTSDraw = np.zeros(((self.starting_size + 1) - self.mullto, len(self.hand_types)))
        self.ts_totals = np.zeros((self.starting_size + 1) - self.mullto)

    def runParis(self):
        self.resetCounters()
        for i in range(self.iterations):
            if i % 5000 == 0:
                print(str(i) + " of " + str(self.iterations))

            foundKeeper = False
            tsBrokeKeeper = False
            keeperAfterDraw = False
            for j in range(0,(self.starting_size + 1) - self.mullto):
                size = self.starting_size - j
                self.hand.new_hand(size)

                results = self.CheckHand()
                self.good_counts[size - self.mullto] += (np.sum(results) > 0)
                self.hand_counts[size - self.mullto,:] += results

                self.hand.draw_card()
                resultAfterDraw = self.CheckHand()

                improvedAfterDraw = self.checkImprovement(results, resultAfterDraw)

                self.good_counts_afterdraw[size - self.mullto] += (np.sum(resultAfterDraw) > 0)
                self.hand_counts_afterdraw[size - self.mullto,:] += resultAfterDraw
                self.improvement_after_draw[j] += improvedAfterDraw
                
                if np.sum(resultAfterDraw) > 0:
                    self.thoughtseizedHand()
                    resultAfterTS = self.CheckHand()

                    if np.sum(resultAfterTS) == 0:
                        self.ts_broke_hand[j] += 1
                        self.ts_hurt_hand[j] += 1
                    else:
                        tsHurtHand = self.checkDamageDone(results, resultAfterTS)
                        self.ts_hurt_hand[j] += 1 if tsHurtHand else 0

                    self.good_counts_afterTSDraw[size - self.mullto] += (np.sum(resultAfterTS) > 0)
                    self.hand_counts_afterTSDraw[size - self.mullto,:] += resultAfterDraw
                    self.ts_totals[size - self.mullto] += 1

                self.totals[size - self.mullto] += 1
                
                if np.sum(results) > 0:
                    self.improvement_after_draw_keeper[j] += improvedAfterDraw
                    if foundKeeper and np.sum(resultAfterTS) == 0:
                        tsBrokeKeeper = True
                    foundKeeper = True
                if not keeperAfterDraw and np.sum(resultAfterDraw) > 0:
                    keeperAfterDraw = True
            self.successAfterDraw += keeperAfterDraw
            self.tsBreaksKeeper += tsBrokeKeeper
            self.success += foundKeeper

    def thoughtseizedHand(self):
        self.hand.generate_subset_hands(1, self.land_value_list)
        subResults = []
        for k in range(0, self.hand.num_subsets):
            self.hand.nextSubset()
            subResults.append(self.CheckHand())
        bestIndex = self.getWorstResult(subResults)
        self.hand.chooseSubset(bestIndex)

    def checkDamageDone(self, resultBefore, resultAfter):
        if True in resultBefore:
            if True not in resultAfter:
                return True
            else:
                bestNewRating = np.argmax(resultAfter)
                bestOldRating = np.argmax(resultBefore)
                return bestNewRating > bestOldRating
        else:
            return False

    def getWorstResult(self, results):
        if len(results) == 0:
            return None
        worst = results[0]
        worstHandIndex = np.argmax(worst)
        handIndex = 0
        if True in worst:
            i = 0
            for res in results[1:]:
                if True not in res:
                    worst = res
                    handIndex = i
                    break
                testIndex = np.argmax(res)
                if testIndex > worstHandIndex:
                    worst = res
                    worstHandIndex = testIndex
                    handIndex = i
                i += 1

        return handIndex        

    def getBestResult(self, results):
        best = None
        bestHandIndex = None
        handIndex = None
        i = 0
        for res in results:
            if True in res:
                if best is None:
                    best = res
                    bestHandIndex = np.argmax(best)
                    handIndex = i
                    if bestHandIndex == 0:
                        break
                else:
                    testIndex = np.argmax(res)
                    if testIndex < bestHandIndex:
                        best = res
                        bestHandIndex = testIndex
                        handIndex = i
            i += 1
        if best is None:
            #used for limited
            handIndex = self.pickBestHandSubset()
            if handIndex is not None:
                best = results[handIndex]
            
        return handIndex

    def pickBestHandSubset(self):
        return None

    def runLondon(self):
        self.resetCounters()
        for i in range(self.iterations):
            if i % 5000 == 0:
                print(str(i) + " of " + str(self.iterations))
            foundKeeper = False
            tsBrokeKeeper = False
            keeperAfterDraw = False

            for j in range(0,(self.starting_size + 1) - self.mullto):
                size = self.starting_size - j
                self.hand.new_hand(self.starting_size)
                drawn = False
                #if not testing the 7
                if j > 0:
                    subResults = []
                    self.hand.generate_subset_hands(j)
                    for k in range(0, self.hand.num_subsets):
                        self.hand.nextSubset()
                        subResults.append(self.CheckHand())
                    bestIndex = self.getBestResult(subResults)
                    
                    if bestIndex is None:
                        subAfterDrawResults = []
                        self.hand.subsetIndex = -1
                        drawnCard = self.hand.draw_card()
                        for k in range(0, self.hand.num_subsets):
                            self.hand.nextSubset()
                            self.hand.add_card_to_cur_hand(drawnCard)
                            subAfterDrawResults.append(self.CheckHand())
                        bestIndex = self.getBestResult(subAfterDrawResults)
                        if bestIndex is None:
                            bestIndex = 0
                        self.hand.chooseSubset(bestIndex)
                        self.hand.add_card_to_cur_hand(drawnCard)
                        results = subResults[bestIndex]
                    else:
                        self.hand.chooseSubset(bestIndex)
                        results = subResults[bestIndex]
                        self.hand.draw_card()
                else:
                    results = self.CheckHand()
                    self.hand.draw_card()

                self.good_counts[size - self.mullto] += (np.sum(results) > 0)
                self.hand_counts[size - self.mullto,:] += results

                resultAfterDraw = self.CheckHand()

                improvedAfterDraw = self.checkImprovement(results, resultAfterDraw)

                self.good_counts_afterdraw[size - self.mullto] += (np.sum(resultAfterDraw) > 0)
                self.hand_counts_afterdraw[size - self.mullto,:] += resultAfterDraw
                self.improvement_after_draw[j] += improvedAfterDraw
                
                if np.sum(resultAfterDraw) > 0:
                    self.thoughtseizedHand()
                    resultAfterTS = self.CheckHand()
                    if np.sum(resultAfterTS) == 0:
                        self.ts_broke_hand[j] += 1
                        self.ts_hurt_hand[j] += 1
                    else:
                        tsHurtHand = self.checkDamageDone(results, resultAfterTS)
                        self.ts_hurt_hand[j] += 1 if tsHurtHand else 0

                    self.good_counts_afterTSDraw[size - self.mullto] += (np.sum(resultAfterTS) > 0)
                    self.hand_counts_afterTSDraw[size - self.mullto,:] += resultAfterDraw
                    self.ts_totals[size - self.mullto] += 1

                self.totals[size - self.mullto] += 1
                
                if np.sum(results) > 0:
                    self.improvement_after_draw_keeper[j] += improvedAfterDraw
                    if foundKeeper and np.sum(resultAfterTS) == 0:
                        tsBrokeKeeper = True
                    foundKeeper = True
                if not keeperAfterDraw and np.sum(resultAfterDraw) > 0:
                    keeperAfterDraw = True
            self.successAfterDraw += keeperAfterDraw
            self.tsBreaksKeeper += tsBrokeKeeper
            self.success += foundKeeper

    def runVancouver(self):
        self.resetCounters()
        for i in range(self.iterations):
            if i % 5000 == 0:
                print(str(i) + " of " + str(self.iterations))

            foundKeeper = False
            tsBrokeKeeper = False
            keeperAfterDraw = False
            for j in range(0,(self.starting_size + 1) - self.mullto):
                size = self.starting_size - j
                self.hand.new_hand(size)

                results = self.CheckHand()

                self.good_counts[size - self.mullto] += (np.sum(results) > 0)
                self.hand_counts[size- self.mullto,:] += results

                self.hand.draw_card()
                resultAfterDraw = self.CheckHand()

                improvedAfterDraw = self.checkImprovement(results, resultAfterDraw)
                if j is not 0 and not improvedAfterDraw:
                    #Replace the card drawn in the last operation
                    self.hand.scry_bottom()
                    resultAfterDraw = self.CheckHand()
                    improvedAfterDraw = self.checkImprovement(results, resultAfterDraw)

                self.good_counts_afterdraw[size- self.mullto] += (np.sum(resultAfterDraw) > 0)
                self.hand_counts_afterdraw[size - self.mullto,:] += resultAfterDraw
                self.improvement_after_draw[j] += improvedAfterDraw
                
                if np.sum(resultAfterDraw) > 0:
                    self.thoughtseizedHand()
                    resultAfterTS = self.CheckHand()
                    if np.sum(resultAfterTS) == 0:
                        self.ts_broke_hand[j] += 1
                        self.ts_hurt_hand[j] += 1
                    else:
                        tsHurtHand = self.checkDamageDone(results, resultAfterTS)
                        self.ts_hurt_hand[j] += 1 if tsHurtHand else 0

                    self.good_counts_afterTSDraw[size - self.mullto] += (np.sum(resultAfterTS) > 0)
                    self.hand_counts_afterTSDraw[size - self.mullto,:] += resultAfterDraw
                    self.ts_totals[size - self.mullto] += 1

                self.totals[size - self.mullto] += 1
                
                if np.sum(results) > 0:
                    self.improvement_after_draw_keeper[j] += improvedAfterDraw
                    if foundKeeper and np.sum(resultAfterTS) == 0:
                        tsBrokeKeeper = True
                    foundKeeper = True
                if not keeperAfterDraw and np.sum(resultAfterDraw) > 0:
                    keeperAfterDraw = True
            self.successAfterDraw += keeperAfterDraw
            self.tsBreaksKeeper += tsBrokeKeeper
            self.success += foundKeeper

    def checkImprovement(self, resultBeforeDraw, resultAfterDraw):
        if True in resultAfterDraw:
            if True in resultBeforeDraw:
                bestNewRating = np.argmax(resultAfterDraw)
                bestOldRating = np.argmax(resultBeforeDraw)
                return bestNewRating < bestOldRating
            else:
                return True
        else:
            return False

    def printResults(self, header):
        p_good = self.good_counts / self.totals
        p_hands = self.hand_counts / self.totals.reshape((self.starting_size + 1) - self.mullto,1)
        p_success = self.success / self.iterations
        p_successAfterDraw = self.successAfterDraw / self.iterations
        p_drawImprovement = [x / self.iterations for x in self.improvement_after_draw]

        p_good_afterDraw = self.good_counts_afterdraw / self.totals
        p_hands_afterDraw = self.hand_counts_afterdraw / self.totals.reshape((self.starting_size + 1) - self.mullto,1)

        p_good_afterTS = self.good_counts_afterTSDraw / self.ts_totals
        p_hands_afterTS = self.hand_counts_afterTSDraw / self.ts_totals.reshape((self.starting_size + 1) - self.mullto,1)

        p_TS_hurt = [x / self.iterations for x in self.ts_hurt_hand]
        p_TS_broke = [x / self.iterations for x in self.ts_broke_hand]

        p_TS_broke_keeper = self.tsBreaksKeeper / self.success

        print(p_good)
        print(np.flip(p_hands, axis = 0))
        print(p_drawImprovement)
        print(p_success)

        filename = "output/" + self.output_file_header + "_" + header+".csv"
        with open(filename, "w") as file:
            file.write(header + " - ")
            file.write(str(self.iterations) + " iterations\n\n")

            self.writeHandTypesToFile(file, p_good, p_hands)

            file.write("\n\nAfter Draw""\n")
            self.writeHandTypesToFile(file, p_good_afterDraw, p_hands_afterDraw)

            file.write("\n\nAfter Draw & Thoughtseize""\n")
            self.writeHandTypesToFile(file, p_good_afterTS, p_hands_afterTS)

            file.write("\n")
            file.write("p of good hand by " + str(self.mullto) + "\n")
            file.write(str(p_success) + "\n")
            file.write("p of improvement after draw\n")
            for size in range(7,self.mullto-1,-1):
                file.write(str(size) + ",")
            file.write("\n")
            file.write(str(p_drawImprovement) + "\n")
            file.write("p of good hand after draw\n")
            file.write(str(p_successAfterDraw) + "\n\n")
            file.write("Thoughtseize Probabilities\n")
            for size in range(7,self.mullto-1,-1):
                file.write(str(size) + ",")
            file.write("Hurt Keepable Hand\n")
            file.write(str(p_TS_hurt) + "\n")
            file.write("Broke Keepable Hand\n")
            file.write(str(p_TS_broke) + "\n")
            file.write("Broke Kept hand\n")
            file.write(str(p_TS_broke_keeper) + "\n")
            file.close()


    def writeHandTypesToFile(self, file, p_good, p_hands):
        file.write("Probabilities of good hands:\n")
        for size in range(self.mullto,8):
            file.write(str(size) + ",")
        file.write("\n")
        for p in p_good:
            file.write(str(p) + ",")
        file.write("\n\n")

        # hand type headers
        file.write("hand sizes/types,")
        for type in self.hand_types:
            file.write(str(type) + ",")

        #results
        file.write("\n")
        for size in reversed(range(len(p_hands))):
            file.write(str(size + self.mullto) + ",")
            for p in p_hands[size,:]:
                file.write(str(p) + ",")
            file.write("\n")