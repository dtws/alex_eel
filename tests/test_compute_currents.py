"""===============================================================================

        FILE: tests/test_compute_currents.py

       USAGE: (not intended to be directly executed)

 DESCRIPTION: 

     OPTIONS: ---
REQUIREMENTS: ---
        BUGS: ---
       NOTES: ---
      AUTHOR: Alex Leontiev (nailbiter@dtws-work.in)
ORGANIZATION: Datawise Inc.
     VERSION: ---
     CREATED: 2020-12-07T15:18:10.226835
    REVISION: ---

==============================================================================="""
import logging
import unittest
from alex_eel import compute_currents
import json


class TestComputeCurrents(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)

    def _assertDictsEqual(self, d1, d2):
        self.assertEqual(*[json.dumps(d, sort_keys=True)for d in [d1, d2]])

    def test_compute_currents(self):
        res = compute_currents([("A", "B", 10)], "A", "B", voltage=10)
        # print(res)
        self._assertDictsEqual(
            res, {"currents": [1.0], "voltages": {}, "equivalent_resistance": 10.0})

    def test_compute_currents_2(self):
        res = compute_currents(
            [("A", "B", 1), ("B", "C", 1)], "A", "C", voltage=10)
        # print(res)
        self._assertDictsEqual(res, {'currents': [5.0, 5.0], 'voltages': {
                               'B': 5.0}, "equivalent_resistance": 2.0})

    def test_compute_currents_3(self):
        res = compute_currents(
            [("A", "B", 1), ("A", "B", 1)], "A", "B", voltage=10)
        # print(res)
        self._assertDictsEqual(
            res, {'currents': [10.0, 10.0], 'voltages': {}, "equivalent_resistance": 0.5})

    def test_compute_currents_4(self):
        res = compute_currents([
            ("A", "B", 1),
            ("B", "C", 1),
            ("B", "E", 1),
            ("C", "D", 1),
            ("D", "E", 1),
            ("E", "D", 1),
            ("E", "F", 1),
            ("D", "F", 1),
            ("D", "G", 1),
            ("F", "G", 1),
            ("F", "H", 1),
        ], "A", "H")
        # print(res)
        self._assertDictsEqual(res, {
            'currents': [
                0.3235294117647059, 
                0.11764705882352938, 
                0.20588235294117657, 
                0.11764705882352944, 
                -0.02941176470588225, 
                0.02941176470588225, 
                0.14705882352941158, 
                0.11764705882352933, 
                0.05882352941176472, 
                -0.05882352941176461,
                0.32352941176470595
            ], 
            'voltages': {
                'B': 0.3235294117647059, 
                'C': 0.4411764705882353, 
                'D': 0.5588235294117647, 
                'E': 0.5294117647058825, 
                'F': 0.676470588235294, 
                'G': 0.6176470588235294
            }, 
            'equivalent_resistance': 3.0909090909090904
        })
