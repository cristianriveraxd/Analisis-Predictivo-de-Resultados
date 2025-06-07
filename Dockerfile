
# Imagen base con Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libxrender1 \
    libsm6 \
    libxext6 \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

# Copiar requerimientos e instalar Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación
COPY . .

# Asegurarse de que la carpeta static exista
RUN mkdir -p /app/static

# Exponer el puerto de Flask
EXPOSE 5000

# Comando por defecto
CMD ["python", "app.py"]
