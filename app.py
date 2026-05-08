import streamlit as st
from dotenv import load_dotenv
import os
from src.insights.analyzer import generate_executive_report

#Modulos locales
from src.utils.data_loader import load_rappi_data
from src.bot.agent import get_rappi_agent

#Variables de entorno
load_dotenv()

#Logo
base_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, "assets", "logo_rappi.png")

#Configuración de la pagina
if os.path.exists(logo_path):
    st.set_page_config(page_title="Rappi Ops - AI Explorer", page_icon=logo_path, layout="wide")
else:
    st.set_page_config(page_title="Rappi Ops - AI Explorer", page_icon="🍔", layout="wide")

#Logo y titulo
col1, col2 = st.columns([1, 14])
with col1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=80)
    else:
        st.write("🍔")
with col2:
    st.title("Sistema de Análisis Inteligente")

st.markdown("---")

#---------------------------------------------------------
#CARGA DE DATOS Y AGENTE
#---------------------------------------------------------

with st.spinner("Cargando base de datos y conectando modelos..."):
    dataframes = load_rappi_data()
    agent = None
    df_metricas = None
    df_orders = None
    
    if dataframes:
        for nombre_hoja, df in dataframes.items():
            df.columns = df.columns.str.strip()
            
            if 'L0W_ROLL' in df.columns:
                df_metricas = df
            elif 'L0W' in df.columns and 'L0W_ROLL' not in df.columns:
                df_orders = df
        
        if df_metricas is not None:
            lista_dfs = [df_metricas]
            if df_orders is not None:
                lista_dfs.append(df_orders)
                
            agent = get_rappi_agent(lista_dfs)
        else:
            st.error("No se encontro la columna 'L0W_ROLL' indicando la tabla de métricas.")
    else:
        st.error("No se pudieron cargar los datos.")

#---------------------------------------------------------
#INTERFAZ DE USUARIO
#---------------------------------------------------------

tab_chat, tab_insights = st.tabs(["Bot Conversacional", "Insights Automaticos"])

with tab_chat:
    st.header("Consulta de Metricas")
    with st.expander("Casos de Uso"):
        st.markdown("""
        Puedes copiar y pegar cualquiera de estas consultas para evaluar el sistema:
        
        * **Filtrado:** *"¿Cuáles son las 5 zonas con mayor Lead Penetration esta semana?"*
        * **Comparaciones:** *"Compara el Perfect Order entre zonas Wealthy y Non Wealthy en México"*
        * **Tendencias temporales:** *"Muestra la evolución de Gross Profit UE en Chapinero últimas 8 semanas"*
        * **Agregaciones:** *"¿Cuál es el promedio de Lead Penetration por país?"*
        * **Analisis multivariable:** *"¿Qué zonas tienen alto Lead Penetration pero bajo Perfect Order?"*
        * **Inferencia:** *"¿Cuáles son las zonas que más crecen en la métrica Orders y qué podría explicarlo?"*
        """)
    
    #Inicializar la memoria del chat en la sesion
    if "messages" not in st.session_state:
        st.session_state.messages = []

    #Renderizar el historial de mensajes en pantalla
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    #Input del usuario
    if prompt := st.chat_input("Escribe tu pregunta analitica aqui..."):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if agent:
            with st.chat_message("assistant"):
                with st.spinner("Analizando tabla de datos..."):
                    try:
                        response = agent.invoke(prompt)
                        respuesta_texto = response["output"]
                        
                        st.markdown(respuesta_texto)
                        st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
                    except Exception as e:
                            st.error(f"Hubo un error de razonamiento: {e}")

with tab_insights:
    st.header("Reporte Ejecutivo de Operaciones")
    st.info("Generacion automatica de insights: Detección de anomalias y tendencias de la semana L0W vs L1W.")

    if st.button("Generar Reporte Automatico"):
        if agent is not None:
            with st.spinner("Calculando variaciones matematicas y redactando reporte con Gemini..."):
                try:
                    # Llamamos a nuestra función generadora
                    reporte_markdown = generate_executive_report(df_metricas)

                    # Mostramos el resultado con estilo
                    st.success("Reporte generado exitosamente.")
                    st.markdown(reporte_markdown)

                    st.download_button(
                        label="Descargar Reporte (Markdown)",
                        data=reporte_markdown,
                        file_name="Reporte_Insights_Rappi.md",
                        mime="text/markdown"
                    )
                except Exception as e:
                    st.error(f"Error al generar el reporte: {e}")
        else:
            st.warning("Carga los datos primero para poder generar el reporte.")