# 0001-sql-filtering-logic-for-bulk-purchase-and-stats

We decided to implement strict filtering in the service layer for bulk purchase and list statistics to ensure data integrity and accurate reporting.

## Context

The initial proposed PRs for "Bulk Purchase" and "List Stats" had several semantic issues:
1. **Bulk Purchase** was fetching all items in a list and marking them as purchased, overwriting the metadata (`purchased_by`, `purchased_at`) of items that were already purchased.
2. **List Stats** was returning category breakdowns for all items, which did not align with the frontend requirement of showing what is *remaining* to be bought.

## Decision

We will implement the following logic in `services/list_service.py`:

- **Bulk Purchase**: The query must explicitly filter for `is_purchased=False`. Only these items will be updated and counted in the return value. This prevents state corruption for already purchased items.
- **List Stats**: The category breakdown will be calculated exclusively from the subset of items where `is_purchased=False`. This provides the "Remaining by Category" view requested by the frontend.
- **Validation**: All service methods for a specific list must first verify the existence of the `GroceryList` and `Member` (where applicable) and raise a `ValueError` if not found, which the route layer will translate to a 404.

## Consequences

- **Data Integrity**: Historical purchase data is preserved.
- **Accuracy**: Stats correctly guide the shopper to remaining items.
- **Efficiency**: Bulk purchase updates are restricted to only necessary rows.
