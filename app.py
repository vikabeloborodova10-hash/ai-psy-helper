import streamlit as st
import requests
import json

# СЮДА ВСТАВЬ СВОЙ КЛЮЧ ИЗ COHERE (начинается на co_...)
API_KEY = "9QfBlbcEa8j4LkyTXhgjsnUY9CjNxUeaXeKPP9e9"

st.set_page_config(page_title="AI Burnout Helper", page_icon="💻", layout="centered")
st.title("💻 Настоящий ИИ-Ассистент против выгорания")
st.write("Поделись тем, что тебя бесит, и реальная нейросеть сгенерирует уникальный ответ.")

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
        
        # Системная инструкция для ИИ
        system_prompt = (
            "Ты — профессиональный психолог для программистов. "
            "Отвечай строго на русском языке, дружелюбно, с легким айтишным юмором. "
            "Выслушай проблему, прояви эмпатию и дай 3 практических шага для снижения стресса."
        )
        
        try:
            with st.spinner("Настоящий ИИ генерирует ответ..."):
                # Запрос к официальному и открытому API Cohere
                response = requests.post(
                    url="https://cohere.com",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json"
                    },
                    data=json.dumps({
                        "model": "command-r-plus", # Отличная умная модель
                        "message": user_input,
                        "preamble": system_prompt # Инструкция поведения ИИ
                    }),
                    timeout=25
                )
                
                result = response.json()
                
                if 'text' in result:
                    ai_response = result['text'].strip()
                    message_placeholder.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    message_placeholder.markdown(f"⚠️ Ошибка сервера ИИ: {result}")
                    
        except Exception as e:
            message_placeholder.markdown(f"❌ Ошибка подключения: {e}")
