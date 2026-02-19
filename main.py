import argparse
import os
from agent import Ghost, Shell, Message, GLMModel


def create_model(source: str, api_key: str, model: str = "glm-4.7-flash"):
  if source == "glm":
    return GLMModel(api_key=api_key, model=model)
  else:
    raise ValueError(f"Unknown source: {source}")


def main():
  parser = argparse.ArgumentParser(description="Personal Agent CLI")
  parser.add_argument("--source", type=str, default="glm", help="Model source to use (e.g., glm)")
  parser.add_argument("--api-key", type=str, help="API key for the model provider")
  parser.add_argument(
    "--model",
    type=str,
    default="glm-4.7-flash",
    help="Model name (e.g., glm-4.7-flash, glm-4.7)",
  )
  args = parser.parse_args()

  api_key = args.api_key or os.environ.get("MODEL_API_KEY")
  if not api_key:
    print("Error: API key required. Provide via --api-key or MODEL_API_KEY environment variable")
    return

  try:
    model = create_model(args.source, api_key, args.model)
    ghost = Ghost(model=model)
    shell = Shell(ghost=ghost)

    print(f"Personal Agent initialized with {args.source} model: {args.model}")
    print("Type your message and press Enter to send. Type 'quit' to exit.")
    print("-" * 50)

    while True:
      try:
        user_input = input("\nYou: ").strip()
        if not user_input:
          continue
        if user_input.lower() in ["quit", "exit", "q"]:
          print("Goodbye!")
          break

        message = Message(role="user", content=user_input)
        response = shell.process_input(message)

        print(f"\nAssistant: {response.content}")
      except KeyboardInterrupt:
        print("\nGoodbye!")
        break
      except Exception as e:
        print(f"\nError: {e}")

  except Exception as e:
    print(f"Error initializing agent: {e}")


if __name__ == "__main__":
  main()
