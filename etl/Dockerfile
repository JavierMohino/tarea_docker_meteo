# Imagen base oficial de Python
FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias y luego instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script
COPY app.py .

# Al arrancar el contenedor, se ejecuta el script
CMD ["python", "app.py"]
