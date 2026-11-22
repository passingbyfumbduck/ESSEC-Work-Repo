from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from groq import Groq


def ask_groq(question: str, client: "Groq | None" = None) -> str:
    if not question.strip():
        raise ValueError("Question cannot be empty")

    if client is None:
        from groq import Groq

        client = Groq()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": question}],
        max_tokens=1024,
    )
    return response.choices[0].message.content
