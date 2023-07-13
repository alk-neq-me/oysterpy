import unittest
from oysterpy.exceptions import UnwrapException

from oysterpy.oyster import Err, Ok, Result


class TestResult(unittest.TestCase):
    def test_is_ok(self):
        data: Result[str, int] = Ok("hello")
        self.assertIs(data.is_ok(), True)


    def test_map_or(self):
        x = Ok("foo").map_or(23, lambda v: len(v))  # str: 3
        self.assertIs(x, 3)

        x = Err("foo").map_or(23, lambda v: len(v))  # int: 23
        self.assertIs(x, 23)

    def test_unwrap(self):
        self.assertRaises(UnwrapException, Err(23).unwrap)
        self.assertRaises(UnwrapException, Ok(23).unwrap_err)
        self.assertEqual(23, Err(23).unwrap_err())
