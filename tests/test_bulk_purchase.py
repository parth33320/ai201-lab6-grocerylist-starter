import pytest
from app import create_app
from extensions import db
from models import Member, GroceryList, Item
from datetime import datetime, timezone

@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_bulk_purchase_success(client, app):
    with app.app_context():
        # Setup data
        member = Member(username="jules", email="jules@example.com")
        db.session.add(member)
        db.session.commit()

        glist = GroceryList(name="Weekly Shop", created_by=member.id)
        db.session.add(glist)
        db.session.commit()

        # 1 already purchased, 2 unpurchased
        item1 = Item(list_id=glist.id, name="Milk", is_purchased=True, purchased_by=member.id, added_by=member.id)
        item2 = Item(list_id=glist.id, name="Eggs", is_purchased=False, added_by=member.id)
        item3 = Item(list_id=glist.id, name="Bread", is_purchased=False, added_by=member.id)
        db.session.add_all([item1, item2, item3])
        db.session.commit()

        list_id = glist.id
        member_id = member.id
        old_purchased_at = item1.purchased_at

    # Action
    response = client.post(f"/lists/{list_id}/purchase-all", json={"user_id": member_id})

    assert response.status_code == 200
    data = response.get_json()
    assert data["purchased"] == 2  # Only unpurchased items

    with app.app_context():
        # Verify items
        items = Item.query.filter_by(list_id=list_id).all()
        for item in items:
            assert item.is_purchased is True
            assert item.purchased_by == member_id

        # Verify item1 metadata was NOT changed
        item1_after = db.session.get(Item, item1.id)
        # Note: Depending on how precision works, we might need to be careful with timestamp comparisons
        # but the logic should avoid updating it at all.
        assert item1_after.purchased_at == old_purchased_at

def test_bulk_purchase_invalid_list(client):
    response = client.post("/lists/invalid-id/purchase-all", json={"user_id": "any"})
    assert response.status_code == 404

def test_bulk_purchase_invalid_member(client, app):
    with app.app_context():
        member = Member(username="jules", email="jules@example.com")
        db.session.add(member)
        db.session.commit()
        glist = GroceryList(name="Weekly Shop", created_by=member.id)
        db.session.add(glist)
        db.session.commit()
        list_id = glist.id

    response = client.post(f"/lists/{list_id}/purchase-all", json={"user_id": "ghost-id"})
    assert response.status_code == 404
