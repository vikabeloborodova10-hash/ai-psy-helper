import streamlit as st
import requests
import json


API_KEY = "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" 

st.set_page_config(page_title="AI Burnout Helper", page_icon="💻", layout="centered")
st.title("💻 ИИ-Ассистент против выгорания программистов")
st.write("Поделись тем, что тебя бесит в коде или работе, а ИИ-психолог разберет твою проблему.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Напиши, что случилось..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        system_prompt = "Ты — professional psychologist for software developers. Respond in Russian, be empathetic, friendly, and give 3 practical steps to reduce stress."
        
        try:
            response = requests.post(
                url="https://openrouter.ai",
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                data=json.dumps({
                    "model": "meta-llama/llama-3-8b-instruct:free",
                    "messages": [{"role": "system", "content": system_prompt}, *st.session_state.messages]
                })
            )
            result = response.json()
            ai_response = result['choices']['message']['content']
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            message_placeholder.markdown("❌ Ошибка подключения к ИИ.")
