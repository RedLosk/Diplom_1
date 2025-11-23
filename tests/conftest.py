from unittest.mock import Mock

import pytest

from praktikum.burger import Burger
from praktikum.ingredient import Ingredient


@pytest.fixture
def burger_with_three_ingredients():
    burger = Burger()
    mock_ingredient1 = Mock(spec=Ingredient)
    mock_ingredient2 = Mock(spec=Ingredient)
    mock_ingredient3 = Mock(spec=Ingredient)

    burger.add_ingredient(mock_ingredient1)
    burger.add_ingredient(mock_ingredient2)
    burger.add_ingredient(mock_ingredient3)

    return burger, mock_ingredient1, mock_ingredient2, mock_ingredient3

