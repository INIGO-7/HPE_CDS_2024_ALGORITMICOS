import streamlit as st
import app_components as ac


st.set_page_config(
    page_title="Helthy AI - Inicio",
    page_icon="imgs/icon.png"#,
)

ac.render_sidebar()

algoritmicos = r"""
‎    __    __    ___  _____  ____  ____  ____  __  __  ____  ___  _____  ___ 
   /__\  (  )  / __)(  _  )(  _ \(_  _)(_  _)(  \/  )(_  _)/ __)(  _  )/ __)
  /(__)\  )(__( (_-. )(_)(  )   / _)(_   )(   )    (  _)(_( (__  )(_)( \__ \
 (__)(__)(____)\___/(_____)(_)\_)(____) (__) (_/\/\_)(____)\___)(_____)(___/
"""
st.text(algoritmicos)

st.title("¡Bienvenidos a HealthyAI!")
st.subheader("Sobre nosotros")

st.write("""
<div style="text-align: justify;">
    Somos un equipo de estudiantes de la Universidad de Deusto compuesto por Sara Hernández, Aitor Hernández, Unai Igartua, Jorge Alcorta e Iñigo Fernández-Sopeña. Nos enorgullece presentar nuestro proyecto HealthyAI, diseñado con el objetivo de ofrecer asesoramiento y orientación sanitaria en una variedad de situaciones, desde heridas menores hasta emergencias médicas graves.<br><br>
</div>
    """, unsafe_allow_html=True)

st.subheader("Nuestro objetivo")
st.write("""
<div style="text-align: justify;">
    El objetivo de esta herramienta es ofrecer orientación sobre primeros auxilios y assoramiento general de manera clara y comprensible para conocer la posible condición que se padezca en cualquier momento, para cualquier usuario, sin importar su nivel de conocimientos médicos. Nos basamos en las capacidades que nos ofrece la Inteligencia Artificial para lograr este objetivo.<br><br>
</div>
    """, unsafe_allow_html=True)

st.subheader("Nota importante")
st.write("""
<div style="text-align: justify;">
    Es fundamental enfatizar que nuestro sistema se concibe como una herramienta complementaria y no sustitutiva de la atención médica profesional. Reconocemos la importancia de buscar ayuda médica calificada en casos de emergencias graves o dudas sobre el estado de salud de una persona.
</div>
    """, unsafe_allow_html=True)