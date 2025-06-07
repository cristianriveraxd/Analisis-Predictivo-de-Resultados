FROM python:3.12

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    && apt-get clean

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto
EXPOSE 5000

# Comando por defecto
CMD ["python3", "app.py"]
