from ibm_watsonx_orchestrate.cli.commands.login import login_command
from unittest.mock import patch

def test_login_call_no_params():
    with patch("ibm_watsonx_orchestrate.cli.commands.login.login_command.login_controller.login") as mock:
        login_command.login(local=True)
        mock.assert_called_once_with(apikey=None, url="http://localhost:4321", is_local=True)


def test_login_call_params():
    with patch("ibm_watsonx_orchestrate.cli.commands.login.login_command.login_controller.login") as mock:
        login_command.login(apikey="test_key", url="test_url")
        mock.assert_called_once_with(apikey="test_key", url="test_url", is_local= False)

