from api.api_manager import ApiManager
from conftest import admin_super_session, created_movie
from utils.data_generator import DataGenerator


class TestMovieAPI:
    api_manager = ApiManager(admin_super_session)
    def test_get_movies(self, api_manager):
        response = api_manager.movie_api.get_movies()
        response_data = response.json()
        assert response_data != []

    def test_get_movie_with_query(self, api_manager, get_movie_params):
        response = api_manager.movie_api.get_movie_with_query(**get_movie_params)
        assert response != []

    def test_get_movie_by_id(self, api_manager, movie_id):
        response = api_manager.movie_api.get_movie_by_id(movie_id)
        assert response.json()["id"] == movie_id

    def test_create_movie(self, admin_super_session, movie_data):
        api_manager = ApiManager(admin_super_session)
        response = api_manager.movie_api.create_movie(movie_data)
        assert response.status_code == 201, "Произошла ошибка при создании фильма"
        assert response.json()["name"] == movie_data["name"], "Имя не совпадает"

    def test_update_movie(self, admin_api_manager, movie_data, created_movie):
        movie_id = created_movie["id"]
        response = admin_api_manager.movie_api.update_movie(movie_id, movie_data)
        assert response.status_code == 200, "Ошибка при обновлении данных"

    def test_delete_movie(self, admin_api_manager, movie_id, created_movie):
        movie_id = created_movie["id"]
        response = admin_api_manager.movie_api.delete_movie(movie_id)

class TestNegativeMovieAPI:
    def test_create_movie_conflict(self, admin_api_manager):
        movie_name = "Witcher"
        movie_data = {
            "name": movie_name,
            "imageUrl": "https://example.com/image.png",
            "price": 100,
            "description": "Описание фильма",
            "location": "SPB",
            "published": True,
            "genreId": 1
        }

        admin_api_manager.movie_api.create_movie(movie_data, expected_status=409)
        response = admin_api_manager.movie_api.create_movie(movie_data, expected_status=409)
        assert response.status_code == 409, "Фильм создался"

    def test_get_movie_by_invalid_id(self, admin_api_manager):
        response = admin_api_manager.movie_api.get_movie_by_id(DataGenerator.generate_random_int(42000, 100000),expected_status=404)
        assert response.status_code == 404, "Фильм найден"

    def test_delete_by_invalid_id(self, admin_api_manager):
        response = admin_api_manager.movie_api.delete_movie(DataGenerator.generate_random_int(42000, 100000),expected_status=404)
        assert response.status_code == 404, "Фильм удалился"

    def test_update_by_invalid_data(self, admin_api_manager, created_movie):
        movie_id = created_movie["id"]
        data = {
            "name": DataGenerator.generate_random_int(1, 100),
            "price": -100,
            "imageUrl": "https://example.com/image.png",
            "description": DataGenerator.generate_random_sentence(5),
            "location": "MSK",
            "published": DataGenerator.generate_random_sentence(3),
            "genreId": DataGenerator.generate_random_boolean()
        }

        response = admin_api_manager.movie_api.update_movie(movie_id, data, expected_status=400)
        assert response.status_code == 400, "Данные обновлены"