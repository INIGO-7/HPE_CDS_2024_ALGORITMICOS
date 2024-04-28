import streamlit as st
import app_components as ac
import requests


urlMixtra = "http://10.10.6.10:8083/generate"
urlEndpoint = "http://10.10.6.67:8080/api/questions"

def generate_HPT_response(prompt_input):
    string_dialogue = """Tú eres Assistant, un asistente médico para hispanohablantes siempre darás respuestas veraces, y completas en Español. \n\n"""
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    print(f"{string_dialogue} Assistant: ")
    data = {
        "inputs": f"{string_dialogue}  Assistant: "
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(urlMixtra, json=data, headers=headers)
    return response


def generate_endpoint_response(url, prompt_input):

    data = {
        "questions": [
            {"id": 1, "question": prompt_input}
        ]
    }

    response_raw = requests.post(url, json=data)

    # response_text = response_raw["questions"][0]["answer"]
    return response_raw





disclaimer = "⚠ Recordamos que esta herramienta no reemplaza la opinión de un profesional de la salud. Si tienes dudas sobre tu salud, por favor, consulta a un médico. No siga ningún tratamiento proporcionado por el chatbot sin consultar a un profesional."
more_info = "Para más información sobre el funcionamiento sobre esta herramienta, visita el apartado 'FAQ' en el menú lateral."


st.set_page_config(
    page_title="Helthy AI - Chatbot",
    page_icon="imgs/icon.png"
)


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Cuéntame los síntomas que presentas."}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
st.sidebar.markdown("---")



ac.render_sidebar()


st.info(more_info)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Cuéntame los síntomas que presentas."}]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = generate_endpoint_response(urlEndpoint, prompt)
            placeholder = st.empty()
            # if response.status_code == 200:
            #     response_json = response.json()
            #     generated_text = response_json.get('generated_text', 'No generated text found')
            # else:
            #     generated_text = "Error en la solicitud: " + str(response.status_code)
            response = response.json()["questions"][0]["answer"]
            placeholder.markdown(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
    st.warning(disclaimer)


