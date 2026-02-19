import pytest
from agent.sources.glm import GLMModel
from agent.model import Message
from tests.config import get_source_config, has_source_api_key


@pytest.mark.integration
def test_glm_initialization():
  model = GLMModel(api_key="fake-key-for-test")
  assert model.api_key == "fake-key-for-test"
  assert model.model == "glm-4.7-flash"


@pytest.mark.integration
@pytest.mark.skipif(not has_source_api_key("glm"), reason="No ZAI_API_KEY environment variable")
def test_glm_real_api_call():
  config = get_source_config("glm")
  model = GLMModel(api_key=config.api_key, model=config.model)
  messages = [Message(role="user", content="Say 'hello'")]
  response = model.generate_completion(messages)
  assert response.content is not None
  assert len(response.content) > 0
  assert "hello" in response.content.lower()


@pytest.mark.integration
@pytest.mark.skipif(not has_source_api_key("glm"), reason="No ZAI_API_KEY environment variable")
def test_glm_real_api_with_tools():
  from agent.model import Tool

  config = get_source_config("glm")
  model = GLMModel(api_key=config.api_key, model=config.model)

  tools = [
    Tool(
      name="get_weather",
      description="Get weather information",
      parameters={"type": "object", "properties": {"location": {"type": "string"}}},
    )
  ]

  messages = [Message(role="user", content="What's the weather in Tokyo?")]
  response = model.generate_completion(messages, tools)
  assert response is not None
  assert hasattr(response, "content")


@pytest.mark.integration
def test_glm_payload_preparation():
  model = GLMModel(api_key="test-key")
  messages = [
    Message(role="system", content="You are helpful"),
    Message(role="user", content="Hello"),
  ]
  payload = model._prepare_payload(messages)
  assert payload["model"] == "glm-4.7-flash"
  assert len(payload["messages"]) == 2
  assert payload["messages"][0]["role"] == "system"
  assert payload["messages"][1]["role"] == "user"


@pytest.mark.integration
def test_glm_tool_formatting():
  from agent.model import Tool

  model = GLMModel(api_key="test-key")
  tool = Tool(name="test_tool", description="A test tool", parameters={"type": "object"})
  formatted = model._format_tool(tool)
  assert formatted["type"] == "function"
  assert formatted["function"]["name"] == "test_tool"
  assert formatted["function"]["description"] == "A test tool"
  assert formatted["function"]["parameters"] == {"type": "object"}
