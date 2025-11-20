import pytest

from praktikum.database import Database
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestDatabase:
    def test_available_buns(self):
        database = Database()
        buns = database.available_buns()

        assert len(buns) == 3
        assert all(isinstance(bun, Bun) for bun in buns)
        assert buns[0].get_name() == 'black bun'
        assert buns[0].get_price() == 100
        assert buns[1].get_name() == 'white bun'
        assert buns[1].get_price() == 200
        assert buns[2].get_name() == 'red bun'
        assert buns[2].get_price() == 300

    def test_available_ingredients(self):
        database = Database()
        ingredients = database.available_ingredients()

        assert len(ingredients) == 6
        assert all(isinstance(ingredient, Ingredient) for ingredient in ingredients)

        sauces = [ing for ing in ingredients if ing.get_type() == INGREDIENT_TYPE_SAUCE]
        assert len(sauces) == 3
        assert sauces[0].get_name() == 'hot sauce'
        assert sauces[0].get_price() == 100
        assert sauces[1].get_name() == 'sour cream'
        assert sauces[1].get_price() == 200
        assert sauces[2].get_name() == 'chili sauce'
        assert sauces[2].get_price() == 300

        fillings = [ing for ing in ingredients if ing.get_type() == INGREDIENT_TYPE_FILLING]
        assert len(fillings) == 3
        assert fillings[0].get_name() == 'cutlet'
        assert fillings[0].get_price() == 100
        assert fillings[1].get_name() == 'dinosaur'
        assert fillings[1].get_price() == 200
        assert fillings[2].get_name() == 'sausage'
        assert fillings[2].get_price() == 300

    @pytest.mark.parametrize('index,expected_name,expected_price', [
        (0, 'black bun', 100),
        (1, 'white bun', 200),
        (2, 'red bun', 300),
    ])
    def test_available_buns_parameterized(self, index, expected_name, expected_price):
        database = Database()
        buns = database.available_buns()

        assert buns[index].get_name() == expected_name
        assert buns[index].get_price() == expected_price

    @pytest.mark.parametrize('index,expected_type,expected_name,expected_price', [
        (0, INGREDIENT_TYPE_SAUCE, 'hot sauce', 100),
        (1, INGREDIENT_TYPE_SAUCE, 'sour cream', 200),
        (2, INGREDIENT_TYPE_SAUCE, 'chili sauce', 300),
        (3, INGREDIENT_TYPE_FILLING, 'cutlet', 100),
        (4, INGREDIENT_TYPE_FILLING, 'dinosaur', 200),
        (5, INGREDIENT_TYPE_FILLING, 'sausage', 300),
    ])
    def test_available_ingredients_parameterized(self, index, expected_type, expected_name, expected_price):
        database = Database()
        ingredients = database.available_ingredients()

        assert ingredients[index].get_type() == expected_type
        assert ingredients[index].get_name() == expected_name
        assert ingredients[index].get_price() == expected_price

    def test_database_initialization(self):
        database = Database()

        assert len(database.buns) == 3
        assert len(database.ingredients) == 6
        assert all(isinstance(bun, Bun) for bun in database.buns)
        assert all(isinstance(ingredient, Ingredient) for ingredient in database.ingredients)

