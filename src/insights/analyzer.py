import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os

def generate_executive_report(df_metrics, df_orders=None):
    """
    Versión Pro: 
    1. Cruza con volumen de órdenes para medir impacto real.
    2. Genera alertas de deterioro y de éxito.
    3. Resume por país antes de enviar al LLM.
    """
    
    #PREPARACIÓN DE DATOS
    #Calcular variación WoW
    df_metrics['WoW_Change'] = (df_metrics['L0W_ROLL'] - df_metrics['L1W_ROLL']) / (df_metrics['L1W_ROLL'].abs() + 0.0001)
    
    if df_orders is not None:
        #Sacamos el volumen actual por zona
        volumen = df_orders[['ZONE', 'L0W']].rename(columns={'L0W': 'Vol_Orders'})
        df_metrics = df_metrics.merge(volumen, on='ZONE', how='left')
    else:
        df_metrics['Vol_Orders'] = 1 # Valor neutro si no hay datos
    
    #FILTRADO INTELIGENTE
    #Deterioros criticos (Caen >10% en zonas de alto volumen)
    alertas_negativas = df_metrics[df_metrics['WoW_Change'] <= -0.10].sort_values(by='Vol_Orders', ascending=False).head(8)
    
    #Exitos destacados (Suben >10% en zonas relevantes)
    victorias = df_metrics[df_metrics['WoW_Change'] >= 0.10].sort_values(by='Vol_Orders', ascending=False).head(5)
    
    #Resumen por pais (para darle contexto macro al LLM)
    resumen_pais = df_metrics.groupby('COUNTRY')['WoW_Change'].mean().to_string()

    #GENERACIÓN CON GEMINI
    llm = ChatGoogleGenerativeAI(
        #Gemini como LLM (Recomiendo usar 'gemini-2.5-flash' en este caso estara le version lite por un tema de tokens
        model="gemini-2.5-flash-lite", 
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    prompt = PromptTemplate.from_template("""
    Eres el Director de Estrategia de Rappi. Tu audiencia son Gerentes de Operaciones que necesitan saber dónde actuar HOY.
    
    CONTEXTO MACRO (Variación promedio por país):
    {resumen_pais}
    
    ZONAS CON DETERIORO CRÍTICO (Priorizadas por volumen de órdenes):
    {alertas}
    
    ZONAS CON CRECIMIENTO DESTACADO:
    {victorias}
    
    Escribe un Reporte Ejecutivo en Markdown:
    1. **Estado de la Operación:** Un resumen de 2 frases sobre la salud general de los países.
    2. **Alertas Rojas:** Analiza las caídas críticas. Si varias zonas de un mismo país fallan en la misma métrica, identifícalo como un problema sistémico.
    3. **Oportunidades:** Menciona brevemente las victorias.
    4. **Plan de Acción:** 3 pasos concretos que el equipo debe tomar (ej. "Revisar incentivos en X zona", "Auditar logística de Retail en Y").
    
    Sé ejecutivo, usa negritas para resaltar datos clave y mantén un tono de urgencia pero profesional.
    """)
    
    cadena = prompt | llm
    respuesta = cadena.invoke({
        "resumen_pais": resumen_pais,
        "alertas": alertas_negativas[['COUNTRY', 'ZONE', 'METRIC', 'WoW_Change', 'Vol_Orders']].to_string(index=False),
        "victorias": victorias[['COUNTRY', 'ZONE', 'METRIC', 'WoW_Change', 'Vol_Orders']].to_string(index=False)
    })
    
    return respuesta.content