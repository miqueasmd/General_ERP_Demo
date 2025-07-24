"""
Global configuration for DemoERP
Centralizes constants and system settings for the application.
"""

# Application information (name, version, description)
APP_INFO = {
    'name': 'DemoERP',
    'version': '1.0.0',
    'description': 'Demo system for managing Customers and Suppliers'
}

# DemoERP corporate colors (UI branding)
COLORS = {
    'primary': '#E7343F',      # Main red (branding)
    'secondary': '#00356B',    # Navy blue
    'success': '#6FE3A6',      # Confirmation green
    'background': '#F5F7FA',   # Main background
    'white': '#ffffff'
}

# Streamlit app configuration (page title, layout, sidebar)
STREAMLIT_CONFIG = {
    'page_title': 'DemoERP',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# System messages (UI feedback for user actions)
MESSAGES = {
    'loading': '⏳ Loading data...',
    'success_save': '✅ Record saved successfully!',
    'error_save': '❌ Error saving the record',
    'demo_loaded': '✅ Form filled with demo data',
    'no_records': 'ℹ️ No records available',
    'validation_error': '❌ Please complete all required fields'
}

# Database configuration (CSV directory, backup options)
DATABASE_CONFIG = {
    'csv_dir': 'data',
    'backup_enabled': True,
    'auto_backup_interval': 24  # hours
}

# System limits (display, file size, description length)
LIMITS = {
    'max_records_display': 1000,
    'max_file_size_mb': 10,
    'max_description_length': 500
}
