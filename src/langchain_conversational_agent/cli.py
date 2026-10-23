# cli.py
from dotenv import load_dotenv
from pydantic import ValidationError

from langchain_conversational_agent.langchain_agent import LangChainAgent
from langchain_conversational_agent.llm_factory import LLMSettings, build_llm
from pydantic_base_models import ConversationConfig


def main() -> None:
    load_dotenv()
    settings = LLMSettings.from_env()
    agent = LangChainAgent(llm=build_llm(settings), config=ConversationConfig())
    session_id = "cli"

    print(f"Model: {settings.describe()}. Type 'exit' to quit, 'reset' to start over.")
    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            break

        if user_input.lower() in {"exit", "quit"}:
            print("bye")
            break
        if user_input.lower() == "reset":
            agent.reset(session_id)
            print("agent> Conversation cleared.")
            continue
        if not user_input:
            print("agent> Please say something.")
            continue

        try:
            reply = agent.send(user_input=user_input, session_id=session_id)
        except ValidationError as exc:
            print(f"agent> {exc.errors()[0]['msg']}")
            continue
        except Exception as exc:
            print(f"agent> The language model request failed: {exc}")
            continue
        print(f"agent> {reply}")


if __name__ == "__main__":
    main()
