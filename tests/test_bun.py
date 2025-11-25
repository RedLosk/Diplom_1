import pytest

from praktikum.bun import Bun


class TestBun:
    @pytest.mark.parametrize('name,price', [
        ('black bun', 100),
        ('white bun', 200),
        ('red bun', 300),
        ('test bun', 0),
        ('', 999.99),
    ])
    def test_get_name(self, name, price):
        bun = Bun(name, price)
        assert bun.get_name() == name

    @pytest.mark.parametrize('name,price', [
        ('black bun', 100),
        ('white bun', 200),
        ('red bun', 300),
        ('test bun', 0),
        ('test bun', 999.99),
    ])
    def test_get_price(self, name, price):
        bun = Bun(name, price)
        assert bun.get_price() == price

    def test_bun_initialization(self):
        bun = Bun('test bun', 150)
        assert bun.name == 'test bun'
        assert bun.price == 150

