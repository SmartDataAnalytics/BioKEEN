# -*- coding: utf-8 -*-

"""Tests for the conversion procedure"""

import unittest

from pybel.constants import HAS_COMPONENT, PART_OF, RELATION
from pybel.dsl import NamedComplexAbundance, Protein
from pybel.testing.utils import n

from biokeen.convert import ConvertHasComponent, ConvertPartOf


def _rel(x):
    return {RELATION: x}


p1 = Protein('HGNC', '1')
nca1 = NamedComplexAbundance('FPLX', '1')


class TestConverters(unittest.TestCase):
    """Tests for the converter classes."""

    def test_convert_has_component_true(self):
        """Test ConvertHasComponent.predicate() true values."""
        u, v, k, d = nca1, p1, n(), _rel(HAS_COMPONENT)
        self.assertTrue(ConvertHasComponent.predicate(u, v, k, d))
        trip = 'HGNC:1', 'partOf', 'complex(FPLX1)'
        self.assertEqual(trip, ConvertHasComponent.convert(u, v, k, d))
        self.assertEqual(trip, ConvertHasComponent.convert(u, v, k, d))

    def test_convert_has_component_false(self):
        """Test ConvertHasComponent.predicate() false values."""
        self.assertFalse(ConvertHasComponent.predicate(nca1, p1, n(), _rel(PART_OF)))

    def test_convert_part_of_true(self):
        """Test ConvertPartOf.predicate() true values."""
        self.assertFalse(ConvertPartOf.predicate(nca1, p1, n(), _rel(HAS_COMPONENT)))

    def test_convert_part_of_false(self):
        """Test ConvertPartOf.predicate() false values."""
        self.assertTrue(ConvertPartOf.predicate(nca1, p1, n(), _rel(PART_OF)))
