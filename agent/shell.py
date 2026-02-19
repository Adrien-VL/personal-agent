from typing import Callable
from agent.model import Message, CompletionResponse
from agent.ghost import Ghost


class InputPort:
  def __init__(self, name: str):
    self.name = name
    self.enhancers: list[Callable[[Message], Message]] = []

  def add_enhancer(self, enhancer: Callable[[Message], Message]):
    self.enhancers.append(enhancer)

  def process(self, message: Message) -> Message:
    for enhancer in self.enhancers:
      message = enhancer(message)
    return message


class OutputPort:
  def __init__(self, name: str):
    self.name = name
    self.processors: list[Callable[[CompletionResponse], CompletionResponse]] = []

  def add_processor(self, processor: Callable[[CompletionResponse], CompletionResponse]):
    self.processors.append(processor)

  def process(self, response: CompletionResponse) -> CompletionResponse:
    for processor in self.processors:
      response = processor(response)
    return response


class ContextEnhancer:
  def __init__(self, name: str):
    self.name = name

  def enhance(self, message: Message) -> Message:
    return message


class RAGEnhancer(ContextEnhancer):
  def __init__(self, name: str = "rag"):
    super().__init__(name)

  def enhance(self, message: Message) -> Message:
    return message


class WebSearchEnhancer(ContextEnhancer):
  def __init__(self, name: str = "web_search"):
    super().__init__(name)

  def enhance(self, message: Message) -> Message:
    return message


class PersistentMemoryEnhancer(ContextEnhancer):
  def __init__(self, name: str = "persistent_memory"):
    super().__init__(name)

  def enhance(self, message: Message) -> Message:
    return message


class Shell:
  def __init__(self, ghost: Ghost):
    self.ghost = ghost
    self.input_ports: dict[str, InputPort] = {}
    self.output_ports: dict[str, OutputPort] = {}
    self.context_enhancers: list[ContextEnhancer] = []

  def add_input_port(self, port: InputPort):
    self.input_ports[port.name] = port

  def add_output_port(self, port: OutputPort):
    self.output_ports[port.name] = port

  def add_context_enhancer(self, enhancer: ContextEnhancer):
    self.context_enhancers.append(enhancer)

  def process_input(self, message: Message, port_name: str = "default") -> CompletionResponse:
    port = self.input_ports.get(port_name, InputPort("default"))
    enhanced_message = port.process(message)

    for enhancer in self.context_enhancers:
      enhanced_message = enhancer.enhance(enhanced_message)

    self.ghost.add_message(enhanced_message)
    response = self.ghost.process()
    self.ghost.add_message(Message(role="assistant", content=response.content))

    return response

  async def process_input_async(
    self, message: Message, port_name: str = "default"
  ) -> CompletionResponse:
    port = self.input_ports.get(port_name, InputPort("default"))
    enhanced_message = port.process(message)

    for enhancer in self.context_enhancers:
      enhanced_message = enhancer.enhance(enhanced_message)

    self.ghost.add_message(enhanced_message)
    response = await self.ghost.process_async()
    self.ghost.add_message(Message(role="assistant", content=response.content))

    return response

  def process_output(
    self, response: CompletionResponse, port_name: str = "default"
  ) -> CompletionResponse:
    port = self.output_ports.get(port_name, OutputPort("default"))
    return port.process(response)
