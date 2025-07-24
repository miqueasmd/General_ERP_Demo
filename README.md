# 🏭 ERP Ficticio IPGFLEXO - Demo

Sistema de demostración para gestión de Clientes y Proveedores, diseñado con interfaz simple y optimizado para automatización RPA.

## 🎯 Características Principales

- **Interfaz Simple**: Diseñada específicamente para automatización con Power Automate Desktop
- **Gestión Completa**: Manejo de Pedidos, Albaranes y Facturas para Clientes y Proveedores  
- **Persistencia Dual**: Soporte para CSV local o PostgreSQL (Neon) remoto
- **Branding Corporativo**: Colores y estilo de IPGFLEXO
- **Edición en Tiempo Real**: Tablas editables con validación automática

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd IPGFLEXO_DemoERP
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   streamlit run erp_demo.py
   ```

4. **Abrir en navegador**
   - La aplicación se abrirá automáticamente en `http://localhost:8501`
   - Si no se abre automáticamente, copia la URL que aparece en terminal

## 🔧 Configuración

### Modo CSV (Por Defecto)
La aplicación usa archivos CSV en la carpeta `./data/` para persistencia.
No requiere configuración adicional.

### Modo PostgreSQL (Opcional)
Para usar PostgreSQL con Neon, configura estas variables de entorno:

```bash
# Windows (PowerShell)
$env:USE_NEON = "1"
$env:PGHOST = "tu-host.neon.tech"
$env:PGUSER = "tu-usuario"
$env:PGPASSWORD = "tu-password"
$env:PGDATABASE = "tu-database"

# Linux/Mac
export USE_NEON=1
export PGHOST=tu-host.neon.tech
export PGUSER=tu-usuario
export PGPASSWORD=tu-password
export PGDATABASE=tu-database
```

## 📋 Estructura de Datos

Cada registro en el ERP contiene los siguientes campos:

| Campo | Descripción | Tipo |
|-------|-------------|------|
| Num_Pedido | Número único del pedido | Texto |
| Nombre_Emisor | Nombre del cliente/proveedor | Texto |
| Cod_Emisor | Código del emisor | Texto |
| Estado | Estado del pedido (Pendiente/Comprobado) | Selección |
| En_ERP | Si está en el ERP (Sí/No) | Selección |
| Fecha_Pedido | Fecha del pedido (DD/MM/AAAA) | Fecha (texto) |
| Fecha_Entrega | Fecha de entrega prevista (DD/MM/AAAA) | Fecha (texto) |
| Cod_Art_EAN | Código EAN del artículo | Texto |
| Cod_Art_Comprador | Código del comprador | Texto |
| Descripcion | Descripción del pedido | Texto largo |
| Cantidad | Cantidad solicitada | Número |
| Tipo | Tipo de producto | Texto |
| Tipo_Cliche | Tipo de cliché | Texto |
| Papel | Tipo de papel | Texto |
| Cod_IPG | Código IPG interno | Texto |
| PDF_Link | Enlace al PDF del pedido | URL |

## 🎨 Personalización Visual

### Colores Corporativos IPGFLEXO
- **Rojo Principal**: #E7343F (botones, acentos)
- **Azul Marino**: #00356B (cabeceras, sidebar)
- **Verde Confirmación**: #6FE3A6 (estado "Comprobado")
- **Fondo Principal**: #F5F7FA

### Logo Personalizado
Para añadir el logo de IPGFLEXO:
1. Coloca tu archivo de logo en la carpeta del proyecto
2. Edita `erp_demo.py` línea ~87 (buscar "Logo placeholder")
3. Reemplaza la línea con: `st.image("tu-logo.png", use_column_width=True)`

## 🤖 Optimización para RPA

### Power Automate Desktop
La interfaz está optimizada para automatización:

- **IDs estables**: Todos los campos tienen IDs únicos y consistentes
- **Selectores CSS**: Elementos con clases CSS específicas para localización fácil
- **Botones prominentes**: Acciones principales claramente identificables
- **Validación mínima**: Reduce errores en automatización

### Principales Selectores para RPA:

```css
/* Formulario de entrada */
input[aria-label="Número de Pedido"]
input[aria-label="Nombre del Emisor"] 
div[data-testid="stSelectbox"] /* Para dropdowns */
button[kind="primary"] /* Botón guardar */

/* Navegación */
input[type="radio"][value="Clientes"]
input[type="radio"][value="Pedidos"]

/* Tabla de datos */
div[data-testid="stDataFrame"]
```

## 📁 Estructura del Proyecto

```
IPGFLEXO_DemoERP/
├── erp_demo.py           # Aplicación principal Streamlit
├── database.py           # Lógica de persistencia (CSV/PostgreSQL)
├── requirements.txt      # Dependencias de Python
├── .streamlit/
│   └── config.toml      # Configuración de tema
├── data/                # Archivos CSV (auto-generados)
│   ├── pedidos_clientes.csv
│   ├── albaranes_clientes.csv
│   └── ...
└── README.md            # Este archivo
```

## 🛠️ Desarrollo y Extensión

### Añadir Nuevas Secciones
1. Edita `erp_demo.py` en la función `main()`
2. Añade lógica similar a la sección "Pedidos"
3. Los datos se guardarán automáticamente según el patrón `{subseccion}_{seccion}.csv`

### Personalizar Campos
1. Modifica `COLUMN_SCHEMA` en `database.py`
2. Actualiza el formulario en `mostrar_formulario_entrada()`
3. Ajusta la configuración de columnas en `mostrar_datos_existentes()`

## 📞 Soporte

Para preguntas sobre este sistema de demostración:
- **Proyecto**: Demo ERP para IPGFLEXO
- **Propósito**: Demostración de capacidades de desarrollo
- **Framework**: Streamlit + Python + Pandas

## 📝 Licencia

Este es un proyecto de demostración. Todos los datos son ficticios y el sistema está diseñado únicamente para propósitos de demostración.

## 📝 Notas sobre el formulario y mensajes de confirmación

- El campo de fecha en el formulario es un campo de texto, y debe introducirse en formato DD/MM/AAAA (por ejemplo, 20/06/2025).
- El formato de fecha en el CSV y en la visualización también es DD/MM/AAAA.
- Esto facilita la automatización y la entrada manual, evitando problemas de localización o pop-ups de calendario.
- Al guardar un registro en el formulario, debería aparecer un mensaje de confirmación "✅ ¡Registro añadido con éxito!" justo debajo del formulario.
- Si no ves el mensaje de confirmación, el registro igualmente se guarda correctamente. Puedes comprobarlo en la pestaña "Ver/Editar Registros".