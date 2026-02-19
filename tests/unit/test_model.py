import pytest
from agent.model import Message, Tool, ToolCall, CompletionResponse


@pytest.mark.unit
def test_message_creation():
  message = Message(role="user", content="test")
  assert message.role == "user"
  assert message.content == "test"


@pytest.mark.unit
def test_tool_creation():
  tool = Tool(name="test_tool", description="A test tool", parameters={"type": "object"})
  assert tool.name == "test_tool"
  assert tool.description == "A test tool"
  assert tool.parameters == {"type": "object"}


@pytest.mark.unit
def test_tool_call_creation():
  tool_call = ToolCall(id="call_123", name="test_tool", arguments='{"key": "value"}')
  assert tool_call.id == "call_123"
  assert tool_call.name == "test_tool"
  assert tool_call.arguments == '{"key": "value"}'


@pytest.mark.unit
def test_completion_response_creation():
  response = CompletionResponse(content="Test response", tool_calls=[], finish_reason="stop")
  assert response.content == "Test response"
  assert response.tool_calls == []
  assert response.finish_reason == "stop"


@pytest.mark.unit
def test_completion_response_with_tool_calls():
  tool_call = ToolCall(id="call_123", name="test_tool", arguments='{"key": "value"}')
  response = CompletionResponse(content="", tool_calls=[tool_call], finish_reason="tool_calls")
  assert len(response.tool_calls) == 1
  assert response.tool_calls[0].id == "call_123"
