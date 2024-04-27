import streamlit as st


def st_button(url, label, font_awesome_icon):
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">', unsafe_allow_html=True)

    button_code = f'''
    <a href="{url}" target="_blank" style="color: #31333F; text-align: left; text-decoration: none; display: inline-block; font-size: 20px; cursor: pointer;"><i class="fa {font_awesome_icon}"></i> {label}</a>
    '''
    return st.markdown(button_code, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.image("imgs/healthy_ai.png", use_column_width=True)
        st.markdown("### Integrantes")
        st.markdown("Jorge Alcorta")
        st.markdown("Sara Hernandez")
        st.markdown("Aitor Hernandez")
        st.markdown("Unai Igartua")
        st.markdown("Iñigo Fernandez-Sopeña")
        #st_button(url="https://github.com/Unaiigartua/Algoritmicos-CDS_Tech_Challenge", label="Github", font_awesome_icon="fa-github")
        

