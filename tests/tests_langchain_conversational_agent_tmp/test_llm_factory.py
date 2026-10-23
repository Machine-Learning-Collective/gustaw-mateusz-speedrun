import pytest
from langchain_core.messages import HumanMessage

from LangChain_Conversational_Agent.llm_factory import DEFAULT_OPENAI_MODEL, DemoChatModel, LLMSettings, build_llm


def test_no_key_means_demo_mode() -> None:
    settings = LLMSettings.from_env({})
    assert settings.provider == "demo"
    assert isinstance(build_llm(settings, {}), DemoChatModel)


def test_api_key_selects_openai_with_default_model() -> None:
    settings = LLMSettings.from_env({"OPENAI_API_KEY": "sk-test"})
    assert settings.provider == "openai"
    assert settings.model == DEFAULT_OPENAI_MODEL
    assert settings.temperature is None
    assert settings.describe() == f"openai ({DEFAULT_OPENAI_MODEL})"


def test_explicit_provider_wins_over_key() -> None:
    settings = LLMSettings.from_env({"OPENAI_API_KEY": "sk-test", "LLM_PROVIDER": "Demo"})
    assert settings.provider == "demo"


def test_model_and_temperature_from_env() -> None:
    settings = LLMSettings.from_env(
        {"OPENAI_API_KEY": "sk-test", "OPENAI_MODEL": "gpt-test", "LLM_TEMPERATURE": "0.2"}
    )
    assert settings.model == "gpt-test"
    assert settings.temperature == 0.2


def test_unknown_provider_rejected() -> None:
    with pytest.raises(ValueError):
        LLMSettings.from_env({"LLM_PROVIDER": "skynet"})


def test_openai_without_key_fails_clearly() -> None:
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        build_llm(LLMSettings(provider="openai"), {})


def test_openai_model_built_without_network_call() -> None:
    llm = build_llm(LLMSettings(provider="openai", model="gpt-test"), {"OPENAI_API_KEY": "sk-test"})
    assert type(llm).__name__ == "ChatOpenAI"
    assert llm.model_name == "gpt-test"


def test_temperature_only_sent_when_configured() -> None:
    env = {"OPENAI_API_KEY": "sk-test"}
    model = "gpt-4.1-mini"  # GPT-5 models reject explicit temperatures; langchain-openai drops them
    assert build_llm(LLMSettings(provider="openai", model=model), env).temperature is None
    assert build_llm(LLMSettings(provider="openai", model=model, temperature=0.3), env).temperature == 0.3


def test_demo_model_echoes_and_counts_history() -> None:
    reply = DemoChatModel().invoke([HumanMessage("first"), HumanMessage("second")])
    assert '"second"' in reply.text
    assert "1 earlier message " in reply.text
