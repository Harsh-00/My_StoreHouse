from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root(): 
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"My": "Warehouse"}

def test_create_product():
    response = client.post("/product", json={"name": "Test Product", "price": 100.0, "quantity": 5})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

def test_get_all_products():
    response = client.get("/product/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product():
    # Create a product
    product_data = {"name": "Test Product get", "price": 100.0, "quantity": 10}
    create_response = client.post("/product", json=product_data)
    product_id = create_response.json()["pk"]

    # Get the product
    response = client.get(f"/product/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product get"

def test_update_product():
    # Create a product
    product_data = {"name": "Test Product update", "price": 100.0, "quantity": 10}
    create_response = client.post("/product", json=product_data)
    product_id = create_response.json()["pk"]

    # updating the product
    updated_data = {"name": "Updated Product", "price": 150.0, "quantity": 5}
    response = client.put(f"/product/{product_id}", json=updated_data)
    assert response.status_code == 200

    # Verify the update
    get_response = client.get(f"/product/{product_id}")
    assert get_response.json()["name"] == "Updated Product"

def test_delete_product():
    # Create a product
    product_data = {"name": "Test Product del", "price": 100.0, "quantity": 10}
    create_response = client.post("/product", json=product_data)
    product_id = create_response.json()["pk"]

    # Delete the product
    delete_response = client.delete(f"/product/{product_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Product deleted", "product_id": product_id}

    # Verify the product is deleted
    get_response = client.get(f"/product/{product_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Product not found"}