
from ibm_watsonx_orchestrate.cli.commands.agents import agents_command

def test_agent_import_call(capsys):
    agents_command.agent_import(file="test_file")
    captured = capsys.readouterr()
    assert captured.out == "Agent Import feature is not implemented yet\n"