import streamlit as st
import cohere

# БЕЗОПАСНО: Ключ автоматически берется из твоего сейфа в Secrets
API_KEY = st.secrets["MY_GROQ_SECRET"]

st.set_page_config(page_title="AI Burnout Helper", page_icon="💻", layout="centered")
st.title("💻 Настоящий ИИ-Ассистент против выгорания")
st.write("Поделись тем, что тебя бесит в коде или работе, и реальная нейросеть сгенерирует ответ.")

# Инициализируем защищенного клиента Cohere V2
@st.cache_resource
def get_cohere_client(api_key):
    return cohere.ClientV2(api_key=api_key)

try:
    co = get_cohere_client(API_KEY)
except Exception as e:
    st.error(f"Ошибка инициализации ИИ: {e}")

# БОКОВАЯ ПАНЕЛЬ
st.sidebar.title("⚙️ Панель управления")
st.sidebar.markdown("**О проекте:** Ультрабыстрый ИИ-психолог со стримингом ответов в реальном времени.")

# Безопасное сессионное хранение истории (никогда не зависает при старте)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Кнопка очистки истории
if st.sidebar.button("🔄 Очистить историю чата"):
    st.session_state.messages = []
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

    with st.chat_message("assistant"):
        # Функция-генератор для живого стриминга текста
        def response_generator():
            system_prompt = (
                "Ты — профессиональный психолог для программистов. "
                "ОБЯЗАТЕЛЬНО обращайся к пользователю на 'ты' и используй слово 'бро' (или 'сестра', если пишет девушка). "
                "Отвечай строго на русском языке. Твой тон должен быть дружелюбным, поддерживающим, "
                "но с примесью тонкой айтишной иронии и легкого юмора над типичными проблемами разработчиков. "
                "Выслушай проблему, прояви эмпатию и дай 3 практических шага для снижения стресса."
            )
            
            stream = co.chat_stream(
                model="command-a-03-2025", 
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            
            for chunk in stream:
                if chunk.type == "content-delta":
                    yield chunk.delta.message.content.text

        try:
            # Магия живой печати букв
            ai_response = st.write_stream(response_generator())
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.markdown(f"❌ Ошибка подключения к ИИ: {e}")
