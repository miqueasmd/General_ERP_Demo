"""
Database management module for DemoERP
Handles both CSV persistence and optional PostgreSQL (Neon) connection
"""
import os
import pandas as pd
from typing import Dict, List, Any, Optional
from pathlib import Path
import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Column configuration for all tables
COLUMN_SCHEMA = {
    'numPedido': 'Num_Pedido',
    'nombreEmisor': 'Nombre_Emisor',
    'codEmisor': 'Cod_Emisor',
    'fechaPedido': 'Fecha_Pedido',
    'fechaEntrega': 'Fecha_Entrega',
    'codArtEan': 'Cod_Art_EAN',
    'codArtComprador': 'Cod_Art_Comprador',
    'descripcion': 'Descripcion',
    'cantidad': 'Cantidad',
    'tipo': 'Tipo',
    'tipoCliche': 'Tipo_Cliche',
    'papel': 'Papel',
    'codIpg': 'Cod_IPG',
    'pdfLink': 'PDF_Link'
}

# SQLAlchemy Base for PostgreSQL
Base = declarative_base()

class ERPRecord(Base):
    """Base model for DemoERP records"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    numPedido = Column(String(50))
    nombreEmisor = Column(String(200))
    codEmisor = Column(String(50))
    fechaPedido = Column(Date)
    fechaEntrega = Column(Date)
    codArtEan = Column(String(50))
    codArtComprador = Column(String(50))
    descripcion = Column(Text)
    cantidad = Column(Integer)
    tipo = Column(String(100))
    tipoCliche = Column(String(100))
    papel = Column(String(100))
    codIpg = Column(String(50))
    pdfLink = Column(String(500))

# Specific models for each table
class OrdersCustomers(ERPRecord):
    __tablename__ = 'pedidos_clientes'

class DeliveryNotesCustomers(ERPRecord):
    __tablename__ = 'albaranes_clientes'

class InvoicesCustomers(ERPRecord):
    __tablename__ = 'facturas_clientes'

class OrdersSuppliers(ERPRecord):
    __tablename__ = 'pedidos_proveedores'

class DeliveryNotesSuppliers(ERPRecord):
    __tablename__ = 'albaranes_proveedores'

class InvoicesSuppliers(ERPRecord):
    __tablename__ = 'facturas_proveedores'

class CSVBackend:
    """Persistence backend using CSV files"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def get_empty_dataframe(self) -> pd.DataFrame:
        """Returns an empty DataFrame with the correct columns"""
        columns = list(COLUMN_SCHEMA.values())
        return pd.DataFrame(columns=columns)
    
    def load_data(self, table_name: str) -> pd.DataFrame:
        """Loads data from CSV or returns an empty DataFrame if not found"""
        file_path = self.data_dir / f"{table_name}.csv"
        try:
            if file_path.exists():
                df = pd.read_csv(file_path, dtype=str)
                # Convert dates to DD/MM/YYYY format
                if 'Fecha_Pedido' in df.columns:
                    df['Fecha_Pedido'] = pd.to_datetime(df['Fecha_Pedido'], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')
                if 'Fecha_Entrega' in df.columns:
                    df['Fecha_Entrega'] = pd.to_datetime(df['Fecha_Entrega'], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')
                if 'Cantidad' in df.columns:
                    df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce').fillna(0).astype(int)
                for col in COLUMN_SCHEMA.values():
                    if col not in df.columns:
                        df[col] = ""
                return df
            else:
                return self.get_empty_dataframe()
        except Exception as e:
            print(f"Error loading {table_name}: {e}")
            return self.get_empty_dataframe()
    
    def save_data(self, table_name: str, dataframe: pd.DataFrame) -> bool:
        """Saves DataFrame to CSV file"""
        file_path = self.data_dir / f"{table_name}.csv"
        try:
            df_to_save = dataframe.copy()
            for col in df_to_save.columns:
                if col not in ['Fecha_Pedido', 'Fecha_Entrega', 'Cantidad']:
                    df_to_save[col] = df_to_save[col].astype(str)
            # Save dates in DD/MM/YYYY format
            if 'Fecha_Pedido' in df_to_save.columns:
                df_to_save['Fecha_Pedido'] = pd.to_datetime(df_to_save['Fecha_Pedido'], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')
            if 'Fecha_Entrega' in df_to_save.columns:
                df_to_save['Fecha_Entrega'] = pd.to_datetime(df_to_save['Fecha_Entrega'], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')
            df_to_save.to_csv(file_path, index=False)
            return True
        except Exception as e:
            print(f"Error saving {table_name}: {e}")
            return False

class PgBackend:
    """Persistence backend using PostgreSQL (Neon)"""
    
    def __init__(self):
        # Environment variables for connection
        self.host = os.getenv('PGHOST')
        self.user = os.getenv('PGUSER') 
        self.password = os.getenv('PGPASSWORD')
        self.database = os.getenv('PGDATABASE')
        
        if not all([self.host, self.user, self.password, self.database]):
            raise ValueError("Missing environment variables for PostgreSQL connection")
        
        # Create engine and session
        self.engine = create_engine(
            f"postgresql://{self.user}:{self.password}@{self.host}/{self.database}"
        )
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_model_class(self, table_name: str):
        """Returns the model class corresponding to the table name"""
        model_map = {
            'pedidos_clientes': OrdersCustomers,
            'albaranes_clientes': DeliveryNotesCustomers,
            'facturas_clientes': InvoicesCustomers,
            'pedidos_proveedores': OrdersSuppliers,
            'albaranes_proveedores': DeliveryNotesSuppliers,
            'facturas_proveedores': InvoicesSuppliers
        }
        return model_map.get(table_name)
    
    def load_data(self, table_name: str) -> pd.DataFrame:
        """Loads data from PostgreSQL"""
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, self.engine)
            # Rename columns to display format
            column_rename = {k: v for k, v in COLUMN_SCHEMA.items() if k in df.columns}
            df = df.rename(columns=column_rename)
            return df
        except Exception as e:
            print(f"Error loading from PostgreSQL {table_name}: {e}")
            return pd.DataFrame(columns=list(COLUMN_SCHEMA.values()))
    
    def save_data(self, table_name: str, dataframe: pd.DataFrame) -> bool:
        """Saves DataFrame to PostgreSQL"""
        try:
            # Rename display columns to DB names
            reverse_mapping = {v: k for k, v in COLUMN_SCHEMA.items()}
            df_to_save = dataframe.rename(columns=reverse_mapping)
            # Clear table and insert new data
            model_class = self.get_model_class(table_name)
            if model_class:
                self.session.query(model_class).delete()
                df_to_save.to_sql(table_name, self.engine, if_exists='append', index=False)
                self.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error saving to PostgreSQL {table_name}: {e}")
            if self.session:
                self.session.rollback()
            return False

class TableManager:
    """Main manager for DemoERP table operations"""
    
    def __init__(self):
        # Select backend based on environment variable
        self.use_neon = os.getenv('USE_NEON', '').lower() in ('1', 'true', 'yes')
        
        if self.use_neon:
            try:
                self.backend = PgBackend()
                print("✅ Connected to PostgreSQL (Neon)")
            except Exception as e:
                print(f"⚠️ Error connecting to PostgreSQL, using CSV: {e}")
                self.backend = CSVBackend()
                self.use_neon = False  # Update state
        else:
            self.backend = CSVBackend()
            print("📁 Using CSV persistence")
    
    def get_dataframe(self, section: str, subsection: str) -> pd.DataFrame:
        """Gets DataFrame for a specific section/subsection"""
        table_name = f"{subsection}_{section}".lower()
        return self.backend.load_data(table_name)
    
    def save_dataframe(self, section: str, subsection: str, dataframe: pd.DataFrame) -> bool:
        """Saves DataFrame for a specific section/subsection"""
        table_name = f"{subsection}_{section}".lower()
        return self.backend.save_data(table_name, dataframe)
    
    def get_empty_dataframe(self) -> pd.DataFrame:
        """Returns an empty DataFrame with the correct structure"""
        if hasattr(self.backend, 'get_empty_dataframe'):
            return self.backend.get_empty_dataframe()
        else:
            return pd.DataFrame(columns=list(COLUMN_SCHEMA.values()))
