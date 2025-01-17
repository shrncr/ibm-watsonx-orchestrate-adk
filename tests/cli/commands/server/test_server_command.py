from ibm_watsonx_orchestrate.cli.commands.server import server_command

def test_server_start_call(capsys):
    server_command.server_start()
    captured = capsys.readouterr()
    assert captured.out == "Server Start feature is not implemented yet\n"