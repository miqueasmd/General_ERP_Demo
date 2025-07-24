"""
Form entry module for DemoERP
Provides the form UI and logic for adding new records (orders, etc.)
"""
import streamlit as st
import pandas as pd
from datetime import datetime

def show_entry_form(section: str, subsection: str, table_manager):
    """
    Render the entry form for adding a new record to the ERP.
    Handles validation, demo data, and saving logic.
    """
    st.markdown('<div class="section-header"><h3>📝 New Record</h3></div>', unsafe_allow_html=True)
    if st.session_state.get('demo_loaded', False):
        demo_info = st.session_state.get('demo_info', {})
        # Do not show demo message, just leave the form ready
        if st.session_state.get('demo_message', False):
            del st.session_state['demo_message']
    st.markdown("""
    <div style='background: #E7343F11; padding: 0.5rem; border-radius: 6px; border-left: 4px solid #E7343F; margin-bottom: 1rem;'>
        <strong>📌 Required Fields:</strong> Fields marked with <span style='color: #E7343F;'>*</span> are mandatory
    </div>
    """, unsafe_allow_html=True)
    # Main form for data entry
    with st.form(key=f"form_{section}_{subsection}"):
        demo_data = st.session_state.get('demo_data', {})
        col1, col2, col3 = st.columns(3)
        with col1:
            order_number = st.text_input("Order Number *", key="Num_Pedido", help="Required field to identify the order", value=demo_data.get('Num_Pedido', ''))
            sender_name = st.text_input("Sender Name *", key="Nombre_Emisor", help="Required field - Customer name", value=demo_data.get('Nombre_Emisor', ''))
            sender_code = st.text_input("Sender Code", key="Cod_Emisor", value=demo_data.get('Cod_Emisor', ''))
            # Show date in DD/MM/YYYY format
            order_date_str = demo_data.get('Fecha_Pedido', datetime.now().strftime('%d/%m/%Y'))
            order_date = st.text_input("Order Date *", key="Fecha_Pedido", help="Required field - Order date (DD/MM/YYYY)", value=order_date_str)
            delivery_date_str = demo_data.get('Fecha_Entrega', datetime.now().strftime('%d/%m/%Y')) if demo_data.get('Fecha_Entrega') else ''
            delivery_date = st.text_input("Delivery Date", key="Fecha_Entrega", value=delivery_date_str)
        with col2:
            ean_code = st.text_input("EAN Code", key="Cod_Art_EAN", value=demo_data.get('Cod_Art_EAN', ''))
            buyer_code = st.text_input("Buyer Code", key="Cod_Art_Comprador", value=demo_data.get('Cod_Art_Comprador', ''))
            quantity = st.number_input("Quantity *", min_value=0.0, step=1.0, key="Cantidad", help="Required field - Order quantity", format="%.0f", value=float(demo_data.get('Cantidad', 0)))
            product_type = st.text_input("Product Type", key="Tipo", value=demo_data.get('Tipo', ''))
            cliche_type = st.text_input("Cliché Type", key="Tipo_Cliche", value=demo_data.get('Tipo_Cliche', ''))
        with col3:
            description = st.text_area("Description *", key="Descripcion", help="Required field - Product/service description", value=demo_data.get('Descripcion', ''))
            paper = st.text_input("Paper", key="Papel", value=demo_data.get('Papel', ''))
            internal_code = st.text_input("Internal Code", key="Cod_IPG", value=demo_data.get('Cod_IPG', ''))
            pdf_link = st.text_input("PDF Link", key="PDF_Link", value=demo_data.get('PDF_Link', ''))
        col_submit, col_clear = st.columns(2)
        with col_submit:
            submitted = st.form_submit_button("💾 Save to ERP", use_container_width=True)
        with col_clear:
            clear_form = st.form_submit_button("🧹 Clear Form", use_container_width=True, type="secondary")
        # Clear form logic
        if clear_form:
            if 'demo_data' in st.session_state:
                del st.session_state.demo_data
            if 'demo_loaded' in st.session_state:
                del st.session_state.demo_loaded
            if 'demo_info' in st.session_state:
                del st.session_state.demo_info
            st.rerun()
        # Submission and validation logic
        if submitted:
            errors = []
            # Validate date format DD/MM/YYYY
            try:
                order_date_dt = datetime.strptime(order_date, '%d/%m/%Y')
            except Exception:
                errors.append("• Order Date (format DD/MM/YYYY)")
            try:
                delivery_date_dt = datetime.strptime(delivery_date, '%d/%m/%Y') if delivery_date else None
            except Exception:
                errors.append("• Delivery Date (format DD/MM/YYYY)")
            if not order_number or order_number.strip() == "":
                errors.append("• Order Number")
            if not sender_name or sender_name.strip() == "":
                errors.append("• Sender Name")
            if not description or description.strip() == "":
                errors.append("• Description")
            if quantity <= 0:
                errors.append("• Quantity (must be greater than 0)")
            if not order_date:
                errors.append("• Order Date")
            if errors:
                st.error(f"""
                ❌ **Cannot save record. The following required fields are missing or the date format is incorrect:**
                {chr(10).join(errors)}
                Please complete all fields marked with * before saving.
                """)
            else:
                new_record = {
                    'Num_Pedido': str(order_number.strip()),
                    'Nombre_Emisor': str(sender_name.strip()),
                    'Cod_Emisor': str(sender_code.strip()) if sender_code else '',
                    'Fecha_Pedido': order_date_dt.strftime('%d/%m/%Y'),
                    'Fecha_Entrega': delivery_date_dt.strftime('%d/%m/%Y') if delivery_date_dt else '',
                    'Cod_Art_EAN': str(ean_code.strip()) if ean_code else '',
                    'Cod_Art_Comprador': str(buyer_code.strip()) if buyer_code else '',
                    'Descripcion': str(description.strip()),
                    'Cantidad': int(quantity),
                    'Tipo': str(product_type.strip()) if product_type else '',
                    'Tipo_Cliche': str(cliche_type.strip()) if cliche_type else '',
                    'Papel': str(paper.strip()) if paper else '',
                    'Cod_IPG': str(internal_code.strip()) if internal_code else '',
                    'PDF_Link': str(pdf_link.strip()) if pdf_link else ''
                }
                df_current = table_manager.get_dataframe(section, subsection)
                df_new = pd.concat([df_current, pd.DataFrame([new_record])], ignore_index=True)
                if table_manager.save_dataframe(section, subsection, df_new):
                    st.session_state['save_success'] = True
                    st.rerun()
                else:
                    st.error("❌ **Error saving the record to the database**") 
    # Show success message after saving, outside the form
    if st.session_state.get('save_success', False):
        st.success("✅ Record added successfully!")
        del st.session_state['save_success'] 