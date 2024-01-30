import json
import unittest
from typing import Any


class TestStyleCategories(unittest.TestCase):
    def setUp(self):
        with open("categories.json", "r", encoding="utf-8") as file:
            self.categories: dict[str, list[str]] = json.load(file)
        with open("styles.json", "r", encoding="utf-8") as file:
            self.styles: dict[str, Any] = json.load(file)

    def test_style_exists(self) -> None:
        for category, category_styles in self.categories.items():
            with self.subTest(category=category):
                self.assertTrue(category_styles, f"Category {category!r} is empty")
                for style in category_styles:
                    with self.subTest(category=category, style=style):
                        if style not in (*self.styles.keys(), *self.categories.keys()):
                            raise self.failureException(f"Style {style!r} is referenced but does not exist")
