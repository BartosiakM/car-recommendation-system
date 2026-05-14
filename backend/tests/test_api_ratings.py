import pytest

from app.models.user_vehicle_rating import UserVehicleRating
from app.models.vehicle import Vehicle


def _seed_vehicle(db, vehicle_id=1, name="TestCar"):
    v = Vehicle(
        vehicle_id=vehicle_id,
        vehicle_name=name,
        production_year=2020,
        performance_score=5,
        size_score=5,
        economy_score=5,
        practicality_score=5,
        exoticness_score=5,
        engagement_score=5,
    )
    db.add(v)
    db.commit()
    return v


def test_upsert_returns_404_when_vehicle_missing(client, db_session):
    r = client.post(
        "/axes-ratings/",
        json={"user_id": 1, "vehicle_id": 1, "performance": 5},
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Vehicle not found"


def test_upsert_creates_rating_when_vehicle_exists(client, db_session):
    _seed_vehicle(db_session, vehicle_id=1)

    r = client.post(
        "/axes-ratings/",
        json={"user_id": 10, "vehicle_id": 1, "performance": 7, "economy": 3},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["user_id"] == 10
    assert data["vehicle_id"] == 1
    assert data["performance"] == 7
    assert data["economy"] == 3


def test_upsert_updates_only_sent_fields(client, db_session):
    _seed_vehicle(db_session, vehicle_id=1)

    r1 = client.post(
        "/axes-ratings/",
        json={"user_id": 10, "vehicle_id": 1, "performance": 7, "economy": 3},
    )
    assert r1.status_code == 200

    r2 = client.post(
        "/axes-ratings/",
        json={"user_id": 10, "vehicle_id": 1, "economy": 9},
    )
    assert r2.status_code == 200
    data = r2.json()
    assert data["performance"] == 7
    assert data["economy"] == 9


def test_list_user_axes_ratings_returns_joined_vehicle_name(client, db_session):
    _seed_vehicle(db_session, vehicle_id=1, name="CarOne")
    _seed_vehicle(db_session, vehicle_id=2, name="CarTwo")

    db_session.add_all(
        [
            UserVehicleRating(user_id=5, vehicle_id=1, performance=1),
            UserVehicleRating(user_id=5, vehicle_id=2, performance=2),
        ]
    )
    db_session.commit()

    r = client.get("/axes-ratings/user/5")
    assert r.status_code == 200
    rows = r.json()
    assert len(rows) == 2
    assert {x["vehicle_name"] for x in rows} == {"CarOne", "CarTwo"}


def test_delete_axes_rating_deletes_row(client, db_session):
    _seed_vehicle(db_session, vehicle_id=1)

    db_session.add(UserVehicleRating(user_id=5, vehicle_id=1, performance=1))
    db_session.commit()

    r = client.delete("/axes-ratings/user/5/vehicle/1")
    assert r.status_code == 200
    assert r.json()["status"] == "deleted"

    still = (
        db_session.query(UserVehicleRating)
        .filter(UserVehicleRating.user_id == 5, UserVehicleRating.vehicle_id == 1)
        .first()
    )
    assert still is None


def test_delete_axes_rating_returns_404_when_missing(client, db_session):
    r = client.delete("/axes-ratings/user/5/vehicle/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Rating not found"
