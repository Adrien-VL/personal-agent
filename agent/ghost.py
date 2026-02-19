from typing import Optional, Any
from agent.model import Message, CompletionResponse, BaseModel


class Ghost:
  def __init__(self, model: BaseModel):
    self.model = model
    self.conversation_history: list[Message] = []
    self.internal_state: dict[str, Any] = {}

  def add_message(self, message: Message):
    self.conversation_history.append(message)

  def get_conversation_history(self) -> list[Message]:
    return self.conversation_history.copy()

  def clear_history(self):
    self.conversation_history.clear()

  def update_internal_state(self, key: str, value: Any):
    self.internal_state[key] = value

  def get_internal_state(self, key: str) -> Any:
    return self.internal_state.get(key)

  def process(self, context: Optional[dict[str, Any]] = None) -> CompletionResponse:
    messages = self._prepare_messages(context)
    return self.model.generate_completion(messages)

  async def process_async(self, context: Optional[dict[str, Any]] = None) -> CompletionResponse:
    messages = self._prepare_messages(context)
    return await self.model.generate_completion_async(messages)

  def _prepare_messages(self, context: Optional[dict[str, Any]] = None) -> list[Message]:
    messages = self.conversation_history.copy()
    if context:
      context_message = Message(role="system", content=self._format_context(context))
      messages.insert(0, context_message)
    return messages

  def _format_context(self, context: dict[str, Any]) -> str:
    parts = []
    for key, value in context.items():
      parts.append(f"{key}: {value}")
    return "\n".join(parts)
