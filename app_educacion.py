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
    # 1. Cálculos de estilo (Esto ya lo tienes)
    respuestas = [p1, p2]
    visual = sum(1 for r in respuestas if "Leer" in r or "Ver" in r)
    auditivo = sum(1 for r in respuestas if "explique" in r or "Escuchar" in r)
    kinestesico = sum(1 for r in respuestas if "hacerlo" in r or "deporte" in r)

    if visual >= auditivo and visual >= kinestesico: resultado = "VISUAL"
    elif auditivo >= visual and auditivo >= kinestesico: resultado = "AUDITIVO"
    else: resultado = "KINESTÉSICO"

    # 2. Mostrar resultado y gráfica
    st.success(f"¡Listo {nombre}! Tu estilo predominante es: **{resultado}**")
    
    df_grafica = pd.DataFrame({
        'Estilo': ['Visual', 'Auditivo', 'Kinestésico'],
        'Puntos': [visual, auditivo, kinestesico]
    })
    st.bar_chart(df_grafica.set_index('Estilo'))

    # 3. GUARDADO ACUMULATIVO (La parte nueva)
    # 3. GUARDADO ACUMULATIVO (Corregido y Mejorado)
    try:
        # A. Leemos lo que YA está en el Excel
        # Usamos .read() pero forzamos a que no traiga basura
        df_previo = conn.read().dropna(how="all")
        
        # B. Creamos la fila del usuario actual 
        # IMPORTANTE: Los nombres aquí deben ser IDÉNTICOS a los de tu Excel
        df_nuevo = pd.DataFrame([{
            "Nombre": nombre,
            "Visual": visual,
            "Auditivo": auditivo,
            "Kinestesico": kinestesico, # Sin acento, igual que tu imagen b08558
            "Resultado": resultado
        }])

        # C. Juntamos lo viejo con lo nuevo
        # ignore_index=True es lo que evita que se encimen los datos
        df_final = pd.concat([df_previo, df_nuevo], ignore_index=True)

        # D. Subimos la lista completa
        conn.update(data=df_final)
        
        st.balloons()
        st.success(f"¡Resumen guardado! Eres el registro #{len(df_final)}.")

    except Exception as e:
        # Este mensaje nos dirá exactamente qué falla si algo sale mal
        st.error(f"Error técnico: {e}")
