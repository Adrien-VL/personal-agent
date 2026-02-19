import pytest
from unittest.mock import MagicMock
from agent.model import Message, CompletionResponse
from agent.ghost import Ghost


@pytest.fixture
def mock_model():
  model = MagicMock()
  model.generate_completion.return_value = CompletionResponse(
    content="Mock response", tool_calls=[], finish_reason="stop"
  )
  return model


@pytest.mark.unit
def test_ghost_initialization(mock_model):
  ghost = Ghost(model=mock_model)
  assert ghost.model == mock_model
  assert ghost.conversation_history == []
  assert ghost.internal_state == {}


@pytest.mark.unit
def test_ghost_adds_message_to_history(mock_model):
  ghost = Ghost(model=mock_model)
  message = Message(role="user", content="test")
  ghost.add_message(message)
  assert len(ghost.conversation_history) == 1
  assert ghost.conversation_history[0] == message


@pytest.mark.unit
def test_ghost_adds_multiple_messages(mock_model):
  ghost = Ghost(model=mock_model)
  messages = [
    Message(role="user", content="message 1"),
    Message(role="assistant", content="response 1"),
    Message(role="user", content="message 2"),
  ]
  for msg in messages:
    ghost.add_message(msg)
  assert len(ghost.conversation_history) == 3


@pytest.mark.unit
def test_ghost_get_conversation_history_returns_copy(mock_model):
  ghost = Ghost(model=mock_model)
  message = Message(role="user", content="test")
  ghost.add_message(message)
  history = ghost.get_conversation_history()
  history.append(Message(role="user", content="modified"))
  assert len(ghost.conversation_history) == 1
  assert len(history) == 2


@pytest.mark.unit
def test_ghost_clear_history(mock_model):
  ghost = Ghost(model=mock_model)
  ghost.add_message(Message(role="user", content="test1"))
  ghost.add_message(Message(role="assistant", content="test2"))
  ghost.clear_history()
  assert ghost.conversation_history == []


@pytest.mark.unit
def test_ghost_update_internal_state(mock_model):
  ghost = Ghost(model=mock_model)
  ghost.update_internal_state("key1", "value1")
  ghost.update_internal_state("key2", 42)
  assert ghost.get_internal_state("key1") == "value1"
  assert ghost.get_internal_state("key2") == 42


@pytest.mark.unit
def test_ghost_get_nonexistent_internal_state(mock_model):
  ghost = Ghost(model=mock_model)
  assert ghost.get_internal_state("nonexistent") is None


@pytest.mark.unit
def test_ghost_process_calls_model(mock_model):
  ghost = Ghost(model=mock_model)
  message = Message(role="user", content="test")
  ghost.add_message(message)
  response = ghost.process()
  mock_model.generate_completion.assert_called_once()
  assert response.content == "Mock response"


@pytest.mark.unit
def test_ghost_process_with_context(mock_model):
  ghost = Ghost(model=mock_model)
  ghost.add_message(Message(role="user", content="test"))
  ghost.process(context={"context_key": "context_value"})
  mock_model.generate_completion.assert_called_once()
  call_args = mock_model.generate_completion.call_args[0][0]
  assert call_args[0].role == "system"
  assert "context_key: context_value" in call_args[0].content


@pytest.mark.unit
def test_ghost_process_with_multiple_messages(mock_model):
  ghost = Ghost(model=mock_model)
  ghost.add_message(Message(role="user", content="Hello"))
  ghost.add_message(Message(role="assistant", content="Hi there!"))
  ghost.add_message(Message(role="user", content="How are you?"))
  ghost.process()
  call_args = mock_model.generate_completion.call_args[0][0]
  assert len(call_args) == 3
  assert call_args[0].role == "user"
  assert call_args[1].role == "assistant"
  assert call_args[2].role == "user"
