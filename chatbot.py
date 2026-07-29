import os
import sys

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "openai/gpt-oss-120b"


def main():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY not found. Copy .env.example to .env and add your key.")
        sys.exit(1)

    client = Groq(api_key=api_key)
    
    messages = [
        {"role": "system", "content": "Answer Questions."}
    ]

    print("=" * 50)
    print("  Simple Chatbot — type 'exit' or 'quit' to stop")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Bot: Catch you later!")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=400,
            )
        except Exception as e:
            print(f"\n[Error contacting Groq API: {e}]")
            messages.pop()  
            continue

        reply = response.choices[0].message.content
        print(f"\nBot: {reply}")

        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
