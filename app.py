import streamlit as st
import cohere
import json
from streamlit_local_storage import LocalStorage

# БЕЗОПАСНО: Ключ автоматически берется из твоего сейфа в Secrets
API_KEY = st.secrets["MY_GROQ_SECRET"]

st.set_page_config(page_title="AI Burnout Helper", page_icon="💻", layout="centered")
st.title("💻 Настоящий ИИ-Ассистент против выгорания")
st.write("Поделись тем, что тебя бесит в коде или работе, и реальная нейросеть сгенерирует ответ.")

# Инициализируем инструмент для работы с памятью браузера
local_storage = LocalStorage()

@st.cache_resource
def get_cohere_client(api_key):
    return cohere.ClientV2(api_key=api_key)

try:
    co = get_cohere_client(API_KEY)
except Exception as e:
    st.error(f"Ошибка инициализации ИИ: {e}")

# БОКОВАЯ ПАНЕЛЬ
st.sidebar.title("⚙️ Панель управления")
st.sidebar.markdown("**О проекте:** Система анализа стресса с постоянным локальным хранением истории чата в браузере.")

# УМНОЕ ВОССТАНОВЛЕНИЕ ИСТОРИИ ИЗ ПАМЯТИ БРАУЗЕРА
if "messages" not in st.session_state:
    try:
        saved_chat = local_storage.getItem("saved_history")
        if saved_chat and saved_chat != "null":
            st.session_state.messages = json.loads(saved_chat)
        else:
            st.session_state.messages = []
    except:
        st.session_state.messages = []

# Кнопка очистки истории
if st.sidebar.button("🔄 Очистить историю чата"):
    st.session_state.messages = []
    local_storage.setItem("saved_history", json.dumps([]))
    st.rerun()

# Отображаем сообщения из истории
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле ввода для пользователя
if user_input := st.chat_input("Напиши, что случилось..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    local_storage.setItem("saved_history", json.dumps(st.session_state.messages))

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        system_prompt = (
            "Ты — профессиональный психолог для программистов. "
            "Отвечай строго на русском языке, дружелюбно, с легким айтишным юмором. "
            "Выслушай проблему, прояви эмпатию и дай 3 практических шага для снижения стресса."
        )
        
        try:
            with st.spinner("Настоящий ИИ генерирует ответ..."):
                response = co.chat(
                    model="command-a-03-2025", 
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ]
                )
                
                # ИСПРАВЛЕНО: Безопасное чтение контента, даже если это список (List)
                content = response.message.content
                if isinstance(content, list):
                    ai_response = content[0].text.strip()
                else:
                    ai_response = content.text.strip()
                
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            local_storage.setItem("saved_history", json.dumps(st.session_state.messages))
            
        except Exception as e:
            message_placeholder.markdown(f"❌ Ошибка подключения к ИИ: {e}")
