import streamlit as st
import pandas as pd
from datetime import datetime

def mostrar_formulario_entrada(seccion: str, subseccion: str, table_manager):
    st.markdown('<div class="section-header"><h3>📝 Nuevo Registro</h3></div>', unsafe_allow_html=True)
    if st.session_state.get('demo_loaded', False):
        demo_info = st.session_state.get('demo_info', {})
        # No mostrar mensaje de demo, solo dejar el formulario listo
        if st.session_state.get('demo_message', False):
            del st.session_state['demo_message']
    st.markdown("""
    <div style='background: #E7343F11; padding: 0.5rem; border-radius: 6px; border-left: 4px solid #E7343F; margin-bottom: 1rem;'>
        <strong>📌 Campos Obligatorios:</strong> Los campos marcados con <span style='color: #E7343F;'>*</span> son obligatorios
    </div>
    """, unsafe_allow_html=True)
    with st.form(key=f"formulario_{seccion}_{subseccion}"):
        demo_data = st.session_state.get('demo_data', {})
        col1, col2, col3 = st.columns(3)
        with col1:
            num_pedido = st.text_input("Número de Pedido *", key="Num_Pedido", help="Campo obligatorio para identificar el pedido", value=demo_data.get('Num_Pedido', ''))
            nombre_emisor = st.text_input("Nombre del Emisor *", key="Nombre_Emisor", help="Campo obligatorio - Nombre del cliente", value=demo_data.get('Nombre_Emisor', ''))
            cod_emisor = st.text_input("Código del Emisor", key="Cod_Emisor", value=demo_data.get('Cod_Emisor', ''))
            # Mostrar la fecha en formato DD/MM/YYYY
            fecha_pedido_str = demo_data.get('Fecha_Pedido', datetime.now().strftime('%d/%m/%Y'))
            fecha_pedido = st.text_input("Fecha del Pedido *", key="Fecha_Pedido", help="Campo obligatorio - Fecha del pedido (DD/MM/AAAA)", value=fecha_pedido_str)
            fecha_entrega_str = demo_data.get('Fecha_Entrega', datetime.now().strftime('%d/%m/%Y')) if demo_data.get('Fecha_Entrega') else ''
            fecha_entrega = st.text_input("Fecha de Entrega", key="Fecha_Entrega", value=fecha_entrega_str)
        with col2:
            cod_art_ean = st.text_input("Código Art. EAN", key="Cod_Art_EAN", value=demo_data.get('Cod_Art_EAN', ''))
            cod_art_comprador = st.text_input("Código Art. Comprador", key="Cod_Art_Comprador", value=demo_data.get('Cod_Art_Comprador', ''))
            cantidad = st.number_input("Cantidad *", min_value=0.0, step=1.0, key="Cantidad", help="Campo obligatorio - Cantidad del pedido", format="%.0f", value=float(demo_data.get('Cantidad', 0)))
            tipo = st.text_input("Tipo", key="Tipo", value=demo_data.get('Tipo', ''))
            tipo_cliche = st.text_input("Tipo Cliché", key="Tipo_Cliche", value=demo_data.get('Tipo_Cliche', ''))
        with col3:
            descripcion = st.text_area("Descripción *", key="Descripcion", help="Campo obligatorio - Descripción del producto/servicio", value=demo_data.get('Descripcion', ''))
            papel = st.text_input("Papel", key="Papel", value=demo_data.get('Papel', ''))
            cod_ipg = st.text_input("Código IPG", key="Cod_IPG", value=demo_data.get('Cod_IPG', ''))
            pdf_link = st.text_input("PDF Link", key="PDF_Link", value=demo_data.get('PDF_Link', ''))
        col_submit, col_clear = st.columns(2)
        with col_submit:
            submitted = st.form_submit_button("💾 Guardar en ERP", use_container_width=True)
        with col_clear:
            clear_form = st.form_submit_button("🧹 Limpiar Formulario", use_container_width=True, type="secondary")
        if clear_form:
            if 'demo_data' in st.session_state:
                del st.session_state.demo_data
            if 'demo_loaded' in st.session_state:
                del st.session_state.demo_loaded
            if 'demo_info' in st.session_state:
                del st.session_state.demo_info
            st.rerun()
        if submitted:
            errores = []
            # Validar formato de fecha DD/MM/YYYY
            try:
                fecha_pedido_dt = datetime.strptime(fecha_pedido, '%d/%m/%Y')
            except Exception:
                errores.append("• Fecha del Pedido (formato DD/MM/AAAA)")
            try:
                fecha_entrega_dt = datetime.strptime(fecha_entrega, '%d/%m/%Y') if fecha_entrega else None
            except Exception:
                errores.append("• Fecha de Entrega (formato DD/MM/AAAA)")
            if not num_pedido or num_pedido.strip() == "":
                errores.append("• Número de Pedido")
            if not nombre_emisor or nombre_emisor.strip() == "":
                errores.append("• Nombre del Emisor")
            if not descripcion or descripcion.strip() == "":
                errores.append("• Descripción")
            if cantidad <= 0:
                errores.append("• Cantidad (debe ser mayor a 0)")
            if not fecha_pedido:
                errores.append("• Fecha del Pedido")
            if errores:
                st.error(f"""
                ❌ **No se puede guardar el registro. Faltan los siguientes campos obligatorios o el formato de fecha es incorrecto:**
                {chr(10).join(errores)}
                Por favor, completa todos los campos marcados con * antes de guardar.
                """)
            else:
                nuevo_registro = {
                    'Num_Pedido': str(num_pedido.strip()),
                    'Nombre_Emisor': str(nombre_emisor.strip()),
                    'Cod_Emisor': str(cod_emisor.strip()) if cod_emisor else '',
                    'Fecha_Pedido': fecha_pedido_dt.strftime('%d/%m/%Y'),
                    'Fecha_Entrega': fecha_entrega_dt.strftime('%d/%m/%Y') if fecha_entrega_dt else '',
                    'Cod_Art_EAN': str(cod_art_ean.strip()) if cod_art_ean else '',
                    'Cod_Art_Comprador': str(cod_art_comprador.strip()) if cod_art_comprador else '',
                    'Descripcion': str(descripcion.strip()),
                    'Cantidad': int(cantidad),
                    'Tipo': str(tipo.strip()) if tipo else '',
                    'Tipo_Cliche': str(tipo_cliche.strip()) if tipo_cliche else '',
                    'Papel': str(papel.strip()) if papel else '',
                    'Cod_IPG': str(cod_ipg.strip()) if cod_ipg else '',
                    'PDF_Link': str(pdf_link.strip()) if pdf_link else ''
                }
                df_actual = table_manager.get_dataframe(seccion, subseccion)
                df_nuevo = pd.concat([df_actual, pd.DataFrame([nuevo_registro])], ignore_index=True)
                if table_manager.save_dataframe(seccion, subseccion, df_nuevo):
                    st.session_state['registro_exito'] = True
                    st.rerun()
                else:
                    st.error("❌ **Error al guardar el registro en la base de datos**") 
    # Mostrar mensaje de éxito tras guardar, fuera del formulario
    if st.session_state.get('registro_exito', False):
        st.success("✅ ¡Registro añadido con éxito!")
        del st.session_state['registro_exito'] 