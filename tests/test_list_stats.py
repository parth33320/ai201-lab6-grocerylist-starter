import pytest
from app import create_app
from extensions import db
from models import Member, GroceryList, Item

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

def test_list_stats_success(client, app):
    with app.app_context():
        member = Member(username="jules", email="jules@example.com")
        db.session.add(member)
        db.session.commit()

        glist = GroceryList(name="Weekly Shop", created_by=member.id)
        db.session.add(glist)
        db.session.commit()

        # Items:
        # 1 purchased in 'dairy'
        # 2 unpurchased in 'produce'
        # 1 unpurchased in 'dairy'
        # 1 unpurchased with no category
        db.session.add_all([
            Item(list_id=glist.id, name="Milk", category="dairy", is_purchased=True, added_by=member.id),
            Item(list_id=glist.id, name="Cheese", category="dairy", is_purchased=False, added_by=member.id),
            Item(list_id=glist.id, name="Apple", category="produce", is_purchased=False, added_by=member.id),
            Item(list_id=glist.id, name="Banana", category="produce", is_purchased=False, added_by=member.id),
            Item(list_id=glist.id, name="Water", is_purchased=False, added_by=member.id),
        ])
        db.session.commit()
        list_id = glist.id

    response = client.get(f"/lists/{list_id}/stats")
    assert response.status_code == 200
    data = response.get_json()

    assert data["total_items"] == 5
    assert data["purchased"] == 1
    assert data["remaining"] == 4

    # Semantic mismatch fix: breakdown should only look at remaining items
    assert data["by_category"]["produce"] == 2
    assert data["by_category"]["dairy"] == 1  # Not 2!
    assert data["by_category"]["uncategorized"] == 1

def test_list_stats_invalid_list(client):
    response = client.get("/lists/invalid-id/stats")
    assert response.status_code == 404
