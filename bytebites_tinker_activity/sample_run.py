from models import Customer, FoodItem, Menu, Order

# Create food items
burger = FoodItem("Spicy Burger", 8.99, "Entrees", 4.7)
soda = FoodItem("Large Soda", 2.49, "Drinks", 4.2)
brownie = FoodItem("Chocolate Brownie", 3.99, "Desserts", 4.9)

# Build menu
menu = Menu()
menu.add_item(burger)
menu.add_item(soda)
menu.add_item(brownie)

print("Full menu:")
for item in menu.items:
    print(" ", item.get_details())

print("\nDrinks only:")
for item in menu.filter_by_category("Drinks"):
    print(" ", item.get_details())

# Customer places an order
customer = Customer("Alex")
print(f"\nVerified user: {customer.verify_user()}")

order = Order()
order.add_item(burger)
order.add_item(soda)
print(f"\nOrder total: ${order.compute_total():.2f}")

customer.add_to_history(order)
print(f"Purchase history count: {len(customer.purchase_history)}")
