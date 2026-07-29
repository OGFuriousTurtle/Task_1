import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = "openai/gpt-oss-120b"

PERSONAS = {
    "RoastBot 🔥": {
        "emoji": "🔥",
        "system_prompt": (
            "Act as a savage standup comic on India's Got Latent. Your only job is "
            "to relentlessly roast whatever the user says. Tear into their arguments "
            "and vibe. Keep it short, punchy, and sarcastic — 2 to 4 sentences max."
        ),
    },
    "ShakespeareBot 🎭": {
        "emoji": "🎭",
        "system_prompt": (
            "For this act, channel the spirit of William Shakespeare. Every response "
            "must be dripping with flowery Early Modern English (thee, thou, doth, verily). "
            "Stay in character no matter what they ask, add some dramatic flair, and maybe "
            "drop a rhyming couplet."
        ),
    },
    "Emoji Translator Bot 😂": {
        "emoji": "😂",
        "system_prompt": (
            "Don't use any actual words. Reply to everything using exclusively emojis. "
            "Make it a dense, playful string of symbols that actually conveys meaning "
            "rather than just random spam."
        ),
    },
"BPHC Burnout Bot 🩴": {
        "emoji": "🩴",
        "system_prompt": (
            "Act as a chronically exhausted BITS Pilani Hyderabad student. "
            "Whenever the user asks a difficult or complex question, deflect it by "
            "telling them to 'lite lo' and refuse to elaborate. Constantly complain "
            "about how an 8 AM morning tut absolutely wrecked your day, or cry about "
            "how the new mandatory attendance policy is destroying campus culture. "
        ),
    },
}

st.set_page_config(page_title="India's Got Latent — Chatbot Act", page_icon="🎤", layout="centered")

st.title("🎤 India's Got Latent: Chatbot Act")

if "persona" not in st.session_state:
    st.session_state.persona = None
if "messages" not in st.session_state:
    st.session_state.messages = []

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("Error: GROQ_API_KEY is missing from environment variables.")
    st.stop()

client = Groq(api_key=api_key)

if st.session_state.persona is None:
    st.subheader("Pick your act before you walk on stage 🎬")
    choice = st.selectbox("Choose a persona:", list(PERSONAS.keys()))
    st.write(f"**Preview:** {PERSONAS[choice]['system_prompt'][:120]}...")
    if st.button("🎤 Start the show", type="primary"):
        st.session_state.persona = choice
        st.session_state.messages = [
            {"role": "system", "content": PERSONAS[choice]["system_prompt"]}
        ]
        st.rerun()
    st.stop()

current = st.session_state.persona
col1, col2 = st.columns([4, 1])
with col1:
    st.info(f"**Current act:** {current}")
with col2:
    if st.button("🔄 Restart"):
        st.session_state.persona = None
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    avatar = PERSONAS[current]["emoji"] if msg["role"] == "assistant" else "🧑‍⚖️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask the bot something, judges...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍⚖️"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar=PERSONAS[current]["emoji"]):
        with st.spinner("thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    temperature=0.9,
                    max_tokens=400,
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"[Error contacting Groq API: {e}]"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
