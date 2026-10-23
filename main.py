"""Terminal chat. Same as `python -m langchain_conversational_agent.cli`, runnable from the project root."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from langchain_conversational_agent.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
