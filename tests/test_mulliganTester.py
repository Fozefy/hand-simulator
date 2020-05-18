import pytest
from hand import Hand
from mulliganTester import MulliganTester

class TestMullTester(MulliganTester):
    hand = Hand("tests/testdeck.txt")
    hand_types = ["testtype1","testtype2"]
    land_value_list = []
    output_file_header = "test"

    def __init__(self):
        MulliganTester.__init__(self)
        self.iterations = 100

    def CheckHand(self):
        return [0,1]

def test_init():
    tester = TestMullTester()
    assert tester.iterations == 100
    assert tester.success == 0.0

def test_runLondon():
    #Very simple test just to ensure we execute
    tester = TestMullTester()
    tester.runLondon()
    assert all(x == 100 for x in tester.totals)

def test_runVancouver():
    #Very simple test just to ensure we execute
    tester = TestMullTester()
    tester.runVancouver()
    assert all(x == 100 for x in tester.totals)

def test_runParis():
    #Very simple test just to ensure we execute
    tester = TestMullTester()
    tester.runParis()
    assert all(x == 100 for x in tester.totals)