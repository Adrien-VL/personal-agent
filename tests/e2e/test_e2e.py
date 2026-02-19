import pytest
from agent.ghost import Ghost
from agent.shell import Shell
from agent.sources.glm import GLMModel
from agent.model import Message
from tests.config import get_source_config, has_source_api_key


@pytest.mark.e2e
@pytest.mark.skipif(not has_source_api_key("glm"), reason="No ZAI_API_KEY environment variable")
def test_e2e_ghost_shell_glm_conversation():
  config = get_source_config("glm")
  model = GLMModel(api_key=config.api_key, model=config.model)
  ghost = Ghost(model=model)
  shell = Shell(ghost=ghost)

  user_message = Message(role="user", content="Say 'test passed'")
  response = shell.process_input(user_message)

  assert response.content is not None
  assert len(response.content) > 0
  assert "test passed" in response.content.lower()

  assert len(ghost.get_conversation_history()) == 2
  assert ghost.get_conversation_history()[0].role == "user"
  assert ghost.get_conversation_history()[1].role == "assistant"


@pytest.mark.e2e
@pytest.mark.skipif(not has_source_api_key("glm"), reason="No ZAI_API_KEY environment variable")
def test_e2e_multi_turn_conversation():
  config = get_source_config("glm")
  model = GLMModel(api_key=config.api_key, model=config.model)
  ghost = Ghost(model=model)
  shell = Shell(ghost=ghost)

  shell.process_input(Message(role="user", content="My name is Alice"))
  response2 = shell.process_input(Message(role="user", content="What is my name?"))

  assert response2.content is not None
  assert "alice" in response2.content.lower()

  assert len(ghost.get_conversation_history()) == 4


@pytest.mark.e2e
@pytest.mark.skipif(not has_source_api_key("glm"), reason="No ZAI_API_KEY environment variable")
def test_e2e_shell_with_input_port():
  config = get_source_config("glm")
  model = GLMModel(api_key=config.api_key, model=config.model)
  ghost = Ghost(model=model)
  shell = Shell(ghost=ghost)

  def prefix_enhancer(msg: Message) -> Message:
    msg.content = f"[Test Mode] {msg.content}"
    return msg

  input_port = shell.input_ports.get("default")
  if input_port is None:
    from agent.shell import InputPort

    input_port = InputPort("default")
    shell.add_input_port(input_port)

  input_port.add_enhancer(prefix_enhancer)

  response = shell.process_input(Message(role="user", content="Say hello"))

  assert response.content is not None
  assert len(response.content) > 0


@pytest.mark.e2e
@pytest.mark.skipif(not has_source_api_key("glm"), reason="No ZAI_API_KEY environment variable")
def test_e2e_shell_with_context_enhancer():
  from agent.shell import WebSearchEnhancer

  config = get_source_config("glm")
  model = GLMModel(api_key=config.api_key, model=config.model)
  ghost = Ghost(model=model)
  shell = Shell(ghost=ghost)

  shell.add_context_enhancer(WebSearchEnhancer())

  response = shell.process_input(Message(role="user", content="Say hello"))

  assert response.content is not None
  assert len(response.content) > 0


@pytest.mark.e2e
@pytest.mark.skipif(not has_source_api_key("glm"), reason="No ZAI_API_KEY environment variable")
def test_e2e_ghost_internal_state():
  config = get_source_config("glm")
  model = GLMModel(api_key=config.api_key, model=config.model)
  ghost = Ghost(model=model)

  ghost.update_internal_state("user_name", "Bob")
  assert ghost.get_internal_state("user_name") == "Bob"

  ghost.update_internal_state("user_id", 12345)
  assert ghost.get_internal_state("user_id") == 12345

  assert ghost.get_internal_state("nonexistent") is None
