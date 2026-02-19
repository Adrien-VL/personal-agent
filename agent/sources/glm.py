from openai import OpenAI, AsyncOpenAI
from typing import Optional, Any
from agent.model import BaseModel, Message, Tool, CompletionResponse, ToolCall


class GLMModel(BaseModel):
  def __init__(self, api_key: str, model: str = "glm-4.7-flash"):
    self.api_key = api_key
    self.model = model
    self.client = OpenAI(api_key=api_key, base_url="https://api.z.ai/api/coding/paas/v4")
    self.async_client = AsyncOpenAI(api_key=api_key, base_url="https://api.z.ai/api/coding/paas/v4")

  def generate_completion(
    self, messages: list[Message], tools: Optional[list[Tool]] = None
  ) -> CompletionResponse:
    payload = self._prepare_payload(messages, tools)
    response = self.client.chat.completions.create(**payload)
    return self._parse_response(response)

  async def generate_completion_async(
    self, messages: list[Message], tools: Optional[list[Tool]] = None
  ) -> CompletionResponse:
    payload = self._prepare_payload(messages, tools)
    response = await self.async_client.chat.completions.create(**payload)
    return self._parse_response(response)

  def _prepare_payload(self, messages: list[Message], tools: Optional[list[Tool]] = None) -> dict:
    payload = {
      "model": self.model,
      "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
    }
    if tools:
      payload["tools"] = [self._format_tool(tool) for tool in tools]
    return payload

  def _format_tool(self, tool: Tool) -> dict:
    return {
      "type": "function",
      "function": {
        "name": tool.name,
        "description": tool.description,
        "parameters": tool.parameters,
      },
    }

  def _parse_response(self, response: Any) -> CompletionResponse:
    choice = response.choices[0]
    message = choice.message
    content = message.content or ""
    tool_calls = []

    if hasattr(message, "tool_calls") and message.tool_calls:
      for tc in message.tool_calls:
        tool_calls.append(
          ToolCall(id=tc.id, name=tc.function.name, arguments=tc.function.arguments)
        )

    return CompletionResponse(
      content=content, tool_calls=tool_calls, finish_reason=choice.finish_reason
    )
