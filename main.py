"""Terminal chat. Same as `python -m LangChain_Conversational_Agent.cli`, runnable from the project root."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from LangChain_Conversational_Agent.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
