from constants import MOVIE_ENDPOINT, MOVIE_URL
from custom_requester.custom_requester import CustomRequester


class MovieAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIE_URL)

    def get_movies(self, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=MOVIE_ENDPOINT,
            expected_status=expected_status
        )

    def get_movie_with_query(self, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=MOVIE_ENDPOINT,
            params=kwargs,
            expected_status=expected_status
        )

    def get_movie_by_id(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=MOVIE_ENDPOINT,
            data=movie_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            expected_status=expected_status
        )

    def update_movie(self, movie_id, movie_data, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIE_ENDPOINT}/{movie_id}",
            data=movie_data,
            expected_status=expected_status
        )