"""
ERP Ficticio IPGFLEXO - Aplicación de Demostración
Interfaz web simple para gestión de Clientes y Proveedores
Optimizada para automatización RPA con Power Automate Desktop
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date
from database import TableManager
from modules.ui_layout import set_page_config, main_header, sidebar_logo
from modules.formulario import mostrar_formulario_entrada
from modules.tabla import mostrar_datos_existentes
from modules.demo_data import crear_datos_demo_sharepoint

set_page_config()

if 'table_manager' not in st.session_state:
    st.session_state.table_manager = TableManager()

def main():
    main_header()
    with st.sidebar:
        sidebar_logo()
        st.markdown("### 📋 Menú Principal ERP")
        seccion = st.radio(
            "Seleccionar Sección:",
            ["Clientes", "Proveedores"],
            key="seccion_principal"
        )
        st.markdown("---")
        subseccion = st.radio(
            "Seleccionar Tipo:",
            ["Pedidos", "Albaranes", "Facturas"],
            key="subseccion"
        )
        st.markdown("---")
        st.markdown("### ℹ️ Sistema")
        backend_info = "PostgreSQL (Neon)" if st.session_state.table_manager.use_neon else "CSV Local"
        st.info(f"**Backend:** {backend_info}")
        st.info(f"**Sección Activa:** {seccion}")
        st.info(f"**Tipo:** {subseccion}")
        st.markdown("---")
        # Sección 'Sistema' eliminada por no aportar información visible relevante
        st.markdown("### 🧪 Demo")
        demo_button_clicked = st.button("📋 Rellenar Formulario Demo", help="Rellena el formulario con datos de ejemplo de SharePoint")
        if 'demo_counter' not in st.session_state:
            st.session_state.demo_counter = 0
        if demo_button_clicked:
            if seccion == "Clientes" and subseccion == "Pedidos":
                datos_sharepoint = crear_datos_demo_sharepoint()
                total = len(datos_sharepoint)
                # Avanzar el contador y hacer wrap-around
                st.session_state.demo_counter = (st.session_state.demo_counter + 1) % total
                registro_actual = datos_sharepoint.iloc[st.session_state.demo_counter]
                demo_data = registro_actual.to_dict()
                st.session_state.demo_data = demo_data
                st.session_state.demo_loaded = True
                st.session_state.demo_info = {
                    'counter': st.session_state.demo_counter + 1,
                    'total': total,
                    'pedido': demo_data['Num_Pedido'],
                    'cliente': demo_data['Nombre_Emisor']
                }
                st.session_state.demo_message = True
            else:
                st.warning("⚠️ Solo disponible para Clientes - Pedidos")
        # Mostrar mensaje de demo en el formulario si corresponde
        if st.session_state.get('demo_message', False):
            st.success("Formulario relleno con datos de demostración. Pulse 'Guardar en ERP' para añadir el registro.")
    if seccion == "Clientes" and subseccion == "Pedidos":
        st.markdown(f"## 📦 {seccion} - Gestión de {subseccion}")
        tab1, tab2 = st.tabs(["📝 Nuevo Registro", "📊 Ver/Editar Registros"])
        with tab1:
            mostrar_formulario_entrada(seccion, subseccion, st.session_state.table_manager)
        with tab2:
            mostrar_datos_existentes(seccion, subseccion, st.session_state.table_manager)
    else:
        st.markdown(f"## 🚧 {seccion} - {subseccion}")
        st.info(f"📋 Sección **{subseccion}** para **{seccion}** en construcción.")
        st.markdown("""
            Esta sección estará disponible en futuras versiones del ERP.
            **Funcionalidades planificadas:**
            - ✅ Gestión completa de registros
            - ✅ Exportación a Excel/PDF
            - ✅ Integración con sistemas externos
            - ✅ Reportes automáticos
        """)

if __name__ == "__main__":
    main()
