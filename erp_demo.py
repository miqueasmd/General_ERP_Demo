"""
DemoERP - Demo Application
Simple web interface for managing Customers and Suppliers
Optimized for RPA automation with Power Automate Desktop

Main entry point for the DemoERP Streamlit application.
Handles sidebar navigation, section selection, and main workflow.
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date
from database import TableManager
from modules.ui_layout import set_page_config, main_header, sidebar_logo
from modules.form_entry import show_entry_form
from modules.table_view import show_existing_records
from modules.demo_data import create_demo_data

set_page_config()

# Initialize the main table manager in session state
if 'table_manager' not in st.session_state:
    st.session_state.table_manager = TableManager()

def main():
    """
    Main function for the DemoERP app.
    Handles sidebar navigation, section/type selection, and tabbed content display.
    """
    main_header()
    with st.sidebar:
        sidebar_logo()
        st.markdown("### 📋 Main Menu")
        # Section selection (Customers or Suppliers)
        section = st.radio(
            "Select Section:",
            ["Customers", "Suppliers"],
            key="main_section"
        )
        st.markdown("---")
        # Subsection selection (Orders, Delivery Notes, Invoices)
        subsection = st.radio(
            "Select Type:",
            ["Orders", "Delivery Notes", "Invoices"],
            key="subsection"
        )
        st.markdown("---")
        st.markdown("### ℹ️ System Info")
        backend_info = "PostgreSQL (Neon)" if st.session_state.table_manager.use_neon else "Local CSV"
        st.info(f"**Backend:** {backend_info}")
        st.info(f"**Active Section:** {section}")
        st.info(f"**Type:** {subsection}")
        st.markdown("---")
        # Demo data button for quick form filling
        st.markdown("### 🧪 Demo")
        demo_button_clicked = st.button("📋 Fill Demo Form", help="Fill the form with sample demo data")
        if 'demo_counter' not in st.session_state:
            st.session_state.demo_counter = 0
        if demo_button_clicked:
            # Only available for Customers - Orders
            if section == "Customers" and subsection == "Orders":
                demo_data_df = create_demo_data()
                total = len(demo_data_df)
                # Advance the counter and wrap around
                st.session_state.demo_counter = (st.session_state.demo_counter + 1) % total
                current_record = demo_data_df.iloc[st.session_state.demo_counter]
                demo_data = current_record.to_dict()
                st.session_state.demo_data = demo_data
                st.session_state.demo_loaded = True
                st.session_state.demo_info = {
                    'counter': st.session_state.demo_counter + 1,
                    'total': total,
                    'order': demo_data['Num_Pedido'],
                    'customer': demo_data['Nombre_Emisor']
                }
                st.session_state.demo_message = True
            else:
                st.warning("⚠️ Only available for Customers - Orders")
        # Show demo message in the form if applicable
        if st.session_state.get('demo_message', False):
            st.success("Form filled with demo data. Click 'Save to ERP' to add the record.")
    # Main content area: show form and table for Customers-Orders, or placeholder for other sections
    if section == "Customers" and subsection == "Orders":
        st.markdown(f"## 📦 {section} - {subsection} Management")
        tab1, tab2 = st.tabs(["📝 New Record", "📊 View/Edit Records"])
        with tab1:
            show_entry_form(section, subsection, st.session_state.table_manager)
        with tab2:
            show_existing_records(section, subsection, st.session_state.table_manager)
    else:
        st.markdown(f"## 🚧 {section} - {subsection}")
        st.info(f"📋 Section **{subsection}** for **{section}** is under construction.")
        st.markdown("""
            This section will be available in future versions of the ERP.
            **Planned features:**
            - ✅ Full record management
            - ✅ Export to Excel/PDF
            - ✅ Integration with external systems
            - ✅ Automated reports
        """)

if __name__ == "__main__":
    main()
