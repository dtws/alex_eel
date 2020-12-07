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
            ("C", "E", 1),
            ("E", "F", 1),
            ("D", "F", 1),
            ("D", "G", 1),
            ("F", "G", 1),
            ("F", "H", 1),
        ], "A", "H")
        print(res)
        self._assertDictsEqual(res,
                               {
                                   "currents": [
                                       0.32544378698224863,
                                       0.1420118343195267,
                                       0.18343195266272194,
                                       0.10059171597633143,
                                       -0.059171597633136175,
                                       0.041420118343195256,
                                       0.16568047337278113,
                                       0.10650887573964496,
                                       0.053254437869822535,
                                       -0.053254437869822424,
                                       0.3254437869822483
                                   ],
                                   "equivalent_resistance": 3.072727272727275,
                                   "voltages": {
                                       "B": 0.32544378698224863,
                                       "C": 0.4674556213017753,
                                       "D": 0.5680473372781067,
                                       "E": 0.5088757396449706,
                                       "F": 0.6745562130177517,
                                       "G": 0.6213017751479293
                                   }
                               }
                               )
