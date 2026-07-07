# GroceryList Context

A shared grocery list API where members manage lists and track purchases.

## Language

**Member**:
An authentication identity in the system who can create or participate in grocery lists.
_Avoid_: User, Account

**Creator**:
The Member who originally created a specific grocery list.
_Avoid_: Owner

**Grocery List**:
A named collection of items, which can be private to the Creator or Shared with other Members.
_Avoid_: List

**Shared List**:
A Grocery List where other Members can view and add items.

**Item**:
A single product or entry added to a Grocery List.

**Quantity**:
The numeric amount of an Item required.

**Unit**:
The measure of an Item (e.g., "kg", "box", "count").

**Category**:
A classification for Items to help navigate the store (e.g., "produce", "dairy").

**Purchasing**:
The act of marking an Item as bought.

**Purchased_at**:
The timestamp recorded when an Item is marked as purchased.

**Bulk Purchase**:
The action of marking all currently Unpurchased Items in a Grocery List as purchased in a single operation.

**Remaining**:
Items on a Grocery List that have not yet been marked as purchased.

**Stats**:
Summary metrics for a Grocery List, specifically focusing on the count of Remaining items by Category.

## Relationships

- A **Member** can be the **Creator** of many **Grocery Lists**.
- A **Grocery List** contains many **Items**.
- An **Item** is added by one **Member** and can be purchased by one **Member**.
