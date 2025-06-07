# 📊 Analisis Predictivo de Resultados
## Descripción 
Aplicación que consume datos de una API pública de fútbol y aplica regresión lineal para predecir resultados o estadísticas relevantes.
Este proyecto realiza un análisis técnico de datos deportivos utilizando técnicas de regresión lineal para identificar tendencias y patrones entre variables clave como partidos jugados, puntos obtenidos, goles locales y goles visitantes. El resultado se presenta a través de una aplicación web interactiva construida con Flask y visualizaciones generadas con Matplotlib.
***
## 🔧 Tecnologias utilizadas 
| Herramienta/Tecnología  | Uso                                    |
| -------------------------- | ---------------------------------------- |
| **Python**         | Análisis de datos y regresión lineal |
| **Pandas / NumPy** | Manipulación de datos                 |
| **Matplotlib**     | Visualización de datos                |
| **Scikit-learn**   | Modelado de regresión lineal          |
| **Flask**          | Backend y lógica del sitio web        |
| **Bootstrap**      | Estilizado responsivo y visual         |
| **HTML / CSS**     | Maquetación de la interfaz            |
| **Jinja2**         | Renderizado dinámico en templates     |
***
## 📁 Estructura del proyecto
```#
├── app.py                 # Archivo principal de Flask
├── static/
│   └── styles.css         # Estilos personalizados
│   └── plot.png           # Graficas generadas
├── templates/
│   └── *.html              # Templates generados
└── README.md              # Redme
└── requirements.txt       # Librerias necesarias para ejecutar el proyecto
└── Dockerfile             # Documento para dockerizar app y desplegar en EC2
└──  *.json                # JSONs creados para validadació de datos

```
***
## 📈 Indicadores de rendimiento
| Indicador                      | Descripción                                                                | Objetivo                         |
| -------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------- |
| **R² (Coeficiente)**    | Mide qué tan bien el modelo explica la variación de los datos             | > 0.5 se considera aceptable     |
| **Pendiente**            | Relación entre variables: impacto de la independiente sobre la dependiente | Mayor pendiente = mayor impacto  |
| **Errores residuales**   | Diferencia entre valores reales y predichos por el modelo                   | Más cercanos a 0 = mejor ajuste |
| **Visualización clara** | Claridad gráfica del análisis                                             | Mejora la toma de decisiones     |
***
## 🔄 Pipeline de datos

El flujo de datos sigue una arquitectura moderna tipo ​*data lakehouse*​, integrando fuentes externas y procesamiento ETL:
![image](https://github.com/user-attachments/assets/f04923fa-8811-46da-8ccc-0c15d4e2c5a5)

1. ​**Fuentes de datos**​: API externa o base de datos.
2. ​**Ingesta**​: Extracción vía batch o CDC.
3. ​**Raw Layer**​: Datos almacenados sin transformación.
4. ​**ETL**​: Limpieza, normalización y transformación.
5. ​**Curated Layer**​: Datos estructurados para análisis.
6. ​**Aplicación**​: Visualización e interpretación vía web.
***
## 🚀 Cómo ejecutar el proyecto

1. Clona este repositorio
```#
git clone https://github.com/cristianriveraxd/Analisis-Predictivo-de-Resultados.git
cd Analisis-Predictivo-de-Resultados
```
2. Instala dependencias
```#
pip install -r requirements.txt
```
4. Ejecuta el proyecto
```#
python app.py
```
***

## 🚀 Despliegue en EC2 (AWS) con docker
1. Clona este repositorio en la instancia generada
```#
git clone https://github.com/cristianriveraxd/Analisis-Predictivo-de-Resultados.git

```
2. Configurar app.py para despliegue en producción
```#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
3. Instalar docker y python en ubuntu
```#
# Actualizar repositorios
sudo apt update

# Instalar dependencias necesarias
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common gnupg

# Agregar la clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker.gpg

# Agregar el repositorio de Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/trusted.gpg.d/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Actualizar de nuevo e instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Verificar que Docker está instalado
docker --version

# Habilitar Docker al inicio y arrancarlo
sudo systemctl enable docker
sudo systemctl start docker

# (Opcional) Ejecutar Docker sin sudo
sudo usermod -aG docker $USER
newgrp docker

# Python y pip
sudo apt install -y python3 python3-pip

```
4. Construye y ejecuta el contenedor en EC2
```#
cd Analisis-Predictivo-de-Resultados
docker build -t flask-champions .
docker run -d -p 5000:5000 flask-champions
```
*Si tienes problemas para acceder a la pagina verifica los puertos accesibles en AWS, en tu instancia *

***
## 🧠 Resultados y visualizaciones

A través de gráficos generados dinámicamente, se analizan relaciones como:

* **Partidos jugados vs. puntos**
  ![image](https://github.com/user-attachments/assets/51aa05f1-659d-4ac7-9da2-7c7d79697bd8)

* **Goles local vs. goles visitante**
  ![image](https://github.com/user-attachments/assets/6770abf6-ec0f-4e39-b1df-0c86c4a1ebce)

* **Grafos obtenidos**
  ![image](https://github.com/user-attachments/assets/0f4b12ac-2324-4584-a1d0-dafdd3ba3423)
  
* **Dashboard interactivo con accordions**
  ![image](https://github.com/user-attachments/assets/d4cc9177-abe7-490c-8bbf-a384480c52f4)
  ![image](https://github.com/user-attachments/assets/a50bc4a2-aa7c-4a44-845e-9174bd843e51)
  ![image](https://github.com/user-attachments/assets/28c68bb0-2314-426e-bff0-882f3ae7d1a0)
  ![image](https://github.com/user-attachments/assets/3f9fcb46-2a75-4ab0-9ed9-fd16ccdf2a5d)
  ![image](https://github.com/user-attachments/assets/d75c72d9-0741-4e50-8c0a-4ef2eb806624)


Cada gráfico incluye:

* Datos reales (puntos)
* Línea de regresión (tendencia)
* Análisis explicativo automático

***

## 📜 Licencia

Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
