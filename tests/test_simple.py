# -*- coding: utf-8 -*-

"""Simple tests for BioKEEN."""

import unittest

from biokeen.constants import VERSION


class TestImport(unittest.TestCase):
    """Simple tests for importing BioKEEN."""

    def test_version_type(self):
        """Test the type of the version string."""
        self.assertIsInstance(VERSION, str)
