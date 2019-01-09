# -*- coding: utf-8 -*-

"""Tests for the conversion procedure"""

import unittest
from typing import Optional, Tuple, Type

from pybel import BELGraph
from pybel.constants import ASSOCIATION, HAS_COMPONENT, PART_OF, POSITIVE_CORRELATION, RELATION
from pybel.dsl import BaseEntity, NamedComplexAbundance, Protein, Rna
from pybel.testing.utils import n
from pybel.typing import EdgeData

from biokeen.convert import (
    AssociationConverter, Converter, CorrelationConverter, HasComponentConverter,
    PartOfConverter, get_triple,
)


def _rel(x):
    return {RELATION: x}


p1 = Protein('HGNC', '1')
r1 = Rna('HGNC', '1')
r2 = Rna('HGNC', '2')
nca1 = NamedComplexAbundance('FPLX', '1')


class TestConverters(unittest.TestCase):
    """Tests for the converter classes."""

    def help_test_convert(self,
                          converter: Type[Converter],
                          u: BaseEntity,
                          v: BaseEntity,
                          edge_data: EdgeData,
                          triple: Optional[Tuple[str, str, str]] = None,
                          ) -> None:
        key = n()
        if triple is not None:
            self.assertTrue(converter.predicate(u, v, key, edge_data))
            self.assertEqual(triple, converter.convert(u, v, key, edge_data))
            graph = BELGraph()
            graph.add_edge(u, v, key=key, **edge_data)
            self.assertEqual(triple, get_triple(graph, u, v, key))
        else:
            self.assertFalse(converter.predicate(u, v, key, edge_data))

    def test_convert_has_component_true(self):
        """Test HasComponentConverter.predicate() true values."""
        u, v, edge_data, triple = nca1, p1, _rel(HAS_COMPONENT), ('HGNC:1', 'partOf', 'complex(FPLX:1)')
        self.help_test_convert(HasComponentConverter, u, v, edge_data, triple)

    def test_convert_correlation_true(self):
        """Test CorrelationConverter.predicate() true values."""
        u, v, edge_data, triple = r1, r2, _rel(POSITIVE_CORRELATION), ('HGNC:1', 'positiveCorrelation', 'HGNC:2')
        self.help_test_convert(CorrelationConverter, u, v, edge_data, triple)

    def test_convert_association_true(self):
        """Test CorrelationConverter.predicate() true values."""
        u, v, edge_data, triple = r1, r2, _rel(ASSOCIATION), ('HGNC:1', 'positiveCorrelation', 'HGNC:2')
        self.help_test_convert(AssociationConverter, u, v, edge_data, triple)

        u, v, edge_data, triple = r1, r2, {RELATION: ASSOCIATION, 'association_type': 'similarity'}, (
            'HGNC:1', 'similarity', 'HGNC:2')
        self.help_test_convert(AssociationConverter, u, v, edge_data, triple)

    def test_convert_has_component_false(self):
        """Test ConvertHasComponent.predicate() false values."""
        self.help_test_convert(HasComponentConverter, nca1, p1, _rel(PART_OF))

    def test_convert_part_of_true(self):
        """Test ConvertPartOf.predicate() true values."""
        self.assertFalse(PartOfConverter.predicate(nca1, p1, n(), _rel(HAS_COMPONENT)))

    def test_convert_part_of_false(self):
        """Test ConvertPartOf.predicate() false values."""
        self.assertTrue(PartOfConverter.predicate(nca1, p1, n(), _rel(PART_OF)))
