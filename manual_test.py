import requests

BASE_URL = "http://127.0.0.1:8000/password"
AUTH = ("root", "12345")  # Укажите реальные данные

def test_set_password():
    """Тест создания или обновления пароля."""
    service_name = "github"
    data = {"password": "super_secure_password"}
    response = requests.post(f"{BASE_URL}/{service_name}/", json=data, auth=AUTH)

    print("SET PASSWORD:", response.status_code, response.json())

def test_get_password():
    """Тест получения пароля по сервису."""
    service_name = "github"
    response = requests.get(f"{BASE_URL}/{service_name}/", auth=AUTH)

    print("GET PASSWORD:", response.status_code, response.json())

def test_search_password():
    """Тест поиска паролей по части имени сервиса."""
    query = "git"
    response = requests.get(f"{BASE_URL}/?service_name={query}", auth=AUTH)

    print("SEARCH PASSWORDS:", response.status_code, response.json())

def run_tests():
    print("Running manual API tests...")
    
    print("\nTesting set password...")
    test_set_password()
    
    print("\nTesting get password...")
    test_get_password()
    
    print("\nTesting search password...")
    test_search_password()

if __name__ == "__main__":
    run_tests()
