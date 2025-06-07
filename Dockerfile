# Usa una imagen oficial de Python como base
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto 5000
EXPOSE 5000

# Ejecuta la app
CMD ["python", "app.py"]
