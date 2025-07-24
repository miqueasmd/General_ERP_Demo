"""
Demo data module for DemoERP
Provides sample data for demo/testing purposes.
"""
import pandas as pd

def create_demo_data():
    """
    Returns a DataFrame with sample demo data for the ERP form.
    Used to quickly fill the form with realistic but fictitious data.
    """
    demo_data = [
        # Example demo records (can be extended)
        {
            'Num_Pedido': '100001',
            'Nombre_Emisor': 'Demo Company A',
            'Cod_Emisor': '1234567890123',
            'Fecha_Pedido': '2025-06-12',
            'Fecha_Entrega': '2025-06-18',
            'Cod_Art_EAN': '1111111111111',
            'Cod_Art_Comprador': 'A-0001',
            'Descripcion': 'Sample product order 1',
            'Cantidad': 1000,
            'Tipo': 'Roll',
            'Tipo_Cliche': 'Standard',
            'Papel': 'Kraft',
            'Cod_IPG': 'DEMO1001',
            'PDF_Link': 'https://demoerp.com/sample1.pdf'
        },
        {
            'Num_Pedido': '100002',
            'Nombre_Emisor': 'Demo Company B',
            'Cod_Emisor': '9876543210987',
            'Fecha_Pedido': '2025-06-15',
            'Fecha_Entrega': '2025-06-20',
            'Cod_Art_EAN': '2222222222222',
            'Cod_Art_Comprador': 'B-0002',
            'Descripcion': 'Sample product order 2',
            'Cantidad': 500,
            'Tipo': 'Sheet',
            'Tipo_Cliche': 'Custom',
            'Papel': 'White',
            'Cod_IPG': 'DEMO1002',
            'PDF_Link': 'https://demoerp.com/sample2.pdf'
        },
        {
            'Num_Pedido': '100003',
            'Nombre_Emisor': 'Demo Company C',
            'Cod_Emisor': '1928374650912',
            'Fecha_Pedido': '2025-06-18',
            'Fecha_Entrega': '2025-06-25',
            'Cod_Art_EAN': '3333333333333',
            'Cod_Art_Comprador': 'C-0003',
            'Descripcion': 'Sample product order 3',
            'Cantidad': 750,
            'Tipo': 'Box',
            'Tipo_Cliche': 'Premium',
            'Papel': 'Recycled',
            'Cod_IPG': 'DEMO1003',
            'PDF_Link': 'https://demoerp.com/sample3.pdf'
        }
    ]
    # Convert date format to DD/MM/YYYY for display
    for d in demo_data:
        if 'Fecha_Pedido' in d and '-' in d['Fecha_Pedido']:
            y, m, d_ = d['Fecha_Pedido'].split('-')
            d['Fecha_Pedido'] = f"{d_}/{m}/{y}"
        if 'Fecha_Entrega' in d and '-' in d['Fecha_Entrega']:
            y, m, d_ = d['Fecha_Entrega'].split('-')
            d['Fecha_Entrega'] = f"{d_}/{m}/{y}"
    return pd.DataFrame(demo_data) 