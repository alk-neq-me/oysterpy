import unittest

from oysterpy.oyster import Option, Some, as_option


class TestOption(unittest.TestCase):
    def test_is_some(self):
        data: Option[str] = Some("hello")
        self.assertIs(data.is_some(), True)

    def test_as_option(self):
        arr = {"name": "bob", "age": 17, "hobby": "art"}
        def get(k: str) -> str | None:
            return arr.get(k)
        find = as_option(get)("name")
        self.assertEqual(find.unwrap(), "bob")

    def test_as_option_decorator(self):
        arr = {"name": "bob", "age": 17, "hobby": "art"}
        @as_option
        def get(k: str) -> str | None:
            return arr.get(k)
        self.assertEqual(get("age").unwrap(), 17)
