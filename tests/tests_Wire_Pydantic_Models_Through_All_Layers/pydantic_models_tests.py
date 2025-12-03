def test_chat_request_invalid_message_type(client):
    # message powinno być str, wysyłamy dict
    resp = client.post("/chat", json={"message": {"foo": "bar"}, "session_id": "x"})
    assert resp.status_code == 422


def test_chat_response_contract(monkeypatch, client):
    from FastApi_Skeleton.main import agent

    def fake_send(msg: str, session_id: str = "default") -> str:
        return "hello"
    def fake_get_history(session_id: str = "default"):
        return []  # poprawny List[Message] zweryfikowany w innych testach

    monkeypatch.setattr(agent, "send", fake_send)
    monkeypatch.setattr(agent, "get_history", fake_get_history)

    resp = client.post("/chat", json={"message": "hi", "session_id": "sess"})
    assert resp.status_code == 200
    data = resp.json()
    assert set(data.keys()) == {"session_id", "message", "history"}
    assert set(data["message"].keys()) >= {"role", "content"}
    assert isinstance(data["history"], list)
