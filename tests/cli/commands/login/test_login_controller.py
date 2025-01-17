import os
from ibm_watsonx_orchestrate.cli.commands.login import login_controller
from ibm_watsonx_orchestrate.cli.config import Config
import jwt
from unittest.mock import patch
from ibm_watsonx_orchestrate.client.client_errors import ClientError


class MockConfig:
    def __init__(self, file):
        configs_folder = os.path.join(os.path.dirname(__file__), "../../resources/configs")
        self.cfg = Config(configs_folder, file)
        self.cfg.save = self.save

    def __call__(self, folder=None, file=None):
        return self.cfg

    def save(self, obj):
        pass


class MockClient:
    def __init__(self, credentials):
        self.token = "test_token"


class MockErrorClient:
    def __init__(self, credentials):
        raise ClientError("Testing client error")


class MockCredentials:
    def __init__(self, url, api_key):
        pass

    # def _set_env_vars_from_credentials(args):
    #     return {}


def test_decode_invalid_jwt():
    fake_jwt = "Not a real Token"
    try:
        login_controller.decode_token(fake_jwt)
        assert False
    except jwt.DecodeError as e:
        assert True


def test_decode_valid_jwt_missing_field():
    jwt_sample_file = os.path.join(os.path.dirname(__file__), "../../resources/jwt/jwt_missing_fields")
    with open(jwt_sample_file, "r") as f:
        jwt = f.readline()
        try:
            login_controller.decode_token(jwt)
            assert False
        except KeyError as e:
            assert True


def test_decode_valid_jwt():
    jwt_sample_file = os.path.join(os.path.dirname(__file__), "../../resources/jwt/jwt_valid")
    with open(jwt_sample_file, "r") as f:
        jwt = f.readline()
        token_config = login_controller.decode_token(jwt)

        assert token_config["token"] == jwt
        assert token_config["expiry"] == 1736435211


@patch("ibm_watsonx_orchestrate.cli.commands.login.login_controller.Config", MockConfig("populated_config.yaml"))
@patch("ibm_watsonx_orchestrate.cli.commands.login.login_controller.Client", MockClient)
@patch("ibm_watsonx_orchestrate.cli.commands.login.login_controller.Credentials", MockCredentials)
@patch(
    "ibm_watsonx_orchestrate.cli.commands.login.login_controller.decode_token",
    return_value={"token": "test_token", "exp": 0},
)
def test_handle_provided_url_and_api_key(mock):
    login_controller.login(apikey="test_api_key", url="test_url")

    mock.assert_called_with("test_token")
    assert mock.return_value["token"] == ("test_token")
    assert mock.return_value["exp"] == 0


@patch("ibm_watsonx_orchestrate.cli.commands.login.login_controller.Config", MockConfig("populated_config.yaml"))
@patch("ibm_watsonx_orchestrate.cli.commands.login.login_controller.Client", MockClient)
@patch("ibm_watsonx_orchestrate.cli.commands.login.login_controller.Credentials", MockCredentials)
@patch(
    "ibm_watsonx_orchestrate.cli.commands.login.login_controller.decode_token",
    return_value={"token": "test_token", "exp": 0},
)
def test_handle_url_and_api_key_from_config(mock, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    login_controller.login(None, None)

    mock.assert_called_with("test_token")
    assert mock.return_value["token"] == ("test_token")
    assert mock.return_value["exp"] == 0


@patch("ibm_watsonx_orchestrate.cli.commands.login.login_controller.Config", MockConfig("empty_config.yaml"))
@patch("ibm_watsonx_orchestrate.cli.commands.login.login_controller.Client", MockClient)
@patch("ibm_watsonx_orchestrate.cli.commands.login.login_controller.Credentials", MockCredentials)
@patch(
    "ibm_watsonx_orchestrate.cli.commands.login.login_controller.decode_token",
    return_value={"token": "test_token", "exp": 0},
)
def test_handle_url_and_api_key_from_input(mock, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "test")
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    login_controller.login(None, None)

    mock.assert_called_with("test_token")
    assert mock.return_value["token"] == ("test_token")
    assert mock.return_value["exp"] == 0


@patch("ibm_watsonx_orchestrate.cli.commands.login.login_controller.Config", MockConfig("populated_config.yaml"))
@patch("ibm_watsonx_orchestrate.cli.commands.login.login_controller.Client", MockErrorClient)
@patch("ibm_watsonx_orchestrate.cli.commands.login.login_controller.Credentials", MockCredentials)
@patch(
    "ibm_watsonx_orchestrate.cli.commands.login.login_controller.decode_token",
    return_value={"token": "test_token", "exp": 0},
)
def test_handle_client_errors(mock, capsys):
    login_controller.login("test", "test")
    captured = capsys.readouterr()
    assert captured.out == "Failed Login Attempt\n"
