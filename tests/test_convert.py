# -*- coding: utf-8 -*-

"""Tests for the conversion procedure"""

import unittest
from typing import Tuple, Type

from biokeen.convert import (
    AssociationConverter, Converter, CorrelationConverter, DrugIndicationConverter, DrugSideEffectConverter,
    NamedComplexHasComponentConverter, PartOfNamedComplexConverter, get_triple,
)
from pybel import BELGraph
from pybel.constants import ASSOCIATION, DECREASES, HAS_COMPONENT, INCREASES, PART_OF, POSITIVE_CORRELATION, RELATION
from pybel.dsl import Abundance, BaseEntity, MicroRna, NamedComplexAbundance, Pathology, Protein, Rna
from pybel.testing.utils import n
from pybel.typing import EdgeData


def _rel(x):
    return {RELATION: x}


def _rela(y):
    return {RELATION: ASSOCIATION, 'association_type': y}


a1 = Abundance('CHEBI', '1')
p1 = Protein('HGNC', '1')
d1 = Pathology('MESH', '1')
m1 = MicroRna('MIRBASE', '1')
r1 = Rna('HGNC', '1')
r2 = Rna('HGNC', '2')
nca1 = NamedComplexAbundance('FPLX', '1')

converters_true_list = [
    (NamedComplexHasComponentConverter, nca1, p1, _rel(HAS_COMPONENT), ('HGNC:1', 'partOf', 'FPLX:1')),
    (PartOfNamedComplexConverter, p1, nca1, _rel(PART_OF), ('HGNC:1', 'partOf', 'FPLX:1')),
    (CorrelationConverter, r1, r2, _rel(POSITIVE_CORRELATION), ('HGNC:1', 'positiveCorrelation', 'HGNC:2')),
    (AssociationConverter, r1, r2, _rel(ASSOCIATION), ('HGNC:1', 'association', 'HGNC:2')),
    (AssociationConverter, r1, r2, _rela('similarity'), ('HGNC:1', 'similarity', 'HGNC:2')),
    (DrugSideEffectConverter, a1, d1, _rel(INCREASES), ('CHEBI:1', 'increases', 'MESH:1')),
    (DrugIndicationConverter, a1, d1, _rel(DECREASES), ('CHEBI:1', 'decreases', 'MESH:1')),
]

converters_false_list = [
    (NamedComplexHasComponentConverter, nca1, p1, _rel(PART_OF)),
    (PartOfNamedComplexConverter, nca1, p1, _rel(HAS_COMPONENT)),
]


class TestConverters(unittest.TestCase):
    """Tests for the converter classes."""

    def help_test_convert(self,
                          converter: Type[Converter],
                          u: BaseEntity,
                          v: BaseEntity,
                          edge_data: EdgeData,
                          triple: Tuple[str, str, str],
                          ) -> None:
        self.assertTrue(issubclass(converter, Converter), msg=f'Not a Converter: {converter.__name__}')
        key = n()
        self.assertTrue(
            converter.predicate(u, v, key, edge_data),
            msg=f'Predicate failed: {converter.__name__}',
        )
        self.assertEqual(
            triple,
            converter.convert(u, v, key, edge_data),
            msg='Conversion failed: {converter.__name__}',
        )
        graph = BELGraph()
        graph.add_edge(u, v, key=key, **edge_data)
        self.assertEqual(
            triple,
            get_triple(graph, u, v, key),
            msg=f'get_triple failed: {converter.__name__}',
        )

    def test_converters_true(self):
        """Test passing converters."""
        for converter, u, v, edge_data, triple in converters_true_list:
            with self.subTest(msg=f'Converter: {converter.__qualname__}'):
                self.help_test_convert(converter, u, v, edge_data, triple)

    def test_converters_false(self):
        """Test falsification of converters."""
        for converter, u, v, edge_data in converters_false_list:
            with self.subTest():
                self.assertFalse(converter.predicate(u, v, n(), edge_data))
