# 1) Customer - To track their names and purchase history
# 2) Food item - name, price, category, and popularity
# 3) Menu - To hold all the food items
# 4) Order/Transaction - To perform based on the other attributes

class Customer:
    def __init__(self, name):
        self.name = name
        self.purchase_history = []

    def verify_user(self):
        return bool(self.name.strip())

    def add_to_history(self, order):
        self.purchase_history.append(order)

    def total_spent(self):
        return sum(order.total for order in self.purchase_history)


class FoodItem:
    def __init__(self, name, price, category, popularity_rating):
        self.name = name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating

    def get_details(self):
        return f"{self.name} | ${self.price:.2f} | {self.category} | Rating: {self.popularity_rating}"


class Menu:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def filter_by_category(self, category):
        return [item for item in self.items if item.category == category]

    def filter_by_max_price(self, max_price):
        return [item for item in self.items if item.price <= max_price]

    def sort_by_price(self, ascending=True):
        return sorted(self.items, key=lambda item: item.price, reverse=not ascending)

    def sort_by_popularity(self):
        return sorted(self.items, key=lambda item: item.popularity_rating, reverse=True)


class Order:
    def __init__(self):
        self.items = []
        self.total = 0.0

    def add_item(self, item):
        self.items.append(item)

    def compute_total(self):
        self.total = sum(item.price for item in self.items)
        return self.total

    def item_count(self):
        return len(self.items)
