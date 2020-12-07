"""===============================================================================

        FILE: /Users/nailbiter/Documents/datawise/alex_eel/tests/test_print_chain.py

       USAGE: (not intended to be directly executed)

 DESCRIPTION: 

     OPTIONS: ---
REQUIREMENTS: ---
        BUGS: ---
       NOTES: ---
      AUTHOR: Alex Leontiev (nailbiter@dtws-work.in)
ORGANIZATION: Datawise Inc.
     VERSION: ---
     CREATED: 2020-12-07T13:55:58.204497
    REVISION: ---

==============================================================================="""
import logging
import unittest
from alex_eel import print_chain


class TestPrintChain(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)

    def test_print_chain(self):
        #        self.assertTrue(1 == 1)
        #        self.assertEqual(1, 1)
        #        self.assertNotEqual(1, 2)
        svg = print_chain([("A", "B", 10)], output_format="svg")
        self._logger.info(svg)
        svg = print_chain([("A", "B", 10)], output_format="graphviz")
        self._logger.info(svg)

    def test_print_chain_2(self):
        #        self.assertTrue(1 == 1)
        #        self.assertEqual(1, 1)
        #        self.assertNotEqual(1, 2)
        svg = print_chain([
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
        ], output_format="svg")
        self._logger.info(svg)
        svg = print_chain([("A", "B", 10)], output_format="graphviz")
        self._logger.info(svg)
