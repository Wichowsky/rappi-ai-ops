# Rappi Ops - AI Explorer

Un Sistema de Análisis Inteligente de Operaciones diseñado para los equipos de Strategy & Ops de Rappi. Esta herramienta proporciona una interfaz de lenguaje natural para consultar métricas operativas y automatiza la detección de anomalías de negocio a través de múltiples conjuntos de datos.

## Arquitectura Técnica

El sistema está construido sobre una arquitectura modular que separa el procesamiento de datos del motor de razonamiento:

* **LLM:** Google Gemini 2.5 Flash.
* **Framework:** LangChain (Pandas Agent & AgentExecutor).
* **Motor de Datos:** Pandas para cruces (joins) de múltiples tablas y agregaciones en tiempo real.
* **Interfaz:** Streamlit para una visualización de datos profesional y accesible.

## Capacidades Principales

* **Razonamiento Multi-Dataset:** El agente está configurado para realizar cruces relacionales entre fuentes de datos separadas (`RAW_ORDERS` y `RAW_INPUT_METRICS`) para proporcionar respuestas contextualizadas que conectan el volumen con la eficiencia.
* **Insights Automáticos:** Un módulo de análisis especializado que identifica anomalías operativas y casos de éxito, priorizándolos por su impacto en el negocio (Volumen de Órdenes).
* **Estabilidad de Formato:** Implementación de `AgentExecutor` con manejo de errores estandarizado (`handle_parsing_errors`) para garantizar un análisis y salida de datos consistentes.

## Estructura del Proyecto

* **`assets/`**: Recursos visuales y logos.
* **`src/`**: Código fuente de la aplicación.
  * **`bot/`**: Configuración y lógica del Agente LangChain.
  * **`insights/`**: Algoritmos de detección automática de anomalías.
  * **`utils/`**: Scripts de carga y limpieza de datos.
* **`app.py`**: Punto de entrada principal de la aplicación Streamlit.
* **`requirements.txt`**: Dependencias del proyecto.
* **`.env`**: Variables de entorno (Excluido vía .gitignore).

## Clonar el repositorio

git clone [https://github.com/Wichowsky/rappi-ai-ops.git](https://github.com/Wichowsky/rappi-ai-ops.git)

## Acceder al repositorio

cd rappi-ai-ops

## Configuración del Entorno

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## Variable de entorno

GOOGLE_API_KEY=Aca hay que colocar la llave de la api de google que se disponga

## Ejecución

streamlit run app.py

## Autoria

Desarrollado por Daniel Liberato