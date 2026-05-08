import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_rappi_data():
    """
    Carga todas hojas del excel
    """
    #ruta
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(base_dir, "data", "Sistema de Análisis Inteligente para Operaciones Rappi - Dummy Data.xlsx") 

    try:
        xls = pd.ExcelFile(file_path)
        dataframes = {}

        for sheet in xls.sheet_names:
            dataframes[sheet] = pd.read_excel(xls, sheet_name=sheet)

        return dataframes
        
    except FileNotFoundError:
        st.error(f"Error: No se encontró el archivo Excel en la carpeta 'data'. Verifica el nombre.")
        return None
    except Exception as e:
        st.error(f"Error inesperado al cargar los datos: {e}")
        return None