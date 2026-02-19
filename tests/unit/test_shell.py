import pytest
from agent.model import Message, CompletionResponse
from agent.shell import (
  InputPort,
  OutputPort,
  ContextEnhancer,
  RAGEnhancer,
  WebSearchEnhancer,
  PersistentMemoryEnhancer,
)


@pytest.fixture
def sample_message():
  return Message(role="user", content="test message")


@pytest.fixture
def sample_response():
  return CompletionResponse(content="test response", tool_calls=[], finish_reason="stop")


@pytest.mark.unit
def test_input_port_initialization():
  port = InputPort("test_port")
  assert port.name == "test_port"
  assert port.enhancers == []


@pytest.mark.unit
def test_input_port_add_enhancer():
  port = InputPort("test_port")

  def dummy_enhancer(msg: Message) -> Message:
    return msg

  port.add_enhancer(dummy_enhancer)
  assert len(port.enhancers) == 1


@pytest.mark.unit
def test_input_port_processes_message(sample_message):
  port = InputPort("test_port")

  def uppercase_enhancer(msg: Message) -> Message:
    msg.content = msg.content.upper()
    return msg

  port.add_enhancer(uppercase_enhancer)
  result = port.process(sample_message)
  assert result.content == "TEST MESSAGE"


@pytest.mark.unit
def test_input_port_processes_with_multiple_enhancers(sample_message):
  port = InputPort("test_port")

  def prefix_enhancer(msg: Message) -> Message:
    msg.content = f"[PREFIX] {msg.content}"
    return msg

  def suffix_enhancer(msg: Message) -> Message:
    msg.content = f"{msg.content} [SUFFIX]"
    return msg

  port.add_enhancer(prefix_enhancer)
  port.add_enhancer(suffix_enhancer)
  result = port.process(sample_message)
  assert result.content == "[PREFIX] test message [SUFFIX]"


@pytest.mark.unit
def test_output_port_initialization():
  port = OutputPort("test_port")
  assert port.name == "test_port"
  assert port.processors == []


@pytest.mark.unit
def test_output_port_add_processor():
  port = OutputPort("test_port")

  def dummy_processor(resp: CompletionResponse) -> CompletionResponse:
    return resp

  port.add_processor(dummy_processor)
  assert len(port.processors) == 1


@pytest.mark.unit
def test_output_port_processes_response(sample_response):
  port = OutputPort("test_port")

  def uppercase_processor(resp: CompletionResponse) -> CompletionResponse:
    resp.content = resp.content.upper()
    return resp

  port.add_processor(uppercase_processor)
  result = port.process(sample_response)
  assert result.content == "TEST RESPONSE"


@pytest.mark.unit
def test_output_port_processes_with_multiple_processors(sample_response):
  port = OutputPort("test_port")

  def prefix_processor(resp: CompletionResponse) -> CompletionResponse:
    resp.content = f"[PREFIX] {resp.content}"
    return resp

  def suffix_processor(resp: CompletionResponse) -> CompletionResponse:
    resp.content = f"{resp.content} [SUFFIX]"
    return resp

  port.add_processor(prefix_processor)
  port.add_processor(suffix_processor)
  result = port.process(sample_response)
  assert result.content == "[PREFIX] test response [SUFFIX]"


@pytest.mark.unit
def test_context_enhancer_base_initialization():
  enhancer = ContextEnhancer("test_enhancer")
  assert enhancer.name == "test_enhancer"


@pytest.mark.unit
def test_context_enhancer_enhance_returns_same_message(sample_message):
  enhancer = ContextEnhancer("test_enhancer")
  result = enhancer.enhance(sample_message)
  assert result == sample_message


@pytest.mark.unit
def test_rag_enhancer_initialization():
  enhancer = RAGEnhancer()
  assert enhancer.name == "rag"


@pytest.mark.unit
def test_rag_enhancer_custom_name():
  enhancer = RAGEnhancer("custom_rag")
  assert enhancer.name == "custom_rag"


@pytest.mark.unit
def test_rag_enhancer_enhance_returns_message(sample_message):
  enhancer = RAGEnhancer()
  result = enhancer.enhance(sample_message)
  assert result == sample_message


@pytest.mark.unit
def test_web_search_enhancer_initialization():
  enhancer = WebSearchEnhancer()
  assert enhancer.name == "web_search"


@pytest.mark.unit
def test_web_search_enhancer_custom_name():
  enhancer = WebSearchEnhancer("custom_search")
  assert enhancer.name == "custom_search"


@pytest.mark.unit
def test_persistent_memory_enhancer_initialization():
  enhancer = PersistentMemoryEnhancer()
  assert enhancer.name == "persistent_memory"


@pytest.mark.unit
def test_persistent_memory_enhancer_custom_name():
  enhancer = PersistentMemoryEnhancer("custom_memory")
  assert enhancer.name == "custom_memory"
