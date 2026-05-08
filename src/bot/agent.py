from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import os
import streamlit as st

@st.cache_resource
def get_rappi_agent(dfs): # <--- NOTA: ahora recibe 'dfs' (puede ser una lista)
    """
    Inicializa el modelo Gemini y crea un agente capaz de interactuar con uno o varios DataFrames.
    """
    
    #Gemini como LLM (Recomiendo usar 'gemini-2.5-flash' en este caso estara le version lite por un tema de tokens
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite", 
        temperature=0, 
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    #Prompt actualizado para manejar múltiples tablas
    custom_prefix = """
    Eres un Analista de Datos Senior (Strategy & Ops) de Rappi. 
    Tu objetivo es responder preguntas complejas sobre métricas operacionales.
    
    TIPS IMPORTANTES SOBRE TUS DATOS:
    - Tienes acceso a múltiples DataFrames. 
    - Si recibes una lista de DataFrames, 'df1' generalmente contiene las Métricas Operacionales (ej. Gross Profit, Lead Penetration) con columnas como L0W_ROLL.
    - 'df2' generalmente contiene el volumen de Órdenes (columna METRIC = 'Orders') con columnas como L0W, L1W, etc.
    - Si te piden analizar crecimiento de "Orders" y buscar explicaciones, DEBES calcular el crecimiento en df2, e identificar las top zonas. Luego, debes hacer un "merge" de esos resultados con df1 usando la columna 'ZONE' para ver qué métricas mejoraron y explicar el crecimiento.
    - El crecimiento de negocio real se mide mejor usando crecimiento ABSOLUTO (L0W - L8W), no porcentual, ya que evita sesgos de zonas muy pequeñas.
    
    REGLA ESTRICTA DE FORMATO:
    Siempre debes devolver tu respuesta final empezando EXACTAMENTE con la frase "Final Answer: " seguida de tu respuesta en español. 
    Si no usas "Final Answer: " el sistema fallará.
    """

    #Agente de Pandas
    agent = create_pandas_dataframe_agent(
        llm,
        dfs,
        verbose=True, 
        allow_dangerous_code=True, 
        prefix=custom_prefix,
        agent_executor_kwargs={"handle_parsing_errors": True}
    )
    
    return agent