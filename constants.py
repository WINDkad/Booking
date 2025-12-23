BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
REGISTER_URL = f"{BASE_URL}{REGISTER_ENDPOINT}"
LOGIN_URL = f"{BASE_URL}{LOGIN_ENDPOINT}"
