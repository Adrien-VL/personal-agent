from abc import ABC, abstractmethod
from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class Message:
  role: str
  content: str


@dataclass
class Tool:
  name: str
  description: str
  parameters: dict[str, Any]


@dataclass
class ToolCall:
  id: str
  name: str
  arguments: str


@dataclass
class CompletionResponse:
  content: str
  tool_calls: list[ToolCall]
  finish_reason: str


class BaseModel(ABC):
  @abstractmethod
  def generate_completion(
    self, messages: list[Message], tools: Optional[list[Tool]] = None
  ) -> CompletionResponse:
    pass

  @abstractmethod
  async def generate_completion_async(
    self, messages: list[Message], tools: Optional[list[Tool]] = None
  ) -> CompletionResponse:
    pass
