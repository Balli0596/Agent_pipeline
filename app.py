
from agent.controller import build_agent, ask_agent


def main():
    print("=" * 50)
    print("AI Agent with Weather and Stock Tools")
    print("Type 'exit' to quit.")
    print("=" * 50)

    agent = build_agent()

    while True:
        try:
            query = input("\nYou: ").strip()

            if query.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break

            if not query:
                continue

            response = ask_agent(agent, query)
            print(f"\nAssistant: {response}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        except Exception as exc:
            print(f"\nError: {exc}")


if __name__ == "__main__":
    main()
