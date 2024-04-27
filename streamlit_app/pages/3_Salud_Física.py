import streamlit as st
import app_components as ac

# try:
#     _ = pagina

# except NameError:
#     pagina = 4

# if 'pagian' not in globals():
#     pagina = "Valor inicial"

nombre_archivo = '/Users/unaiigartua/Desktop/Clase/HACKATON_ALGORITMICOS/datos.txt'

def leer_pagina():
    try:
        with open(nombre_archivo, 'r') as archivo:
            pagina = int(archivo.read().strip()) # Usa strip para remover espacios y saltos de línea
    except FileNotFoundError:
        print(f"No se encontró el archivo {nombre_archivo}, se inicializará mi_variable a un valor predeterminado.")
        pagina = 0  # Define un valor por defecto si el archivo no existe
    return pagina

def escribir_pagina(pagina):
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(str(pagina))

pagina = leer_pagina()


st.set_page_config(
    page_title="Helthy AI - Inicio",
    page_icon="imgs/icon.png"#,
)

ac.render_sidebar()
# leer pagina desde .properties



# st.title("Salud Física")

# st.write(""" Prevención de Enfermedades: Promover hábitos de vida
# saludables para prevenir enfermedades y mantener un
# cuerpo sano.
# ▪ Cuidado de Lesiones y Dolencias: Consejos y
# recomendaciones para el cuidado de lesiones menores y
# dolencias físicas para una pronta recuperación.
# ▪ Descanso y Sueño: Educación sobre la importancia del
# descanso adecuado y patrones de sueño saludables para
# la recuperación física y el bienestar general.
# ▪ Enfermedades Crónicas:
# • Educación y Prevención: Información sobre hábitos
# de vida saludables para prevenir el desarrollo de
# enfermedades crónicas como la diabetes,
# enfermedades cardíacas y respiratorias.
# HPE CDS Tech Challenge 2023/2024. Fase III: El Hackathón
# 5
# • Gestión de Enfermedades: Orientación sobre cómo
# manejar y controlar enfermedades crónicas una vez
# diagnosticadas, incluyendo la adherencia al
# tratamiento y el manejo de síntomas.
# • Apoyo y Recursos: Proporcionar recursos y apoyo
# para aquellos que viven con enfermedades crónicas,
# incluyendo grupos de apoyo y acceso a servicios de
# atención médica especializada.""")

# # dos botones para cambiar la variable página
# if st.button('test'):
#     pagina = 1

# if st.button('test2'):
#     pagina = 2

# st.write(pagina)

if pagina == 1:
    st.write("CHATBOT")
    st.write(pagina)
    pagina = leer_pagina()

    if st.button('Volver'):
        escribir_pagina(0)

elif pagina == 2:
    st.write("AUDIO")
    st.write(pagina)
    pagina = leer_pagina()
    
    if st.button('Volver'):
        escribir_pagina(0)

else:
    st.title("Salud Física")
    st.write(""" 
    Prevención de Enfermedades: Promover hábitos de vida
    saludables para prevenir enfermedades y mantener un
    cuerpo sano.
    ▪ Cuidado de Lesiones y Dolencias: Consejos y
    recomendaciones para el cuidado de lesiones menores y
    dolencias físicas para una pronta recuperación.
    ▪ Descanso y Sueño: Educación sobre la importancia del
    descanso adecuado y patrones de sueño saludables para
    la recuperación física y el bienestar general.
    ▪ Enfermedades Crónicas:
    • Educación y Prevención: Información sobre hábitos
    de vida saludables para prevenir el desarrollo de
    enfermedades crónicas como la diabetes,
    enfermedades cardíacas y respiratorias.
    HPE CDS Tech Challenge 2023/2024. Fase III: El Hackathón
    5
    • Gestión de Enfermedades: Orientación sobre cómo
    manejar y controlar enfermedades crónicas una vez
    diagnosticadas, incluyendo la adherencia al
    tratamiento y el manejo de síntomas.
    • Apoyo y Recursos: Proporcionar recursos y apoyo
    para aquellos que viven con enfermedades crónicas,
    incluyendo grupos de apoyo y acceso a servicios de
    atención médica especializada.
    """)
    st.write(pagina)
    pagina = leer_pagina()
    
    if st.button('Chatbot'):
        escribir_pagina(1)

    if st.button('Audio'):
        escribir_pagina(2)