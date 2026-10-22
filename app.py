import streamlit as st
import cohere

# СЮДА ВСТАВЬ СВОЙ КЛЮЧ ИЗ COHERE (начинается на co_...)
API_KEY = "9QfBlbcEa8j4LkyTXhgjsnUY9CjNxUeaXeKPP9e9"

st.set_page_config(page_title="AI Burnout Helper", page_icon="💻", layout="centered")
st.title("💻 Настоящий ИИ-Ассистент против выгорания")
st.write("Поделись тем, что тебя бесит в коде или работе, и реальная нейросеть сгенерирует ответ.")

# Инициализируем клиента Cohere через официальный безопасный протокол
@st.cache_resource
def get_cohere_client(api_key):
    return cohere.ClientV2(api_key=api_key)

try:
    co = get_cohere_client(API_KEY)
except Exception as e:
    st.error(f"Ошибка инициализации ИИ: {e}")

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
            with st.spinner("Настоящий ИИ генерирует ответ..."):
                # Используем официальный защищенный метод чата Cohere V2
                response = co.chat(
                    model="command-r-plus", 
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ]
                )
                
                # Достаем текст ответа напрямую из защищенного объекта
                ai_response = response.message.content[0].text.strip()
                
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            message_placeholder.markdown(f"❌ Ошибка подключения к ИИ: {e}")
