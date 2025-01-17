from ibm_watsonx_orchestrate.cli.commands.tools import tools_controller
from typer import BadParameter
import json
from unittest.mock import patch
import os


class MockSDKResponse:
    def __init__(self, response_obj):
        self.response_obj = response_obj

    def dumps_spec(self):
        return json.dumps(self.response_obj)


# @patch("ibm_watsonx_orchestrate.cli.command.tool_import_command.create_openapi_json_tool")
# def test_openapi_params_valid(mock, capsys):
#     mock.return_value = MockSDKResponse(
#         {
#             "name": "getEmployeeTimeOff",
#             "permission": "READ_ONLY",
#         }
#     )
#     tool_import_command.handle("openapi", file="tests/cli/resources/yaml_samples/tool.yaml")
#     captured = capsys.readouterr()
#     json_captured = json.loads(str(captured.out))

#     assert mock.called
#     assert mock.call_args_list[0][1]["http_method"] == "GET"
#     assert mock.call_args_list[0][1]["http_path"] == "/employees/{employeeId}/timeoff"

#     assert json_captured["name"] == "getEmployeeTimeOff"
#     assert json_captured["permission"] == "READ_ONLY"


# def test_openapi_no_file():
#     try:
#         tool_import_command.handle("openapi", file=None)
#         assert False
#     except BadParameter:
#         assert True


def test_python_params_valid(capsys):
    # TODO: Mock importlib or Mock Tool
    tools_controller.import_tool(
        "python", file=os.path.join(os.path.dirname(__file__), "../../resources/python_samples/tool_w_metadata.py")
    )

    captured = capsys.readouterr()
    json_captured = json.loads(str(captured.out))

    assert json_captured["name"] == "myName"
    assert json_captured["permission"] == "ADMIN"


def test_python_no_file():
    try:
        tools_controller.import_tool("python", file=None)
        assert False
    except BadParameter:
        assert True


def test_skill_valid():
    tools_controller.import_tool(
        "skill",
        skillset_id="fake_skillset",
        skill_id="fake_skill",
        skill_operation_path="fake_operation_path",
    )


def test_skill_missing_args():
    try:
        tools_controller.import_tool(
            "skill", skillset_id=None, skill_id=None, skill_operation_path=None
        )
        assert False
    except BadParameter:
        assert True


def test_invalid_kind():
    try:
        tools_controller.import_tool("invalid")
        assert False
    except ValueError as e:
        assert True
        assert str(e) == "Invalid kind selected"
