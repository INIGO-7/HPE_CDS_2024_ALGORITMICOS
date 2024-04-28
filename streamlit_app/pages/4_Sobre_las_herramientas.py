import streamlit as st
import app_components as ac

conditions = [
    'Anaphylactic shock', 'Bleeding', 'Choking', 'Drowning',
    'Fracture', 'Poison', 'Stroke', 'Chicken pox',
    'Dengue', 'Malaria', 'Heart attack', 'Shock',
    'Burn', 'Dehydration', 'Asthma attacks',
    'Chronic kidney disease', 'Meningitis', 'Head injury'
]

st.set_page_config(
    page_title="Helthy AI - Sobre las herramientas",
    page_icon="imgs/icon.png"
)

ac.render_sidebar()

st.title("Sobre las Herramientas")

st.subheader("Modelo de Diagnóstico mediante Lenguaje Natural")
st.markdown("""
<div style="text-align: justify;">
    El modelo de diagnóstico mediante Lenguaje Natural es la parte más importante de nuestro proyecto y sobre la que se basan todas las herramientas. <br><br>
    Se trata de un modelo pre-entrenado de BERT (Bidirectional Encoder Representations from Transformers) para la clasificación de secuencias y adapta la última capa para clasificar enfermedades a partir de síntomas. BERT es una técnica basada en redes neuronales para el pre-entrenamiento del procesamiento del lenguaje natural desarrollada por Google. Capta el contexto bidireccional en una oración, lo que significa que puede entender el significado de una palabra en relación con las palabras que la rodean. Esto consigue perfeccionar la comprensión de las búsquedas de los usuarios. <br><br>
    Hemos entrenado este modelo con un dataset que empareja descripciones de síntomas expresadas en lenguaje natural con enfermedades. <br><br>
    Finalmente, se utiliza el modelo entrenado para hacer predicciones sobre nuevas descripciones de síntomas, devolviendo las enfermedades más probables junto con sus probabilidades.<br><br>
    Las enfermedades con las que se ha entrenado el modelo son:<br><br>
</div>
""", unsafe_allow_html=True)

cols = st.columns(3)
per_column = len(conditions) // len(cols) + (len(conditions) % len(cols) > 0)
for index, condition in enumerate(conditions):
    col_index = index // per_column
    cols[col_index].write(condition)

st.subheader("Herramienta de Diagnóstico mediante Lenguaje Natural")
st.markdown("""
<div style="text-align: justify;">
    Esta herramienta se encuentra en el apartado 'Diagnóstico con IA' y permite a los usuarios obtener una predicción de las enfermedades más probables para sus síntomas. <br><br>
    Para obtener la predicción, el usuario debe introducir una descripción de sus síntomas en el cuadro de texto y hacer clic en el botón 'Diagnóstico'. Con esta información, el modelo de diagnóstico mediante Lenguaje Natural realiza una predicción y muestra las dos enfermedades más probables junto con sus probabilidades. <br><br>
    Tambien una vez recivido el caso de diagnostico lo busca en los distintos tipos de mas probables de diagnostico segun diferentes organizaciones de salud reconocidas y te da una manera de afrontarlo. <br><br>
    Esta herramienta solo puede diagnosticar enfermedades con las que ha sido entrenada y no debe ser tomada como un diagnóstico definitivo. Si tienes dudas sobre tu salud, por favor, consulta a un médico. <br><br>
    Ejemplo de uso:<br><br>
</div>       
""", unsafe_allow_html=True)

st.code("""
Escribe tus síntomas aquí:
    I am sneezing all day and I have a fever and cough. I have a lot of snot.

Diagnóstico:
    Predicción 1: Common Cold con una confianza del 85.01%

    Predicción 2: Pneumonia con una confianza del 2.39%
""", language='css')

