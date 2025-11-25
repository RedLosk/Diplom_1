from unittest.mock import Mock

import pytest

from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestBurger:
    def test_set_buns(self):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = 'test bun'
        mock_bun.get_price.return_value = 100

        burger.set_buns(mock_bun)

        assert burger.bun == mock_bun

    def test_add_ingredient(self):
        burger = Burger()
        mock_ingredient = Mock(spec=Ingredient)
        mock_ingredient.get_name.return_value = 'test ingredient'
        mock_ingredient.get_price.return_value = 50

        burger.add_ingredient(mock_ingredient)

        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient

    def test_add_multiple_ingredients(self):
        burger = Burger()
        mock_ingredient1 = Mock(spec=Ingredient)
        mock_ingredient2 = Mock(spec=Ingredient)
        mock_ingredient3 = Mock(spec=Ingredient)

        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)
        burger.add_ingredient(mock_ingredient3)

        assert len(burger.ingredients) == 3
        assert burger.ingredients[0] == mock_ingredient1
        assert burger.ingredients[1] == mock_ingredient2
        assert burger.ingredients[2] == mock_ingredient3

    def test_remove_ingredient(self, burger_with_three_ingredients):
        burger, mock_ingredient1, mock_ingredient2, mock_ingredient3 = burger_with_three_ingredients

        burger.remove_ingredient(1)

        assert len(burger.ingredients) == 2
        assert burger.ingredients[0] == mock_ingredient1
        assert burger.ingredients[1] == mock_ingredient3

    def test_move_ingredient(self, burger_with_three_ingredients):
        burger, mock_ingredient1, mock_ingredient2, mock_ingredient3 = burger_with_three_ingredients

        burger.move_ingredient(2, 0)

        assert len(burger.ingredients) == 3
        assert burger.ingredients[0] == mock_ingredient3
        assert burger.ingredients[1] == mock_ingredient1
        assert burger.ingredients[2] == mock_ingredient2

    @pytest.mark.parametrize('index,new_index,expected_order', [
        (0, 2, [1, 2, 0]),  # Перемещение из начала в конец
        (2, 0, [2, 0, 1]),  # Перемещение из конца в начало
        (1, 0, [1, 0, 2]),  # Перемещение из середины в начало
        (0, 1, [1, 0, 2]),  # Перемещение из начала в середину
    ])

    def test_move_ingredient_parameterized(self, index, new_index, expected_order):
        burger = Burger()
        mock_ingredient0 = Mock(spec=Ingredient)
        mock_ingredient1 = Mock(spec=Ingredient)
        mock_ingredient2 = Mock(spec=Ingredient)
        ingredients = [mock_ingredient0, mock_ingredient1, mock_ingredient2]

        for ingredient in ingredients:
            burger.add_ingredient(ingredient)

        burger.move_ingredient(index, new_index)

        assert len(burger.ingredients) == 3
        for i, expected_idx in enumerate(expected_order):
            assert burger.ingredients[i] == ingredients[expected_idx]

    @pytest.mark.parametrize('remove_index', [0, 1, 2])
    def test_remove_ingredient_parameterized(self, burger_with_three_ingredients, remove_index):
        burger, mock_ingredient1, mock_ingredient2, mock_ingredient3 = burger_with_three_ingredients
  
        expected_ingredients = [mock_ingredient1, mock_ingredient2, mock_ingredient3]
        expected_ingredients.pop(remove_index)

        burger.remove_ingredient(remove_index)

        assert len(burger.ingredients) == 2
        assert burger.ingredients == expected_ingredients

    @pytest.mark.parametrize('bun_price,ingredient_prices,expected_price', [
        (100, [], 200),  # Только булочки (цена * 2)
        (100, [50], 250),  # Булочки + 1 ингредиент
        (100, [50, 30, 20], 300),  # Булочки + 3 ингредиента
        (200, [100, 100], 600),  # Другие цены
        (0, [0], 0),  # Нулевые цены
    ])
    def test_get_price(self, bun_price, ingredient_prices, expected_price):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = bun_price

        burger.set_buns(mock_bun)

        for price in ingredient_prices:
            mock_ingredient = Mock(spec=Ingredient)
            mock_ingredient.get_price.return_value = price
            burger.add_ingredient(mock_ingredient)

        assert burger.get_price() == expected_price

    def test_get_receipt_with_ingredients(self):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = 'test bun'
        mock_bun.get_price.return_value = 100

        mock_ingredient1 = Mock(spec=Ingredient)
        mock_ingredient1.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock_ingredient1.get_name.return_value = 'hot sauce'
        mock_ingredient1.get_price.return_value = 50

        mock_ingredient2 = Mock(spec=Ingredient)
        mock_ingredient2.get_type.return_value = INGREDIENT_TYPE_FILLING
        mock_ingredient2.get_name.return_value = 'cutlet'
        mock_ingredient2.get_price.return_value = 30

        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient1)
        burger.add_ingredient(mock_ingredient2)

        receipt = burger.get_receipt()

        assert '(==== test bun ====)' in receipt
        assert '= sauce hot sauce =' in receipt
        assert '= filling cutlet =' in receipt
        assert 'Price: 280' in receipt

    def test_get_receipt_without_ingredients(self):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = 'test bun'
        mock_bun.get_price.return_value = 100

        burger.set_buns(mock_bun)

        receipt = burger.get_receipt()

        assert '(==== test bun ====)' in receipt
        assert 'Price: 200' in receipt
        lines = receipt.split('\n')
        ingredient_lines = [line for line in lines if line.startswith('= ')]
        assert len(ingredient_lines) == 0

    @pytest.mark.parametrize('bun_name,expected_name_in_receipt', [
        ('black bun', 'black bun'),
        ('white bun', 'white bun'),
        ('red bun', 'red bun'),
        ('test bun', 'test bun'),
    ])
    def test_get_receipt_bun_name_parameterized(self, bun_name, expected_name_in_receipt):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = 100

        burger.set_buns(mock_bun)

        receipt = burger.get_receipt()

        assert f'(==== {expected_name_in_receipt} ====)' in receipt
        assert 'Price: 200' in receipt

    @pytest.mark.parametrize('ingredient_type,ingredient_name,expected_type_in_receipt', [
        (INGREDIENT_TYPE_SAUCE, 'hot sauce', 'sauce'),
        (INGREDIENT_TYPE_SAUCE, 'sour cream', 'sauce'),
        (INGREDIENT_TYPE_FILLING, 'cutlet', 'filling'),
        (INGREDIENT_TYPE_FILLING, 'dinosaur', 'filling'),
    ])
    def test_get_receipt_ingredient_type_parameterized(self, ingredient_type, ingredient_name, expected_type_in_receipt):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = 'test bun'
        mock_bun.get_price.return_value = 100

        mock_ingredient = Mock(spec=Ingredient)
        mock_ingredient.get_type.return_value = ingredient_type
        mock_ingredient.get_name.return_value = ingredient_name
        mock_ingredient.get_price.return_value = 50

        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient)

        receipt = burger.get_receipt()

        assert f'= {expected_type_in_receipt} {ingredient_name} =' in receipt

    def test_get_receipt_format(self):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = 'test bun'
        mock_bun.get_price.return_value = 100

        mock_ingredient = Mock(spec=Ingredient)
        mock_ingredient.get_type.return_value = INGREDIENT_TYPE_SAUCE
        mock_ingredient.get_name.return_value = 'hot sauce'
        mock_ingredient.get_price.return_value = 50

        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient)

        receipt = burger.get_receipt()
        lines = receipt.split('\n')

        assert lines[0] == '(==== test bun ====)'
        assert lines[1] == '= sauce hot sauce ='
        assert lines[2] == '(==== test bun ====)'
        assert lines[3] == ''
        assert lines[4] == 'Price: 250'

    def test_burger_initialization(self):
        burger = Burger()
        assert burger.bun is None
        assert burger.ingredients == []

