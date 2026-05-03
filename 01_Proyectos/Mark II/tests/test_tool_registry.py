from core.tools import TOOL_DECLARATIONS, get_tool, get_tool_names, planner_tool_reference, registry_summary


def test_registry_has_expected_tools():
    names = set(get_tool_names())
    assert "open_app" in names
    assert "web_search" in names
    assert "file_processor" in names
    assert "cmd_control" not in names


def test_tool_declarations_match_registry():
    declared = {tool["name"] for tool in TOOL_DECLARATIONS}
    names = set(get_tool_names())
    assert declared == names
    assert get_tool("open_app") is not None


def test_planner_reference_is_generated():
    text = planner_tool_reference()
    assert "open_app" in text
    assert "file_controller" in text
    assert "cmd_control" not in text


def test_registry_summary_shape():
    summary = registry_summary()
    assert summary["tool_count"] == len(TOOL_DECLARATIONS)
    assert "categories" in summary
    assert "tools" in summary
