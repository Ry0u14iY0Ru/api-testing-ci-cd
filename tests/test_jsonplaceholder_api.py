import requests
import pytest
import json
import time
from typing import Dict, Any


BASE_URL = "https://jsonplaceholder.typicode.com"


class TestJSONPlaceholderAPI:
    """Тесты для JSONPlaceholder API"""
    
    @pytest.fixture
    def test_user_data(self):
        """Фикстура с тестовыми данными пользователя"""
        return {
            "name": "Test User",
            "username": "testuser",
            "email": "test.user@example.com",
            "address": {
                "street": "Test Street",
                "suite": "Apt. 100",
                "city": "Test City",
                "zipcode": "12345",
                "geo": {"lat": "0", "lng": "0"}
            },
            "phone": "1-234-567-8900",
            "website": "testuser.com",
            "company": {
                "name": "Test Company",
                "catchPhrase": "Test phrase",
                "bs": "Test business"
            }
        }
    
    def test_get_user_success(self):
        """Тест успешного получения пользователя"""
        response = requests.get(f"{BASE_URL}/users/1")
        
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        
        user_data = response.json()
        
        # Проверка обязательных полей
        required_fields = ["id", "name", "username", "email", "address", "phone", "website", "company"]
        for field in required_fields:
            assert field in user_data
        
        # Проверка значений
        assert user_data["id"] == 1
        assert "@" in user_data["email"]
        assert isinstance(user_data["address"], dict)
    
    def test_get_all_users(self):
        """Тест получения списка всех пользователей"""
        response = requests.get(f"{BASE_URL}/users")
        
        assert response.status_code == 200
        
        users = response.json()
        assert isinstance(users, list)
        assert len(users) == 10
        
        # Проверка уникальности ID
        user_ids = [user["id"] for user in users]
        assert len(set(user_ids)) == len(users)
    
    def test_create_user(self, test_user_data):
        """Тест создания нового пользователя"""
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(
            f"{BASE_URL}/users",
            data=json.dumps(test_user_data),
            headers=headers
        )
        
        assert response.status_code == 201
        
        created_user = response.json()
        assert created_user["id"] == 11
        assert created_user["name"] == test_user_data["name"]
        assert created_user["email"] == test_user_data["email"]
    
    def test_update_user(self, test_user_data):
        """Тест обновления пользователя"""
        user_id = 1
        test_user_data["name"] = "Updated Name"
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.put(
            f"{BASE_URL}/users/{user_id}",
            data=json.dumps(test_user_data),
            headers=headers
        )
        
        assert response.status_code == 200
        
        updated_user = response.json()
        assert updated_user["id"] == user_id
        assert updated_user["name"] == "Updated Name"
    
    def test_delete_user(self):
        """Тест удаления пользователя"""
        response = requests.delete(f"{BASE_URL}/users/1")
        
        assert response.status_code in [200, 204]
    
    def test_response_performance(self):
        """Тест производительности API"""
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/users/1")
        response_time = (time.time() - start_time) * 1000
        
        assert response.status_code == 200
        assert response_time < 2000  # Меньше 2 секунд
    
    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_get_multiple_users(self, user_id):
        """Параметризованный тест для нескольких пользователей"""
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["id"] == user_id


def test_integration_flow():
    """Интеграционный тест: полный цикл работы с пользователем"""
    # 1. Создание пользователя
    new_user = {
        "name": "Integration User",
        "email": "integration@test.com",
        "username": "integration"
    }
    
    headers = {"Content-Type": "application/json"}
    create_response = requests.post(
        f"{BASE_URL}/users",
        data=json.dumps(new_user),
        headers=headers
    )
    
    assert create_response.status_code == 201
    created_user = create_response.json()
    
    # 2. Проверка создания
    get_response = requests.get(f"{BASE_URL}/users/{created_user['id']}")
    assert get_response.status_code == 200
    
    # 3. Обновление
    update_data = {"name": "Updated Integration User"}
    update_response = requests.patch(
        f"{BASE_URL}/users/{created_user['id']}",
        data=json.dumps(update_data),
        headers=headers
    )
    
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Integration User"
    
    # 4. Удаление
    delete_response = requests.delete(f"{BASE_URL}/users/{created_user['id']}")
    assert delete_response.status_code in [200, 204]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
