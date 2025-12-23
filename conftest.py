import random
import uuid
import pytest
import requests
from api.api_manager import ApiManager
from constants import BASE_URL, SUPER_ADMIN_CREDENTIALS, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator, faker

random_email = DataGenerator.generate_random_email()
random_name = DataGenerator.generate_random_name()
random_password = DataGenerator.generate_random_password()

@pytest.fixture()
def test_user():
    return {
        "email": f"{uuid.uuid4().hex}@example.com",
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture()
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def admin_super_session():
    session = requests.Session()
    requester = CustomRequester(session, base_url=BASE_URL)

    login_data = {
        "email": "api1@gmail.com",
        "password": "asdqwe123Q"
    }

    response = requester.send_request(method="POST", endpoint=LOGIN_ENDPOINT, data=login_data)
    token = response.json().get("accessToken")
    assert token is not None, "Токен не найден в ответе"

    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture(scope="session")
def admin_api_manager(admin_super_session):
    return ApiManager(session=admin_super_session)

@pytest.fixture()
def movie_data():
    return {
        "name": DataGenerator.generate_random_name(),
        "imageUrl": "https://example.com/image.png",
        "price": DataGenerator.generate_random_int(1, 1000),
        "description": DataGenerator.generate_random_sentence(5),
        "location": random.choice(["MSK", "SPB"]),
        "published": DataGenerator.generate_random_boolean(),
        "genreId": DataGenerator.generate_random_int(1, 5)
    }

@pytest.fixture()
def created_movie(admin_super_session, movie_data):
    api_manager = ApiManager(admin_super_session)
    response = api_manager.movie_api.create_movie(movie_data)
    assert response.status_code == 201, "Ошибка при создании фильма"
    assert response.json().get("id") is not None, "id фильма отсутствует в ответе"
    return response.json()

@pytest.fixture(scope="session")
def requester():
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session=session)

@pytest.fixture(scope="session")
def get_movie_params():
    return {
        "pageSize": faker.random_int(min=1, max=3),
        "page": faker.random_int(min=1, max=3),
        "minPrice": faker.random_int(min=100, max=500),
        "maxPrice": faker.random_int(min=501, max=1000),
        "locations": random.choice(["MSK", "SPB"]),
        "published": random.choice([True, False]),
        "genreId": faker.random_int(min=1, max=5),
        "createdAt": DataGenerator.generate_random_asc_or_desc(),
    }

@pytest.fixture(scope="session")
def movie_id(api_manager):
    response = api_manager.movie_api.get_movies()
    response_data = response.json()
    return random.choice(response_data["movies"])["id"]