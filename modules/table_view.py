"""
Table view module for DemoERP
Provides the UI and logic for displaying and editing existing records.
"""
import streamlit as st
import pandas as pd

def show_existing_records(section: str, subsection: str, table_manager):
    """
    Render the table view for existing records in the ERP.
    Allows filtering, inline editing, and saving changes.
    """
    st.markdown('<div class="section-header"><h3>📊 Existing Records</h3></div>', unsafe_allow_html=True)
    df = table_manager.get_dataframe(section, subsection)
    if df.empty:
        st.info(f"ℹ️ No records in {section} - {subsection}")
        return
    # Format columns for display
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
    # Filter controls
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    with col_filter1:
        filter_order = st.text_input("🔍 Filter by Order Number", key="filter_order_search", placeholder="Type to filter...")
    with col_filter2:
        filter_sender = st.text_input("🔍 Filter by Sender", key="filter_sender_search", placeholder="Type to filter...")
    with col_filter3:
        if filter_order or filter_sender:
            st.info("🔍 Active filters")
        else:
            st.info("👀 No filters")
    df_filtered = df.copy()
    if filter_order:
        df_filtered = df_filtered[df_filtered['Num_Pedido'].str.contains(filter_order, case=False, na=False)]
    if filter_sender:
        df_filtered = df_filtered[df_filtered['Nombre_Emisor'].str.contains(filter_sender, case=False, na=False)]
    st.markdown(f"**Total records:** {len(df_filtered)} of {len(df)}")
    if len(df_filtered) > 0:
        st.info("💡 **Table editing:** You can edit cells directly, add rows with ➕ or delete rows by selecting the checkbox ☑️ and pressing ❌ (delete button). Changes are saved permanently to the CSV when you press 'Save Changes'!")
    if not df_filtered.empty:
        df_edited = st.data_editor(
            df_filtered,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            column_config={
                "Num_Pedido": st.column_config.TextColumn("Order Number", help="Order number"),
                "Nombre_Emisor": st.column_config.TextColumn("Sender Name", help="Customer sender name"),
                "Cod_Emisor": st.column_config.TextColumn("Sender Code", help="Sender code"),
                "Fecha_Pedido": st.column_config.TextColumn("Order Date", help="Order date (DD/MM/YYYY)"),
                "Fecha_Entrega": st.column_config.TextColumn("Delivery Date", help="Delivery date (DD/MM/YYYY)"),
                "Cod_Art_EAN": st.column_config.TextColumn("EAN Code", help="Article EAN code"),
                "Cod_Art_Comprador": st.column_config.TextColumn("Buyer Code", help="Buyer's article code"),
                "Descripcion": st.column_config.TextColumn("Description", help="Product description"),
                "Cantidad": st.column_config.NumberColumn("Quantity", min_value=0, step=1, format="%d"),
                "Tipo": st.column_config.TextColumn("Product Type", help="Product type"),
                "Tipo_Cliche": st.column_config.TextColumn("Cliché Type", help="Cliché type"),
                "Papel": st.column_config.TextColumn("Paper", help="Paper type"),
                "Cod_IPG": st.column_config.TextColumn("Internal Code", help="Internal code"),
                "PDF_Link": st.column_config.LinkColumn("PDF Link", help="Order PDF link - Click to open", display_text="🔗 View PDF")
            }
        )
        # Save and info controls
        col_save, col_info = st.columns([2, 3])
        with col_save:
            if st.button("💾 Save Changes", key=f"save_{section}_{subsection}"):
                original_records = len(df)
                edited_records = len(df_edited)
                deleted_records = original_records - edited_records
                added_records = max(0, edited_records - original_records)
                df_to_save = df_edited.copy()
                # No need to convert dates, already strings in DD/MM/YYYY format
                if table_manager.save_dataframe(section, subsection, df_to_save):
                    change_messages = []
                    if deleted_records > 0:
                        change_messages.append(f"🗑️ {deleted_records} record(s) **successfully deleted**")
                    if added_records > 0:
                        change_messages.append(f"➕ {added_records} record(s) **successfully added**")
                    if change_messages:
                        st.success(f"✅ **Changes saved successfully!** {' • '.join(change_messages)}")
                        st.info(f"📊 **Current total records:** {len(df_to_save)}")
                        st.rerun()
                    else:
                        st.success("✅ **Changes saved successfully!** Records have been **updated correctly**")
                else:
                    st.error("❌ **Error saving changes to the database**")
        with col_info:
            st.info("💡 **How to use:** Edit cells directly, use ➕ to add rows, select rows with ☑️ and use ❌ to delete. Press 'Save Changes' to make changes permanent.") 