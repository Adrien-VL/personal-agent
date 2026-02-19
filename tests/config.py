import os
from dataclasses import dataclass


@dataclass
class SourceConfig:
  name: str
  api_key: str
  model: str
  base_url: str


TEST_SOURCES = {
  "glm": SourceConfig(
    name="glm",
    api_key=os.getenv("ZAI_API_KEY", ""),
    model="glm-4.7-flash",
    base_url="https://api.z.ai/api/coding/paas/v4",
  ),
}


def get_source_config(source_name: str) -> SourceConfig:
  config = TEST_SOURCES.get(source_name)
  if not config:
    raise ValueError(f"Unknown test source: {source_name}")
  return config


def has_source_api_key(source_name: str) -> bool:
  config = get_source_config(source_name)
  return bool(config.api_key)
