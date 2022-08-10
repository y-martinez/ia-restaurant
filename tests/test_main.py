import pytest

from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.connection import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello World"}


def test_create_product():

    # POST
    good_data = {"name": "Soda", "price": 10.5, "sku": "P-A12345", "stock": 100}
    bad_data_missing = {"name": "Soda", "price": 10.5, "sku": "P-A12345"}
    bad_data_duplicate_sku = {
        "name": "Burger",
        "price": 3.0,
        "sku": "P-A12345",
        "stock": 100,
    }

    response = client.post("api/v1/products", json=good_data)
    assert response.status_code == status.HTTP_201_CREATED

    data_commited = response.json()
    assert good_data["name"] == data_commited["name"]
    assert good_data["price"] == data_commited["price"]
    assert good_data["sku"] == data_commited["sku"]
    assert good_data["stock"] == data_commited["stock"]

    response = client.post("api/v1/products", json=bad_data_missing)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.post("api/v1/products", json=bad_data_duplicate_sku)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"] == "SKU already on inventory"


def test_read_all_products():

    additional_data = {"name": "Burger", "price": 1, "sku": "P-A13453", "stock": 100}

    response = client.post("api/v1/products", json=additional_data)
    response = client.get("api/v1/products")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

    response = client.get("api/v1/products", params={"offset": 2})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0

    response = client.get("api/v1/products", params={"offset": 1})
    assert response.status_code == status.HTTP_200_OK

    data_response = response.json()

    assert data_response[0]["name"] == additional_data["name"]
    assert data_response[0]["price"] == additional_data["price"]
    assert data_response[0]["sku"] == additional_data["sku"]
    assert data_response[0]["stock"] == additional_data["stock"]

    response = client.get("api/v1/products", params={"limit": 1})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
