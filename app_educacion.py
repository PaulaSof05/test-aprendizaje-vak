import streamlit as st
import pandas as pd

from streamlit_gsheets import GSheetsConnection

# Creamos la conexión con tu Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# --- Dentro del bloque 'if enviado:' reemplaza el guardado de CSV por esto: ---
df_nuevo = pd.DataFrame([{
    "Nombre": nombre_alumno,
    "Visual": visual,
    "Auditivo": auditivo,
    "Kinestesico": kinestesico,
    "Resultado": estilo_final,
    "Fecha": pd.Timestamp.now()
}])

# Enviamos los datos a Google Sheets
conn.create(data=df_nuevo, spreadsheet="https://docs.google.com/spreadsheets/d/1DkEoFRnOfNceo_73qMplVraMeHDU_LYZqAulDUxM6c8/edit?gid=0#gid=0")
st.success("¡Datos guardados en la base de datos central!")

# Configuración estética de la página
st.set_page_config(page_title="Test de Aprendizaje VAK", page_icon="🎓")

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
    # Lógica de cálculo simplificada
    respuestas = [p1, p2]
    visual = sum(1 for r in respuestas if "Leer" in r or "Ver" in r)
    auditivo = sum(1 for r in respuestas if "explique" in r or "Escuchar" in r)
    kinestesico = sum(1 for r in respuestas if "hacerlo" in r or "deporte" in r)

    resultado = ""
    if visual >= auditivo and visual >= kinestesico: resultado = "VISUAL"
    elif auditivo >= visual and auditivo >= kinestesico: resultado = "AUDITIVO"
    else: resultado = "KINESTÉSICO"

    # Mostrar resultado con estilo
    st.success(f"¡Listo {nombre}! Tu estilo predominante es: **{resultado}**")
    
    # Aquí es donde la magia de Data Science ocurre: Guardamos en un DataFrame
    datos = {"Nombre": [nombre], "Resultado": [resultado]}
    df = pd.DataFrame(datos)
    st.write("Vista previa de tus datos guardados:", df)
    # Creamos una gráfica de barras con los resultados
    st.subheader("📊 Tu Perfil de Aprendizaje")
    datos_grafica = pd.DataFrame({
        'Estilo': ['Visual', 'Auditivo', 'Kinestésico'],
        'Puntos': [visual, auditivo, kinestesico]
    })
    st.bar_chart(data=datos_grafica, x='Estilo', y='Puntos', color="#0077b6")
    # Creamos un DataFrame para la gráfica
    df_grafica = pd.DataFrame({
        'Estilo': ['Visual', 'Auditivo', 'Kinestésico'],
        'Puntos': [visual, auditivo, kinestesico]
    })

    # Mostramos la gráfica de barras
    st.divider() # Una línea para separar
    st.subheader("📊 Tu Perfil de Aprendizaje")
    st.bar_chart(df_grafica.set_index('Estilo'))
    

    st.info("💡 Tip: Si eres Visual, usa mapas mentales. Si eres Auditivo, graba tus clases. Si eres Kinestésico, ¡sigue programando!")


