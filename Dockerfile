FROM python:latest


WORKDIR /app


COPY . /app


RUN python3 -m venv /app/venv


RUN /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000

# Comando por defecto
CMD ["python", "app.py"]
