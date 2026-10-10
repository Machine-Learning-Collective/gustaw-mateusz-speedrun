# cli.py
import sys

from langchain_community.chat_models.fake import FakeListChatModel

from Pydantic_Base_Models import ConversationConfig
from LangChain_Conversational_Agent.langchain_agent import LangChainAgent


def main() -> None:
    llm = FakeListChatModel(
        responses=[
            "Hello, how can I help you?",
            "I see.",
            "Can you tell me more?",
            "Thanks for sharing.",
        ]
    )

    config = ConversationConfig()
    agent = LangChainAgent(llm=llm, config=config)
    session_id = "cli"

    print("Type 'exit' to quit.")
    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            break

        if user_input.lower() in {"exit", "quit"}:
            print("bye")
            break

        if not user_input:
            print("agent> Please say something.")
            continue

        reply = agent.send(user_input=user_input, session_id=session_id)
        print(f"agent> {reply}")

    sys.exit(0)


if __name__ == "__main__":
    main()
