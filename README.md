# CRM Django Application

Aplicación CRM para gestión de clientes, compañías e interacciones con generación de datos ficticios.

## Requisitos

- Python 3.8+
- Django 4.1+
- Faker 18.0+

## Instalación

1. Clonar repositorio:

```bash
git clone https://github.com/tu-usuario/test.git
```

```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows
pip install -r requirements.txt
```

```bash
python manage.py migrate
python manage.py populate_data
python manage.py runserver
```
