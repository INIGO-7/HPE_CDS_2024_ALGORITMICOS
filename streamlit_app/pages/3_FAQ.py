import streamlit as st 
import app_components as ac

conditions = [
    'Anaphylactic shock', 'Bleeding', 'Choking', 'Drowning',
    'Fracture', 'Poison', 'Stroke', 'Chicken pox',
    'Dengue', 'Malaria', 'Heart attack', 'Shock',
    'Burn', 'Dehydration', 'Asthma attacks',
    'Chronic kidney disease', 'Meningitis', 'Head injury'
]

num_columns = 3
per_column = len(conditions) // num_columns + (len(conditions) % num_columns > 0)




st.set_page_config(
    page_title="Helthy AI - FAQ",
    page_icon="imgs/icon.png"
)


st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)
ac.render_sidebar()


st.title("FAQ")

st.markdown("#### Diagnóstico mediante Lenguaje Natural")

with st.expander("¿Es privado el diagnóstico que recibo?", expanded=False):
    st.markdown("Sí, la tanto los sintomas que introduces como el diagnóstico recibido es privado. Al utilizar un modelo local, no se envía información a servidores externos. Además, no se almacena información de las conversaciones o identificadores de usuario.")


with st.expander("¿Cómo funciona el diagnosticador?", expanded=False):
    st.markdown("El diagnosticador utiliza un modelo de lenguaje natural entrenado con diagnósticos recibidos para algunas enfermedades, además de diferentes fuentes reconocidas de salud y bienestar.\n\n Para más información sobre el funcionamiento del modelo, visita el apartado 'Sobre las Herramientas' en el menú lateral.")

with st.expander("¿Que enfermedades puede predecir?", expanded=False):
    cols = st.columns(num_columns)
    # Distribute the conditions across the columns
    for index, condition in enumerate(conditions):
        col_index = index // per_column
        cols[col_index].write(condition)

with st.expander("¿Qué debo hacer si tengo dudas sobre mi salud?", expanded=False):
    st.markdown("Si tienes dudas sobre tu salud, por favor, consulta a un médico. La información proporcionada por el chatbot no debe ser tomada como un diagnóstico definitivo.")

with st.expander("¿Cómo de precisa es esta herramienta?", expanded=False):
    st.markdown("El chatbot es una herramienta de ayuda y no reemplaza la opinión de un profesional de la salud. La precisión del modelo depende de la calidad de los datos con los que fue entrenado y no debe ser tomado como un diagnóstico definitivo.\n\n Para más información sobre la precisión obtenida con el modelo, visita el apartado 'Sobre las Herramientas' en el menú lateral.")


st.markdown("#### Chatbot para Diagnóstico Médico enfocado a ayudas urgentes y consultas de interes en salud ")

with st.expander("¿Cómo funciona el chatbot?", expanded=False):
    st.markdown("El chatbot utiliza dos modelos de lenguaje, uno para predecir un diagnóstico basado en los síntomas que proporcionas y otro para generar respuestas coherentes y útiles.\n\n Para más información sobre el funcionamiento de los modelos, visita el apartado 'Sobre las Herramientas' en el menú lateral.")

with st.expander("¿Cómo de precisa es esta herramienta?", expanded=False):
    st.markdown("El chatbot es una herramienta de ayuda y no reemplaza la opinión de un profesional de la salud. La precisión del chatbot depende de la calidad de los datos con los que fue entrenado y no debe ser tomado como un diagnóstico definitivo.\n\n Para más información sobre la precisión obtenida con los modelos, visita el apartado 'Sobre las Herramientas' en el menú lateral.")

with st.expander("¿Qué debo hacer en caso de una emergencia médica?", expanded=False):
    st.markdown("En caso de una emergencia médica, como un paro cardíaco o un accidente grave, llama inmediatamente al número de emergencia local y sigue las instrucciones del operador. \n\n Si es posible, proporciona información relevante sobre la situación y sigue los primeros auxilios básicos hasta que llegue la ayuda médica.")

with st.expander("¿Qué debo hacer si tengo dudas sobre mi salud?", expanded=False):
    st.markdown("Si tienes dudas sobre tu salud, por favor, consulta a un médico. La información proporcionada por el chatbot no debe ser tomada como un diagnóstico definitivo.")

with st.expander("¿Qué recursos están disponibles para ayudar con problemas de salud mental?", expanded=False):
    st.markdown("Hay varios recursos disponibles, como líneas de ayuda telefónica, terapia en línea, grupos de apoyo comunitarios y aplicaciones móviles de salud mental.  \n\n También es importante hablar con un profesional de la salud mental para obtener orientación personalizada y tratamiento adecuado.")

with st.expander("¿Qué hago si el chatbot me ha dado un tratamiento?", expanded=False):
    st.markdown("El chatbot no proporciona tratamientos médicos. Si el chatbot ha proporcionado información sobre un tratamiento, por favor, consulta a un médico para obtener un diagnóstico y tratamiento adecuado.")


with st.expander("¿Que enfermedades puede predecir?", expanded=False):
    cols = st.columns(num_columns)
    # Distribute the conditions across the columns
    for index, condition in enumerate(conditions):
        col_index = index // per_column
        cols[col_index].write(condition)