# 🏭 DemoERP - Generic ERP Demo Template

A simple, modern ERP demo for managing Customers and Suppliers. Built with Streamlit and Python, designed for RPA automation and as a portfolio-ready template for rapid ERP prototyping.

## 🚀 Features
- **Intuitive UI**: Clean, responsive interface for easy data entry and review
- **Full CRUD**: Manage Orders, Delivery Notes, and Invoices for both Customers and Suppliers
- **Dual Persistence**: Use local CSV files or connect to PostgreSQL (Neon)
- **RPA-Ready**: Optimized for automation tools (e.g., Power Automate Desktop)
- **Demo Data**: Quickly fill forms with realistic sample data
- **Easy Customization**: Modular code, clear structure, and full English documentation

## 🛠️ Quick Start

### Requirements
- Python 3.8+
- pip

### Installation
```bash
# Clone the repository
cd General_ERP_Demo

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run erp_demo.py
```

The app will open at [http://localhost:8501](http://localhost:8501).

### Data Storage Modes
- **CSV (default):** Data is stored in the `./data/` folder (auto-created).
- **PostgreSQL (Neon):** Set environment variables to enable remote DB (see below).

#### PostgreSQL Environment Variables
```bash
# Example (Linux/Mac)
export USE_NEON=1
export PGHOST=your-neon-host
export PGUSER=your-user
export PGPASSWORD=your-password
export PGDATABASE=your-db
```

## 🐳 Run with Docker

You can run DemoERP in a container for easy deployment:

```dockerfile
# Dockerfile (already compatible)
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "erp_demo.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run
```bash
docker build -t demoerp .
docker run -p 8501:8501 demoerp
```

> For PostgreSQL, pass environment variables with `-e` or use a `.env` file.

## 📁 Project Structure
```
General_ERP_Demo/
├── erp_demo.py           # Main Streamlit app
├── database.py           # Data persistence logic (CSV/PostgreSQL)
├── config.py             # Global config and constants
├── modules/
│   ├── form_entry.py     # Form UI logic
│   ├── table_view.py     # Table view/edit logic
│   ├── demo_data.py      # Demo/sample data
│   └── ui_layout.py      # UI layout and branding
├── requirements.txt      # Python dependencies
├── .gitignore            # Git exclusions
├── data/                 # Local CSV data (auto-generated)
└── README.md             # This file
```

## ✨ Customization
- Add new sections/types: Extend `erp_demo.py` and `modules/`
- Change fields: Edit `COLUMN_SCHEMA` in `database.py` and update forms/tables
- UI/branding: Adjust `modules/ui_layout.py` and `config.py`

## 📄 License
This project is for demo and educational purposes. All data is fictitious.

## 👤 Author & Contact
Created by [Miqueas Molina](https://miqueasmd.github.io/)