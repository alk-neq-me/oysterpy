import unittest

from oysterpy.oyster import Option, Some


class TestOption(unittest.TestCase):
    def test_is_some(self):
        data: Option[str] = Some("hello")
        self.assertIs(data.is_some(), True)

