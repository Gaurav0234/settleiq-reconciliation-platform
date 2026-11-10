from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes.health import router
from app.db.session import get_db
from app.main import app


client = TestClient(app)


class FakeResult:
    def scalar_one(self):
        return 1


class HealthyDatabase:
    def execute(self, query):
        return FakeResult()


class UnavailableDatabase:
    def execute(self, query):
        raise SQLAlchemyError("Database connection failed")


def test_health_endpoint_returns_healthy_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_database_health_when_database_is_available():
    def override_get_db():
        yield HealthyDatabase()

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.get("/health/db")

        assert response.status_code == 200
        assert response.json() == {
            "status": "healthy",
            "database": "connected",
        }
    finally:
        app.dependency_overrides.clear()


def test_database_health_when_database_is_unavailable():
    def override_get_db():
        yield UnavailableDatabase()

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.get("/health/db")

        assert response.status_code == 503
        assert response.json() == {
            "status": "unhealthy",
            "database": "unavailable",
        }
    finally:
        app.dependency_overrides.clear()