st.subheader("Chatbot para Diagnóstico Médico")
st.markdown("""
<div style="text-align: justify;">
    Esta herramienta se encuentra en el apartado 'Chatbot' y permite a los usuarios interactuar con un asistente virtual primero para obtener un diagnóstico y posteriormente información las enfermedades y primeros auxilios. <br><br>
    El chatbot utiliza dos modelos de lenguaje, uno para predecir un diagnóstico basado en los síntomas que proporcionas y otro para generar respuestas coherentes y útiles. <br><br>
    El diagnóstico se realiza de la misma manera que en la herramienta de diagnóstico mediante Lenguaje Natural, introduciendo una descripción de los síntomas en el chat y esperando la respuesta del asistente. <br><br>
    A partir del diagnóstico, el modelo que contestará será LLAMA 2, un modelo de lenguaje natural que genera respuestas coherentes y útiles sin necesidad de haberlo finetuneado. <br><br>

    Esta herramienta no debe ser tomada como un diagnóstico definitivo y si tienes dudas sobre tu salud, por favor, consulta a un médico. <br><br>
    Ejemplo de uso:<br><br>
</div>
""", unsafe_allow_html=True)

st.code("""
Model: 
    Cuéntame los síntomas que presentas.

User: 
    I am sneezing all day and I have a fever and cough. I have a lot of snot.
        
Model:
    Predicción 1: Common Cold (bastante probable)

    Predicción 2: Pneumonia (muy poco probable)
        
User:
    What can I do to relieve a cold?

Model:
    1. Stay hydrated by drinking plenty of fluids, such as water, tea, or soup.
    2. Use over-the-counter medications, such as pain relievers or decongestants,
        to help alleviate congestion and reduce fever.
    3. Rest and give your body time to recover.
    4. Use saline nasal sprays or drops to help loosen and clear out mucus.
    5. Try using a humidifier to add moisture to the air, which can help to 
        ease congestion and make breathing easier.
    6. Gargle with salt water to soothe a sore throat.
    7. Avoid close contact with others to prevent the spread of the infection.
    8. Try a warm compress on your face to help loosen mucus and reduce sinus 
        pressure.
    9. Use a neti pot or nasal irrigator to rinse out your nasal passages.
    10. Try taking over-the-counter antihistamines to help reduce the severity 
        of sneezing and congestion. It's important to note that colds are caused 
        by viruses, so antibiotics will not be effective in treating them. 
        Additionally, if your symptoms worsen or you experience difficulty 
        breathing, chest pain, or a fever over 102°F (39°C), seek medical 
        attention immediately.
""", language='css')

st.subheader("Herramientas Adicionales")

st.markdown("""
En nuestro proyecto también utilizamos algunas herramientas adicionales para manejar diferentes tipos de entradas y para la recomendación de primeros auxilios. Estas herramientas incluyen:

- **Imagen:** Utilizamos el repositorio TorchXRayVision para el análisis de radiografías.
- **Texto:** Para el procesamiento de texto utilizamos modelos de NLP.
- **Audio:** Implementamos WHISPER para el análisis de audio.

Además, hemos desarrollado un pipeline de recomendación de primeros auxilios que se encuentra disponible en nuestro repositorio de GitHub. Este pipeline consta de dos notebooks:

1. **text2disease.ipynb:** Contiene un modelo de BERT fine-tuned para la predicción de condiciones médicas.
2. **first_aid_chatbot.ipynb:** Este notebook utiliza un dataset complementario (Medical_Aid.json) que contiene condiciones médicas y respuestas sobre qué hacer en esas situaciones.

También, para abordar consultas urgentes o de emergencia gráficas, se ha implementado un sistema que permite a los usuarios subir imágenes de lesiones o heridas al chat, y recibir una respuesta inmediata sobre el tipo de lesión y cómo tratarla.

Se ha hecho uso de un conjunto de datos amplio que abarca varios tipos de lesiones, incluyendo abrasiones, hematomas, quemaduras, cortes, heridas diabéticas, laceraciones, heridas normales, úlceras por presión, heridas quirúrgicas y úlceras venosas. Cada tipo de lesión cuenta con un conjunto de ejemplos que oscila entre 100 y 600 imágenes. Estos datos se emplearon para entrenar un modelo de clasificación de imágenes basado en ResNet34, una arquitectura de red neuronal que se utiliza para aplicaciones de visión por computadora de aprendizaje profundo, como la detección de objetos y la segmentación de imágenes. En nuestro caso, para identificar con precisión el tipo de lesión presente en una imagen subida por el usuario.

Una vez que la imagen ha sido clasificada, el sistema utiliza la técnica RAG para generar un diagnóstico detallado y ofrecer recomendaciones específicas sobre cómo tratar la lesión identificada. Esto se logra, una vez más, codificando segmentos de texto relevantes.
""", unsafe_allow_html=True)


