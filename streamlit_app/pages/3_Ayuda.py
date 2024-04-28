import sys
import os

sys.path.insert(0, os.path.abspath('../src'))
from full_recommendation import *


import streamlit as st
import app_components as ac
import requests
import streamlit_extras
from streamlit_extras.bottom_container import bottom 
from streamlit_mic_recorder import mic_recorder, speech_to_text
import pandas as pd
from io import StringIO
from PIL import Image
import requests
from fastai.learner import load_learner

from transformers import AutoTokenizer
from transformers import TFAutoModelForSequenceClassification
from transformers import TextClassificationPipeline


state = st.session_state

write_message_chat = False
write_message_audio = False
write_message_image = False




urlMixtra = "http://10.10.6.67:8080/api/converse"
urlEndpoint = "http://10.10.6.67:8080/api/questions"
urlImage = "http://10.10.6.67:8080/api/image"

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
    st.session_state.messages = [{"role": "assistant", "content": "Cuéntame los síntomas que presentas o mándame una imagen."}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
st.sidebar.markdown("---")



ac.render_sidebar()


st.info(more_info)

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Cuéntame los síntomas que presentas o mándame una imagen."}]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])



with bottom():
    if len(st.session_state.messages) <= 1:
        with st.container():
            left, right = st.columns([0.8, 0.2])
            with left:

                uploaded_file = st.file_uploader("Elige una imagen...", type=['jpg', 'jpeg', 'png'])
                if uploaded_file is not None:
                    # Mostrar la imagen cargada
                    st.image(uploaded_file, caption='Imagen cargada.', use_column_width=True)

                    # Enviar la imagen al servidor Flask
                    if st.button('Enviar imagen'):
                        files = {'image': uploaded_file.getvalue()}
                        image_response_raw = requests.post(urlImage, files=files)
                        image_response = image_response_raw.json()["response"]
                        # Mostrar respuesta del servidor
                        #st.text(image_response.text)
                        write_message_image = True
                        message = {"role": "assistant", "content": (image_response)}
                        st.session_state.messages.append(message)


    with st.container():
        left, right = st.columns([0.8, 0.2])
        with left:
            if prompt := st.chat_input():
                write_message_chat = True
                print (type(prompt))
                mandar=prompt
                ocultar = True
                st.session_state.messages.append({"role": "user", "content": prompt})     
                
        with right:
            if text := speech_to_text(language='es-ES', use_container_width=True, just_once=True, key='STT'):
                write_message_audio = True
                print(type(text))
                mandar=text
                ocultar = True
                st.session_state.messages.append({"role": "user", "content": text})
                
                
              
if write_message_chat:
    with st.chat_message("user"):
        st.write(prompt)  


if write_message_audio:
    with st.chat_message("user"):
        st.write(text)   

if write_message_image:
    with st.chat_message("assistant"):
        st.write(image_response)
    
write_message_image = False
write_message_chat = False
write_message_audio = False

RES_PATH = "../res"
DATASETS_PATH = os.path.join(RES_PATH, "datasets")
MODELS_PATH = os.path.join(RES_PATH, "models")
first_aid_path = os.path.join(DATASETS_PATH, "Medical_Aid_v2.json")
model_path = os.path.join(MODELS_PATH, "bert_finetuned")
classifier = ConditionClassifierBERT(24, first_aid_path)




if st.session_state.messages[-1]["role"] != "assistant":
    if len(st.session_state.messages) <= 2:
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                condition, advice = classifier.get_first_aid(model_path, prompt)
                response = f"La condición detectada es: {condition}. Aquí tienes algunos consejos: {advice}"
                placeholder = st.empty()

                placeholder.markdown(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
    st.warning(disclaimer)



