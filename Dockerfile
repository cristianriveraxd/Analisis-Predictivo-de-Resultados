FROM python:3.12-slim

# Evita prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema necesarias para compilar extensiones de Python
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de la aplicación
WORKDIR /app
COPY . .

# Instalar las dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto
CMD ["python3", "app.py"]
