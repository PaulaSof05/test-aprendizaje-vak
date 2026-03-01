import streamlit as st
import pandas as pd

# Configuración estética de la página
st.set_page_config(page_title="Test de Aprendizaje VAK", page_icon="🎓")

from streamlit_gsheets import GSheetsConnection

# Creamos la conexión con tu Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🎓 Diagnóstico de Estilo de Aprendizaje")
st.write("Hola. Responde estas preguntas para personalizar tu experiencia educativa.")

# Formulario interactivo
with st.form("test_form"):
    nombre = st.text_input("Escribe tu nombre completo:")
    
    p1 = st.radio(
        "1. Cuando tienes que aprender algo nuevo, prefieres:",
        ["Leer instrucciones o ver diagramas", 
         "Que alguien te lo explique verbalmente", 
         "Empezar a hacerlo y ver qué pasa"]
    )
    
    p2 = st.radio(
        "2. En tu tiempo libre, prefieres:",
        ["Ver una película o leer", 
         "Escuchar música o un podcast", 
         "Hacer deporte o alguna manualidad"]
    )

    # Botón de envío
    enviado = st.form_submit_button("Obtener mi resultado")

if enviado:
    # 1. Cálculos de estilo
    respuestas = [p1, p2]
    visual = sum(1 for r in respuestas if "Leer" in r or "Ver" in r)
    auditivo = sum(1 for r in respuestas if "explique" in r or "Escuchar" in r)
    kinestesico = sum(1 for r in respuestas if "hacerlo" in r or "deporte" in r)

    if visual >= auditivo and visual >= kinestesico: resultado = "VISUAL"
    elif auditivo >= visual and auditivo >= kinestesico: resultado = "AUDITIVO"
    else: resultado = "KINESTÉSICO"

    # 2. Mostrar resultado y gráfica (una sola vez)
    st.success(f"¡Listo {nombre}! Tu estilo predominante es: **{resultado}**")
    
    st.subheader("📊 Tu Perfil de Aprendizaje")
    df_grafica = pd.DataFrame({
        'Estilo': ['Visual', 'Auditivo', 'Kinestésico'],
        'Puntos': [visual, auditivo, kinestesico]
    })
    st.bar_chart(df_grafica.set_index('Estilo'))

    # 3. Guardado en Google Sheets
    df_nuevo = pd.DataFrame([{
        "Nombre": nombre,
        "Visual": visual,
        "Auditivo": auditivo,
        "Kinestesico": kinestesico,
        "Resultado": resultado
    }])

    # Intentamos guardar
    try:
        conn.create(data=df_nuevo) # Ya no necesitas la URL aquí si la pusiste en Secrets
        st.balloons()
        st.success(f"¡Perfecto {nombre}! Tus respuestas se guardaron en la base de datos.")
    except Exception as e:
        st.error("Hubo un tema con los permisos de Google. Revisa los Secrets.")
