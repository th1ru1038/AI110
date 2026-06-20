# ByteBites UML Class Diagram

```
┌──────────────────────────────────────┐
│               Customer               │
├──────────────────────────────────────┤
│ - name: str                          │
│ - purchase_history: list[Order]      │
├──────────────────────────────────────┤
│ + verify_user() -> bool              │
│ + add_to_history(order: Order)       │
│ + total_spent() -> float             │
└─────────────────┬────────────────────┘
                  │ places (1..*)
                  ▼
┌──────────────────────────────────────┐
│                Order                 │
├──────────────────────────────────────┤
│ - items: list[FoodItem]              │
│ - total: float                       │
├──────────────────────────────────────┤
│ + add_item(item: FoodItem)           │
│ + compute_total() -> float           │
│ + item_count() -> int                │
└─────────────────┬────────────────────┘
                  │ contains (1..*)
                  ▼
┌──────────────────────────────────────┐
│              FoodItem                │
├──────────────────────────────────────┤
│ - name: str                          │
│ - price: float                       │
│ - category: str                      │
│ - popularity_rating: float           │
├──────────────────────────────────────┤
│ + get_details() -> str               │
└──────────────────────────────────────┘
                  ▲
                  │ holds (0..*)
┌──────────────────────────────────────┐
│                Menu                  │
├──────────────────────────────────────┤
│ - items: list[FoodItem]              │
├──────────────────────────────────────┤
│ + add_item(item: FoodItem)           │
│ + filter_by_category(cat: str)       │
│   -> list[FoodItem]                  │
│ + filter_by_max_price(max: float)    │
│   -> list[FoodItem]                  │
│ + sort_by_price(ascending: bool)     │
│   -> list[FoodItem]                  │
│ + sort_by_popularity()               │
│   -> list[FoodItem]                  │
└──────────────────────────────────────┘
```

## Relationships

| Relationship     | Type        | Description                                         |
|------------------|-------------|-----------------------------------------------------|
| Customer → Order | Association | A customer places orders, stored in history         |
| Order → FoodItem | Aggregation | An order groups items and computes the total        |
| Menu → FoodItem  | Aggregation | The menu catalogs all items, filterable by category |
