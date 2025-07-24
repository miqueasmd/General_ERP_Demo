import streamlit as st
import pandas as pd

def mostrar_datos_existentes(seccion: str, subseccion: str, table_manager):
    st.markdown('<div class="section-header"><h3>📊 Registros Existentes</h3></div>', unsafe_allow_html=True)
    df = table_manager.get_dataframe(seccion, subseccion)
    if df.empty:
        st.info(f"ℹ️ No hay registros en {seccion} - {subseccion}")
        return
    if 'Fecha_Pedido' in df.columns:
        df['Fecha_Pedido'] = pd.to_datetime(df['Fecha_Pedido'], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')
    if 'Fecha_Entrega' in df.columns:
        df['Fecha_Entrega'] = pd.to_datetime(df['Fecha_Entrega'], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')
    if 'Cantidad' in df.columns:
        df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce').fillna(0).astype(int)
    text_columns = ['Num_Pedido', 'Nombre_Emisor', 'Cod_Emisor', 'Cod_Art_EAN', 'Cod_Art_Comprador', 'Descripcion', 'Tipo', 'Tipo_Cliche', 'Papel', 'Cod_IPG', 'PDF_Link']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).replace('nan', '').replace('""', '').replace('"', '')
            df[col] = df[col].replace('""', '').replace("''", '')
    df = df.fillna('')
    col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
    with col_filtro1:
        filtro_pedido = st.text_input("🔍 Filtrar por Núm. Pedido", key="filtro_pedido_search", placeholder="Escriba para filtrar...")
    with col_filtro2:
        filtro_emisor = st.text_input("🔍 Filtrar por Emisor", key="filtro_emisor_search", placeholder="Escriba para filtrar...")
    with col_filtro3:
        if filtro_pedido or filtro_emisor:
            st.info("🔍 Filtros activos")
        else:
            st.info("👀 Sin filtros")
    df_filtrado = df.copy()
    if filtro_pedido:
        df_filtrado = df_filtrado[df_filtrado['Num_Pedido'].str.contains(filtro_pedido, case=False, na=False)]
    if filtro_emisor:
        df_filtrado = df_filtrado[df_filtrado['Nombre_Emisor'].str.contains(filtro_emisor, case=False, na=False)]
    st.markdown(f"**Total registros:** {len(df_filtrado)} de {len(df)}")
    if len(df_filtrado) > 0:
        st.info("💡 **Edición de tabla:** Puede editar celdas directamente, añadir filas con ➕ o eliminar filas seleccionando la casilla ☑️ y presionando ❌ (botón eliminar). ¡Los cambios se guardan permanentemente en el CSV al presionar 'Guardar Cambios'!")
    if not df_filtrado.empty:
        df_editado = st.data_editor(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            column_config={
                "Num_Pedido": st.column_config.TextColumn("Núm. Pedido", help="Número de pedido"),
                "Nombre_Emisor": st.column_config.TextColumn("Nombre Emisor", help="Nombre del cliente emisor"),
                "Cod_Emisor": st.column_config.TextColumn("Cód. Emisor", help="Código del emisor"),
                "Fecha_Pedido": st.column_config.TextColumn("Fecha Pedido", help="Fecha de pedido (DD/MM/YYYY)"),
                "Fecha_Entrega": st.column_config.TextColumn("Fecha Entrega", help="Fecha de entrega (DD/MM/YYYY)"),
                "Cod_Art_EAN": st.column_config.TextColumn("Cód. EAN", help="Código EAN del artículo"),
                "Cod_Art_Comprador": st.column_config.TextColumn("Cód. Comprador", help="Código del artículo del comprador"),
                "Descripcion": st.column_config.TextColumn("Descripción", help="Descripción del producto"),
                "Cantidad": st.column_config.NumberColumn("Cantidad", min_value=0, step=1, format="%d"),
                "Tipo": st.column_config.TextColumn("Tipo", help="Tipo de producto"),
                "Tipo_Cliche": st.column_config.TextColumn("Tipo Cliché", help="Tipo de cliché"),
                "Papel": st.column_config.TextColumn("Papel", help="Tipo de papel"),
                "Cod_IPG": st.column_config.TextColumn("Cód. IPG", help="Código IPG interno"),
                "PDF_Link": st.column_config.LinkColumn("PDF Link", help="Enlace al PDF del pedido - Click para abrir", display_text="🔗 Ver PDF")
            }
        )
        col_guardar, col_info = st.columns([2, 3])
        with col_guardar:
            if st.button("💾 Guardar Cambios", key=f"guardar_{seccion}_{subseccion}"):
                registros_originales = len(df)
                registros_editados = len(df_editado)
                registros_eliminados = registros_originales - registros_editados
                registros_añadidos = max(0, registros_editados - registros_originales)
                df_para_guardar = df_editado.copy()
                # Eliminar conversión innecesaria de fechas, ya son strings en formato DD/MM/YYYY
                if table_manager.save_dataframe(seccion, subseccion, df_para_guardar):
                    mensaje_cambios = []
                    if registros_eliminados > 0:
                        mensaje_cambios.append(f"🗑️ {registros_eliminados} registro(s) **eliminado(s) con éxito**")
                    if registros_añadidos > 0:
                        mensaje_cambios.append(f"➕ {registros_añadidos} registro(s) **añadido(s) con éxito**")
                    if mensaje_cambios:
                        st.success(f"✅ **¡Cambios guardados con éxito!** {' • '.join(mensaje_cambios)}")
                        st.info(f"📊 **Total registros actuales:** {len(df_para_guardar)}")
                        st.rerun()
                    else:
                        st.success("✅ **¡Cambios guardados con éxito!** Los registros han sido **actualizados correctamente**")
                else:
                    st.error("❌ **Error al guardar cambios en la base de datos**")
        with col_info:
            st.info("💡 **Cómo usar:** Edite celdas directamente, use ➕ para añadir filas, seleccione filas con ☑️ y use ❌ para eliminar. Presione 'Guardar Cambios' para hacer los cambios permanentes.") 