import requests

BASE_URL = "http://127.0.0.1:8000"
AUTH_ROOT = ("root", "12345")  # Пользователь root
AUTH_OTHER = ("otheruser", "password123")  # Другой пользователь


def test_create_password(auth=AUTH_ROOT):
    print("Тест создания/обновления пароля...")
    url = f"{BASE_URL}/password/yundex/"
    data = {"password": "very_secret_pass"}
    response = requests.post(url, json=data, auth=auth)

    if response.status_code == 201:
        print("Пароль успешно создан.")
        return True
    elif response.status_code == 200:
        print("Пароль успешно обновлен.")
        return True
    else:
        print(f"Ошибка создания/обновления пароля: {response.status_code}")
        print(response.json())
        return False


def test_retrieve_password(auth=AUTH_ROOT):
    print("Тест получения пароля по имени сервиса...")
    url = f"{BASE_URL}/password/yundex/"
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        password_data = response.json()
        print(f"Получен пароль: {password_data['password']}, service_name: {password_data['service_name']}")
        return True
    else:
        print(f"Ошибка получения пароля: {response.status_code}")
        print(response.json())
        return False


def test_search_passwords(auth=AUTH_ROOT):
    print("Тест поиска паролей по части имени сервиса...")
    url = f"{BASE_URL}/password/?service_name=yun"
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        passwords = response.json()
        if passwords:
            print(f"Найдено совпадений: {len(passwords)}")
            for item in passwords:
                print(f"service_name: {item['service_name']}, password: {item['password']}")
            return True
        else:
            print("Совпадений не найдено.")
            return False
    else:
        print(f"Ошибка поиска паролей: {response.status_code}")
        print(response.json())
        return False


def test_unauthorized_access():
    print("Тест доступа без авторизации...")
    url = f"{BASE_URL}/password/yundex/"
    response = requests.get(url)

    if response.status_code == 401:
        print("Доступ без авторизации запрещен (OK).")
        return True
    else:
        print(f"Ошибка: доступ без авторизации разрешен ({response.status_code}).")
        return False



def run_tests():
    print("Запуск ручных тестов...")
    tests = [
        ("Создание пароля", test_create_password),
        ("Получение пароля", test_retrieve_password),
        ("Поиск паролей", test_search_passwords),
        ("Доступ без авторизации", test_unauthorized_access),
    ]

    all_passed = True
    for name, test_func in tests:
        print(f"\n--- Тест: {name} ---")
        result = test_func()
        if not result:
            all_passed = False

    if all_passed:
        print("\nВсе тесты прошли успешно!")
    else:
        print("\nНекоторые тесты не прошли.")


if __name__ == "__main__":
    run_tests()