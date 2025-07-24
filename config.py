"""
Configuración global para ERP IPGFLEXO
Centraliza constantes y configuraciones del sistema
"""

# Información de la aplicación
APP_INFO = {
    'name': 'ERP IPGFLEXO',
    'version': '1.0.0',
    'description': 'Sistema de demostración para gestión de Clientes y Proveedores'
}

# Colores corporativos IPGFLEXO
COLORS = {
    'primary': '#E7343F',      # Rojo IPGFLEXO
    'secondary': '#00356B',    # Azul marino
    'success': '#6FE3A6',      # Verde confirmación
    'background': '#F5F7FA',   # Fondo principal
    'white': '#ffffff'
}

# Configuración de la aplicación
STREAMLIT_CONFIG = {
    'page_title': 'ERP IPGFLEXO',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Mensajes del sistema
MESSAGES = {
    'loading': '⏳ Cargando datos...',
    'success_save': '✅ ¡Registro guardado con éxito!',
    'error_save': '❌ Error al guardar el registro',
    'demo_loaded': '✅ Formulario rellenado con datos de demostración',
    'no_records': 'ℹ️ No hay registros disponibles',
    'validation_error': '❌ Por favor, completa todos los campos obligatorios'
}

# Configuración de base de datos
DATABASE_CONFIG = {
    'csv_dir': 'data',
    'backup_enabled': True,
    'auto_backup_interval': 24  # horas
}

# Límites del sistema
LIMITS = {
    'max_records_display': 1000,
    'max_file_size_mb': 10,
    'max_description_length': 500
}
