import streamlit as st
import requests
import json

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
        
        # Строим четкую инструкцию для ИИ на русском языке
        prompt = (
            f"Инструкция: Ты профессиональный психолог для программистов. "
            f"Ответь на русском языке дружелюбно, прояви эмпатию и дай 3 практических шага. "
            f"Проблема разработчика: {user_input}\nОтвет психолога:"
        )
        
        try:
            with st.spinner("ИИ генерирует ответ..."):
                # Используем бесплатный открытый сервер Hugging Face API без ключей
                API_URL = "https://huggingface.co"
                
                response = requests.post(
                    API_URL,
                    json={
                        "inputs": prompt,
                        "parameters": {
                            "max_new_tokens": 300,
                            "temperature": 0.7,
                            "return_full_text": False
                        }
                    },
                    timeout=20
                )
                
                result = response.json()
                
                # Достаем сгенерированный текст из ответа Hugging Face
                if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
                    ai_response = result[0]['generated_text'].strip()
                elif isinstance(result, dict) and 'error' in result:
                    ai_response = f"⚠️ Модель временно загружается, подожди 10 секунд и отправь снова. (Ошибка: {result['error']})"
                else:
                    ai_response = "🤖 ИИ задумался, попробуй перефразировать мысль."
                
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            message_placeholder.markdown(f"❌ Ошибка сети: {e}")
