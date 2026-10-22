import streamlit as st
import requests
import json

# СЮДА ВСТАВЬ СВОЙ НОВЫЙ КЛЮЧ ИЗ GROQ (начинается на gsk_...)
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
        system_prompt = (
            "Ты — профессиональный психолог для программистов. "
            "Отвечай строго на русском языке, дружелюбно, с легким айтишным юмором. "
            "Выслушай проблему, прояви эмпатию и дай 3 практических шага для снижения стресса."
        )
        
        try:
            # Делаем прямой запрос к ультрабыстрому серверу Groq
            response = requests.post(
                url="https://groq.com",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": "llama3-8b-8192", # Используем стабильную и быструю модель Llama 3
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *st.session_state.messages
                    ]
                })
            )
            result = response.json()
            
            if 'error' in result:
                message_placeholder.markdown(f"❌ Ошибка ИИ: {result['error']['message']}")
            else:
                ai_response = result['choices']['message']['content']
                message_placeholder.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            message_placeholder.markdown(f"❌ Ошибка подключения: {e}")
