from ibm_watsonx_orchestrate.cli.commands.chat import chat_command

def test_chat_start_call(capsys):
    chat_command.chat_start()
    captured = capsys.readouterr()
    assert captured.out == "Chat Start feature is not implemented yet\n"