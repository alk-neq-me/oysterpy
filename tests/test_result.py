import unittest
from oysterpy.exceptions import UnwrapException

from oysterpy.oyster import Err, Ok, Result, as_result


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

    def test_custom_error_enum(self):
        from enum import Enum

        class ErrorKind(str, Enum):
            NotFound = "ErrorKind@NotFound"

        self.assertEqual("ErrorKind@NotFound", Err(ErrorKind.NotFound).unwrap_err())

    def test_as_result_hof(self):
        arr = ["apple", "cherry", "banana"]

        class NotFound(Exception):
            """not found error"""

        def unsafe_find(x: str) -> str:
            for i in arr:
                if i == x:
                    return i
            raise NotFound("404 key")

        self.assertEqual(as_result(unsafe_find)("apple").unwrap(), "apple")

    def test_as_result_decorator(self):
        arr = ["apple", "cherry", "banana"]

        class NotFound(Exception):
            """not found error"""

        @as_result
        def unsafe_find(x: str) -> str:
            for i in arr:
                if i == x:
                    return i
            raise NotFound("404 key")

        safe_error: Result[str, str] = unsafe_find("apple")

        self.assertEqual(safe_error.unwrap(), "apple")

    def test_in_line_as_result(self):
        arr = ["apple", "cherry", "banana"]
        result = as_result(lambda e: next(e))((i for i in arr if i == "apple"))

        self.assertEqual(result.unwrap(), "apple")
