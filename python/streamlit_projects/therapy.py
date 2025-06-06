import streamlit as st
import random
import pandas as pd
import hashlib
from datetime import datetime

st.set_page_config(page_title="Microtherapy Bot", layout="centered")

st.title("🧠 Microtherapy Bot")
st.markdown("Your 5-minute emotional reset — powered by kindness and clarity.")

# ---------------- MOOD OPTIONS ----------------
moods = {
    "😊 Happy": "You're glowing — let’s build on that energy.",
    "😢 Sad": "It's okay to feel down. Let's reflect gently.",
    "😠 Angry": "Anger is valid. Let’s breathe through it.",
    "😰 Anxious": "Anxiety is a signal. Let's ground ourselves.",
    "😐 Numb": "Feeling blank is also a feeling. Let's reawaken.",
    "💭 Reflective": "Deep thoughts today? Let’s make sense of them."
}

mood = st.selectbox("How are you feeling right now?", list(moods.keys()))
st.info(moods[mood])

# ---------------- THERAPY LOGIC ----------------
questions = {
    "😢 Sad": [
        "What made you feel this way today?",
        "Is there something you're holding in?",
        "When was the last time you felt heard?"
    ],
    "😠 Angry": [
        "What's underneath your anger — hurt or fear?",
        "Is your anger trying to protect something?",
        "What would you say if you felt completely safe?"
    ],
    "😰 Anxious": [
        "What's one thing that *is* in your control right now?",
        "What would calm you right now, truly?",
        "Is this fear a fact, or a feeling?"
    ],
    "😊 Happy": [
        "What made today joyful?",
        "Who or what helped create this moment?",
        "How can you keep this momentum tomorrow?"
    ],
    "😐 Numb": [
        "If numbness could speak, what would it say?",
        "What do you *wish* you were feeling?",
        "What's one small thing you still care about?"
    ],
    "💭 Reflective": [
        "What insight are you carrying today?",
        "Is there a decision weighing on you?",
        "What’s something your past self would thank you for?"
    ]
}

positive_thoughts = [
    "You’ve survived 100% of your worst days.",
    "This too shall pass — always has, always will.",
    "You are not your emotions. You are the sky — emotions are just weather.",
    "Even in stillness, you are healing.",
    "Being kind to yourself is productive too."
]

actions = [
    "Take 10 slow breaths. Count each one.",
    "Write down one thing you’re grateful for.",
    "Stand up, stretch your body for 1 minute.",
    "Send a kind message to someone.",
    "Drink a glass of water, slowly, mindfully."
]

# ------------- OUTPUT -------------
st.markdown("### ✨ Your 5-Minute Reset")

selected_question = random.choice(questions[mood])
selected_thought = random.choice(positive_thoughts)
selected_action = random.choice(actions)

st.markdown(f"**🧠 Reflect:** {selected_question}")
st.markdown(f"**💡 Thought:** {selected_thought}")
st.markdown(f"**🎯 Action:** {selected_action}")

# ------------- SAVE SESSION -------------
if st.button("📓 Save this session"):
    entry = f"{datetime.now()} | Mood: {mood} | Q: {selected_question} | T: {selected_thought} | A: {selected_action}"
    hash_id = hashlib.sha1(entry.encode()).hexdigest()[:10]

    df = pd.DataFrame([[datetime.now(), mood, selected_question, selected_thought, selected_action, hash_id]],
                      columns=["Time", "Mood", "Question", "Thought", "Action", "ID"])

    try:
        old = pd.read_csv("mood_log.csv")
        df = pd.concat([old, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv("mood_log.csv", index=False)
    st.success(f"✅ Session saved with ID: `{hash_id}`")

# Optional: Show past sessions
with st.expander("📜 View Past Sessions"):
    try:
        log = pd.read_csv("mood_log.csv")
        st.dataframe(log.tail(5))
    except:
        st.info("No past sessions saved yet.")
