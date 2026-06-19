# ByteBites UML Class Diagram

```
┌─────────────────────────────────┐
│            Customer             │
├─────────────────────────────────┤
│ - name: str                     │
│ - purchase_history: list[Order] │
├─────────────────────────────────┤
│ + verify_user() -> bool         │
│ + add_to_history(order: Order)  │
└────────────────┬────────────────┘
                 │ places (1..*)
                 ▼
┌─────────────────────────────────┐
│              Order              │
├─────────────────────────────────┤
│ - items: list[FoodItem]         │
│ - total: float                  │
├─────────────────────────────────┤
│ + add_item(item: FoodItem)      │
│ + compute_total() -> float      │
└────────────────┬────────────────┘
                 │ contains (1..*)
                 ▼
┌─────────────────────────────────┐
│            FoodItem             │
├─────────────────────────────────┤
│ - name: str                     │
│ - price: float                  │
│ - category: str                 │
│ - popularity_rating: float      │
├─────────────────────────────────┤
│ + get_details() -> str          │
└─────────────────────────────────┘
                 ▲
                 │ holds (0..*)
┌─────────────────────────────────┐
│              Menu               │
├─────────────────────────────────┤
│ - items: list[FoodItem]         │
├─────────────────────────────────┤
│ + add_item(item: FoodItem)      │
│ + filter_by_category(cat: str)  │
│   -> list[FoodItem]             │
└─────────────────────────────────┘
```

## Relationships

| Relationship     | Type        | Description                                      |
|------------------|-------------|--------------------------------------------------|
| Customer → Order | Association | A customer places orders, stored in history      |
| Order → FoodItem | Aggregation | An order groups items and computes the total     |
| Menu → FoodItem  | Aggregation | The menu catalogs all items, filterable by category |
