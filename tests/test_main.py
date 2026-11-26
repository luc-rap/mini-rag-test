import pytest
from fastapi.testclient import TestClient

from app import llm
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_returns_answer(monkeypatch):
    async def fake_generate(prompt):
        return f"fake answer to: {prompt}"

    monkeypatch.setattr(llm, "generate", fake_generate)

    response = client.post("/ask", json={"question": "hello"})

    assert response.status_code == 200
    assert response.json() == {"answer": "fake answer to: hello"}


@pytest.mark.parametrize("body", [{}, {"question": ""}, {"question": 123}])
def test_ask_rejects_invalid_input(body):
    response = client.post("/ask", json=body)
    assert response.status_code == 422


def test_ask_returns_502_when_model_fails(monkeypatch):
    async def failing_generate(prompt):
        raise ConnectionError("model is down")

    monkeypatch.setattr(llm, "generate", failing_generate)

    response = client.post("/ask", json={"question": "hello"})

    assert response.status_code == 502