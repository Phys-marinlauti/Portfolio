# Clasificación de Morfología de Galaxias usando Redes Neuronales

## Resumen del Proyecto

Este proyecto explora la clasificación de galaxias basándose en sus características físicas utilizando una red neuronal simple. El objetivo es identificar galaxias elípticas a partir de un conjunto de datos obtenido del proyecto Galaxy Zoo. El proceso incluye carga de datos, análisis exploratorio de datos, manejo de valores atípicos (outliers), ingeniería de características, entrenamiento del modelo y evaluación.

## Conjunto de Datos

El conjunto de datos utilizado en este proyecto es `galaxy_morphology_labeled.csv`. Contiene varios atributos físicos de galaxias y sus correspondientes etiquetas de clase morfológica.

**Nota sobre el Acceso a los Datos:**

El conjunto de datos tiene aproximadamente 65 MB, lo cual es demasiado grande para alojarlo directamente en GitHub. Puedes acceder al conjunto de datos desde [**Inserta aquí el enlace a la plataforma donde alojaste los datos, por ejemplo, URL del conjunto de datos en Kaggle o URL pública de Google Cloud Storage**].

Para ejecutar este notebook, por favor descarga el archivo `galaxy_morphology_labeled.csv` desde el enlace proporcionado arriba y colócalo en el mismo directorio que el archivo del notebook, o actualiza el código del notebook para cargar los datos directamente desde la URL proporcionada si es aplicable (por ejemplo, si usas un enlace público de GCS que pandas pueda leer).

## Análisis y Hallazgos

El análisis exploratorio de datos reveló que ciertas características, particularmente las bandas de color y las relaciones axiales, muestran diferencias notables en la distribución entre galaxias elípticas y no elípticas. La característica de ingeniería `dg_color` también mostró una buena separación entre clases.

La red neuronal entrenada alcanzó una precisión general del 84% en el conjunto de prueba. El reporte de clasificación y la matriz de confusión proporcionan información detallada sobre el rendimiento del modelo, mostrando su precisión y recall al identificar galaxias elípticas y no elípticas.

(Opcional: Agrega aquí una breve interpretación de las métricas clave o los resultados de la matriz de confusión).

## Trabajo Futuro

Áreas potenciales para mejorar incluyen:

*   Experimentar con diferentes arquitecturas de red neuronal u otros algoritmos de clasificación.
*   Realizar una selección de características más rigurosa.
*   Abordar formalmente el posible desbalance de clases si existe en el conjunto de datos completo.
*   Implementar validación cruzada para obtener una estimación más robusta del rendimiento del modelo.

---

**Autor:** Lautaro Marin
**Contacto:** marinlauti00@gmail.com
