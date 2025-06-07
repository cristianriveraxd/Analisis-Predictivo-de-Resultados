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
cd proyecto-regresion
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
## 🧠 Resultados y visualizaciones

A través de gráficos generados dinámicamente, se analizan relaciones como:

* **Partidos jugados vs. puntos**
  ![image](https://github.com/user-attachments/assets/51aa05f1-659d-4ac7-9da2-7c7d79697bd8)

* **Goles local vs. goles visitante**
  ![image](https://github.com/user-attachments/assets/6770abf6-ec0f-4e39-b1df-0c86c4a1ebce)

Cada gráfico incluye:

* Datos reales (puntos)
* Línea de regresión (tendencia)
* Análisis explicativo automático

***

## 📜 Licencia

Este proyecto se distribuye bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
