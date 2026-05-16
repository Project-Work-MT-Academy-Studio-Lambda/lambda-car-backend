from tests.conftest import app_module


class FakeAuthService:
    def __init__(self, user):
        self.user = user
        self.command = None

    def login_session(self, cmd):
        self.command = cmd
        return "session-token", self.user


class TestAuthRouter:
    def test_login_sets_http_only_session_cookie(self, api_client_factory, user_factory):
        dependencies = app_module("dependencies")
        settings = app_module("settings").load_settings()
        service = FakeAuthService(user_factory())
        client = api_client_factory({dependencies.get_auth_service: lambda: service})

        response = client.post(
            "/api/v1/lambdacar/admin/auth/login",
            json={"email": "user@test.com", "password": "secret"},
        )

        assert response.status_code == 200
        assert service.command.email == "user@test.com"
        assert response.json()["user"]["email"] == "user@test.com"
        assert settings.session_cookie_name in response.cookies
        set_cookie = response.headers["set-cookie"]
        assert "HttpOnly" in set_cookie
        assert "SameSite=lax" in set_cookie

    def test_logout_clears_session_cookie(self, api_client_factory):
        client = api_client_factory({})

        response = client.post("/api/v1/lambdacar/admin/auth/logout")

        assert response.status_code == 204
        assert "lambda_car_session" in response.headers["set-cookie"]
        assert "Max-Age=0" in response.headers["set-cookie"]
