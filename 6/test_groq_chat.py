import pytest

from groq_chat import ask_groq


@pytest.fixture
def client(mocker):
    client = mocker.Mock()
    choice = mocker.Mock()
    choice.message.content = "4"
    client.chat.completions.create.return_value.choices = [choice]
    return client


def test_returns_answer(client):
    assert ask_groq("What is 2+2?", client) == "4"


def test_sends_expected_request(client):
    ask_groq("What is 2+2?", client)

    client.chat.completions.create.assert_called_once_with(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "What is 2+2?"}],
        max_tokens=1024,
    )


def test_propagates_api_failure(client):
    client.chat.completions.create.side_effect = ConnectionError("API down")

    with pytest.raises(ConnectionError, match="API down"):
        ask_groq("What is 2+2?", client)


def test_rejects_blank_question(client):
    with pytest.raises(ValueError, match="Question cannot be empty"):
        ask_groq("  ", client)

    client.chat.completions.create.assert_not_called()
