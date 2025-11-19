import streamlit as st
import json
from ollama_local import ask_ollama

st.title("Plant Control Philosophy Assistant")
st.write("Ask anything like: How is pump P-101 controlled?")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Load discovered knowledge
try:
    with open("rules_for_llm.json") as f:
        rules = json.load(f)
    knowledge = json.dumps(rules, indent=2)
except:
    knowledge = "No rules discovered yet."

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask about any pump, valve, or control loop..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    full_prompt = f"""
You are an expert plant control engineer.
Use ONLY the following discovered rules (never hallucinate):

{knowledge}

User question: {prompt}

Answer clearly and cite the exact rule when possible.
"""
    with st.chat_message("assistant"):
        response = ask_ollama(full_prompt)
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
