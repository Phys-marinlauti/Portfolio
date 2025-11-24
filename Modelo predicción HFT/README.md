Predicción a muy corto plazo del Bono AL30
Autor: Lautaro Marín


- Archivos incluidos:

El repositorio contiene dos componentes principales: el entrenamiento en Python y la inferencia en C++.
    
    - En la parte de Python se incluyen los siguientes archivos: pipeline_training.py (script principal que realiza todo el procesamiento, ingeniería de señales, entrenamiento, validación y exportación del modelo), model_weights.txt (coeficientes de la regresión lineal, con el intercepto en la última línea), model_means.txt y model_stds.txt (parámetros del StandardScaler), last_features_raw.txt y last_features_scaled.txt (última fila del dataset antes y después de escalarse) y features_final.csv (dataset final de testeo). Se incluyen también, en la carpeta "market_data_AL30", los 3 CSV's utilizados para el entrenamiento.

    - En la parte de C++ se incluye el archivo predict_al30.cpp, que implementa la inferencia utilizando los parámetros exportados.

- Dependencias:

El entrenamiento requiere Python 3.8 o superior, junto con las librerías pandas, numpy y scikit-learn.
La inferencia requiere un compilador compatible con C++11 o posterior.

- Cómo ejecutar el proyecto:

    1) Entrenamiento del modelo en Python:
        Desde la carpeta del proyecto se debe abrir el archivo:
            python pipeline_training.py
        Dentro de este, cambiar la variable "FOLDER" por la ruta en la que se encuentran los CSV a leer.
        Habiendo hecho esto, ejecutar el código. 
        Este script entrenará el modelo, validará los resultados y generará los archivos necesarios para la inferencia en C++. Si ocurre alguna inconsistencia (por ejemplo problemas de dimensiones, RMSE anormalmente bajo, MAE fuera de rango o errores de escalado), el proceso se detendrá automáticamente y mostrará el motivo.

    2) Compilación del modelo en C++:
        Una vez disponibles los archivos exportados, se compila el ejecutable mediante:
        g++ -O2 -std=c++17 predict_al30.cpp -o predictor

    3) Ejecución del modelo en C++:
        Para obtener la predicción del próximo midprice se ejecuta:
            ./predictor
    El programa cargará los parámetros, estandarizará las 72 características de entrada y devolverá el midprice actual, el cambio de precio predicho y el precio estimado del siguiente tick.



- Contacto

Lautaro Marín
marinlauti00@gmail.com
