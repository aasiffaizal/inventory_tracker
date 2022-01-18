from db.base import get_table_name


def test_get_table_name_returns_snake_case():
    assert 'test_shopify' == get_table_name('TestShopify')
    assert 'test_name_test' == get_table_name('TestNameTest')
