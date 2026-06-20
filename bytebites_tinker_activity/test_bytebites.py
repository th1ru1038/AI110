import pytest
from models import Customer, FoodItem, Menu, Order


# --- Fixtures ---

@pytest.fixture
def sample_items():
    return {
        "burger": FoodItem("Spicy Burger", 8.99, "Entrees", 4.7),
        "soda":   FoodItem("Large Soda",   2.49, "Drinks",  4.2),
        "brownie": FoodItem("Chocolate Brownie", 3.99, "Desserts", 4.9),
    }

@pytest.fixture
def menu(sample_items):
    m = Menu()
    for item in sample_items.values():
        m.add_item(item)
    return m


# --- Order total tests ---

def test_order_total_with_multiple_items(sample_items):
    """Adding a burger and soda produces the correct total."""
    order = Order()
    order.add_item(sample_items["burger"])
    order.add_item(sample_items["soda"])
    assert order.compute_total() == pytest.approx(11.48)

def test_order_total_is_zero_when_empty():
    """An order with no items has a total of $0."""
    order = Order()
    assert order.compute_total() == 0.0

def test_order_item_count(sample_items):
    """item_count reflects the number of items added."""
    order = Order()
    order.add_item(sample_items["burger"])
    order.add_item(sample_items["soda"])
    assert order.item_count() == 2


# --- Menu filtering tests ---

def test_filter_by_category_returns_matching_items(menu, sample_items):
    """filter_by_category('Drinks') returns only drink items."""
    results = menu.filter_by_category("Drinks")
    assert results == [sample_items["soda"]]

def test_filter_by_category_returns_empty_for_unknown(menu):
    """filter_by_category returns an empty list for a category not on the menu."""
    assert menu.filter_by_category("Sushi") == []

def test_filter_by_max_price(menu, sample_items):
    """filter_by_max_price(4.00) returns only items at or under $4."""
    results = menu.filter_by_max_price(4.00)
    assert sample_items["soda"] in results
    assert sample_items["brownie"] in results
    assert sample_items["burger"] not in results


# --- Menu sorting tests ---

def test_sort_by_price_ascending(menu, sample_items):
    """sort_by_price returns items cheapest first."""
    results = menu.sort_by_price(ascending=True)
    assert results[0] == sample_items["soda"]
    assert results[-1] == sample_items["burger"]

def test_sort_by_popularity(menu, sample_items):
    """sort_by_popularity returns the highest-rated item first."""
    results = menu.sort_by_popularity()
    assert results[0] == sample_items["brownie"]


# --- Customer tests ---

def test_verify_user_with_valid_name():
    """verify_user returns True for a customer with a real name."""
    assert Customer("Alex").verify_user() is True

def test_verify_user_rejects_empty_name():
    """verify_user returns False for an empty or whitespace-only name."""
    assert Customer("").verify_user() is False
    assert Customer("   ").verify_user() is False

def test_customer_total_spent(sample_items):
    """total_spent sums totals across all past orders."""
    customer = Customer("Alex")
    order1 = Order()
    order1.add_item(sample_items["burger"])
    order1.compute_total()

    order2 = Order()
    order2.add_item(sample_items["soda"])
    order2.compute_total()

    customer.add_to_history(order1)
    customer.add_to_history(order2)

    assert customer.total_spent() == pytest.approx(11.48)
