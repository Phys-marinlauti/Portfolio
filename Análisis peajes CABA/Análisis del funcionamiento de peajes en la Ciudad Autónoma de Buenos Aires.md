Este estudio presenta un análisis exploratorio de datos del dataset ([_Vehicular Traffic in Buenos Aires 2023_](https://www.kaggle.com/datasets/gasparpm/vehicular-traffic-in-buenos-aires-2023)). Este contiene datos del tráfico vehicular en los peajes de la Ciudad Autónoma de Buenos Aires a lo largo del año 2023. Se utilizaron herramientas de análisis y visualización de datos para identificar patrones de comportamiento, correlaciones clave y tendencias asociadas al flujo vehicular y los métodos de pago. Entre los hallazgos más destacados se incluyen:

- Diferencias significativas en el volumen de tráfico entre días laborables y fines de semana, así como variaciones estacionales a lo largo del año.
- Peajes como la Autopista Perito Moreno, que concentra el 35,20% del total de pasadas, reflejan su importancia estratégica como conexión entre el conurbano y la ciudad.
- Una alta correlación entre la no aceptación de efectivo y un mayor porcentaje de infracciones, con peajes sin opción de pago en efectivo registrando un 23,6% de infracciones frente al 5% de aquellos que sí aceptan este método.
- Tendencias horarias, como un mayor porcentaje de infracciones en horario nocturno (20-7hs), que representan el 21,54% del total.

Estos resultados son relevantes para optimizar la gestión del tráfico, proponer ajustes en los métodos de pago y diseñar políticas que reduzcan la evasión de peajes. Asimismo, se identificaron oportunidades para futuros análisis más detallados que exploren la relación entre las tasas de infracción, los métodos de pago y las características de cada peaje.


---
# Introducción
Los peajes son herramientas muy útiles a la hora de manejar el flujo del tráfico; estudiar las métricas asociadas a estos puede ayudarnos a entender diversos patrones en el tráfico vehicular zonal.  
Se realizó, utilizando Python y distintas librerías (**ver código en la siguiente celda del notebook**), el análisis y posterior visualización de la base de datos indicada. La misma contiene el número de pasos y distintas variables asociadas a los peajes de la Ciudad de Buenos Aires comprendidas para el período 01/01/2023 - 31/12/2023. 

--- 


# Análisis
## Tendencias y patrones en la cantidad de pasadas por los peajes
Se utiliza el registro de pasadas para determinar cuántos autos cruzaron un peaje. Se decide utilizar esto para estudiar dos evoluciones distintas, **la evolución de pasadas totales según el día**, y **la evolución de pasadas totales según el horario**.

## Pasadas totales por hora promediado por día
![horas 1.png|100](https://i.postimg.cc/JzTfXKsH/horas.png)

Se segmentó la muestra en días de semana y días de fin de semana. Se tomó la suma de todas las pasadas a lo largo del año para cada hora en específico y se promedió por la cantidad de días. Se decidió realizar esta separación ya que se asume que el cambio en las actividades cotidianas de la población en general presenta diferencias entre semana y fin de semana.  
A simple vista, observamos diferencias en el comportamiento del tráfico, pues vemos una distribución notablemente sesgada hacia las horas más altas cuando hablamos del segundo grupo.

## Evolución de pasadas totales según el día
![año.png](https://i.postimg.cc/RCKxYcD2/a-o.png)
Otro patrón a considerar es la evolución del tráfico con respecto al día. En este caso, se realizó la suma de pasadas para cada día. Por simplicidad, se optó por separar la muestra en "semana", "sábado" y "domingo". Lo primero que se puede notar es que hay una diferencia no despreciable entre la cantidad de pasadas dentro de la semana y fuera de ella. Lo interesante está en observar que también la hay entre días de fin de semana, es decir, las pasadas de domingo son menos también. Nuevamente, el cambio de rutinas puede ser una explicación a tener en cuenta.  
Por otro lado, también notamos, y se podría profundizar realizando un modelo de regresión o un simple ajuste polinómico, que hay una evolución a medida que pasa el año, pues el tráfico aumenta de manera consistente hasta volver a reducirse al final de año. 

## Porcentaje de cantidad de pasadas segregado por peaje
![mapa cant grande.png](https://i.postimg.cc/PxD9Bj21/mapa-cant-grande.png)
Se tomaron los datos de pasadas totales en todo el año y se agruparon por peaje. Se halló una dispersión mucho más alta de lo esperada en los datos, pues es visible que hay una gran disparidad entre la cantidad de pasadas para cada peaje, siendo el de la Autopista Perito Moreno (AVE) responsable del 35,20% del total. Esto puede ser atribuible, en parte, a la centralidad de la autopista como conexión entre el conurbano y CABA. 

## Sentido del tráfico vehicular
Con el objetivo de ahondar en el comportamiento del tráfico, se buscó desglosar la cantidad de pasadas por peaje y sentido. Se tomó la diferencia entre autos que entran y que salen del centro para cada peaje, y se calculó el porcentaje sobre el total de pasadas que esa diferencia representa. Esto se hizo para obtener qué peajes representaban una mayor entrada o salida de vehículos.  
![mapa sent grande.png](https://i.postimg.cc/q7h53rfW/mapa-sent-grande.png)

Por otro lado, para profundizar el estudio de las tendencias observadas según el horario, se agrupó el total de pasadas por día según sentido y se las graficó según su horario.  

![horas sent.png](https://i.postimg.cc/nhc8MNht/horas-sent.png)

Si bien no se puede apuntar una causalidad sin un análisis más en profundidad (se puede comparar el tráfico de ambos grupos según si es día de semana o no, por ejemplo), observamos que la distribución para el grupo sentido a provincia se encuentra sesgada hacia horas más elevadas. Factores como una disparidad entre ambos grupos para días de semana y de fin de semana podrían ser una explicación. (Es decir, mucha más gente moviéndose a provincia los fines de semana por ocio, y más gente moviéndose al centro los días de semana por otras actividades podría ser una explicación. Se necesita más análisis para verificarlo).

## Distribución y tendencias de los métodos de pago

Se analizó la distribución de cantidad de pasadas según el medio de pago. En primera instancia, se separó la muestra entre "semana" y "fin de semana", se promedió la cantidad de pasadas de acuerdo a la cantidad de días en cada grupo y se las comparó.  

![bar1 1.png](https://i.postimg.cc/CL4ThwYN/bar1.png)  

Principalmente notamos, en general, una cantidad de pasadas promedio menor en el grupo de "fin de semana"; aún así, se observa que hay una mayor tendencia a pagar con efectivo, pasando de un 7,21% de las transacciones totales en la semana a un 10,72% los fines de semana.  
Se tomó, por otro lado, el porcentaje del total para las "Violaciones" o "Infracciones"; se calculó un 11,20% en la semana y un 11,05% los fines de semana. Esto, nuevamente, puede ser atribuible a una mayor prevalencia de las actividades de ocio en los fines de semana.  

![por tot bars.png](https://i.postimg.cc/52tGfvs4/por-tot-bars.png)

Por otro lado, se buscó estudiar el porcentaje de infracciones segregado por peaje en base al total de pasadas en cada uno de estos.  

![mapa inf grande posta.png](https://i.postimg.cc/MK5Nktb3/mapa-inf-grande-posta.png)

Se calculó también el promedio del porcentaje de infracciones, el cual se encuentra en 21,74%; se puede ver también que hay peajes con hasta un 47,12% de infracciones, como es el caso del PB3. Esto puede representar una cantidad importante frente al total de pasos dentro de ciertos peajes. Podemos observar también cierta correlación entre volumen de tráfico y porcentaje de infracciones, pero decido dejar de lado ese análisis por ahora.  

Una explicación para el elevado porcentaje de infracciones en ciertos peajes puede hallarse en la no inclusión del efectivo como método de pago. Se segmentó la distribución de métodos de pago según el peaje.  

![bar-2.png](https://i.postimg.cc/sDJ9MnTY/bar21.png)
![3](https://i.postimg.cc/WbVwbRwp/bar22.png)
![4](https://i.postimg.cc/ryx9kyWY/bar23.png)

Si bien es notable a simple vista, se segmentaron los grupos de peajes con efectivo como medio de pago contra aquellos sin efectivo como medio de pago, y se tomó el promedio de infracciones sobre el total de pasadas de cada grupo, obteniendo así un 5% para peajes con efectivo contra un 23,6% para peajes sin efectivo, lo cual configura un aumento porcentual considerable. Se calcula también el volumen que representan ambos grupos sobre el total, siendo un 66,93% para el grupo con efectivo contra un 33,07% para el grupo sin este. Entonces, si bien los peajes sin efectivo reciben más porcentaje de infracciones, este tiene menos peso al tener estos menos volumen.  

Se realizó también un desagregado de la cantidad de infracciones y de pagos en efectivo por hora del día.  

![inf ef hora.png](https://i.postimg.cc/8CjqmWvK/inf-ef-hora.png)

Se halló así, para las infracciones, una distribución que no se mantiene constante con respecto al tiempo. Se observa una mayor presencia de infracciones en horarios más cercanos a la madrugada, y se calculó que un 21,54% de estas se ubica en el rango 20-7HS, horario en el que no se registra una cantidad significativa de tráfico vehicular. A su vez, la proporción de pago en efectivo varía de forma menos significativa a lo largo del día. Se puede explorar más la relación entre ambas categorías estudiando el comportamiento por hora para cada peaje, pero esto escapa al objetivo de este documento.  

---

# Conclusiones

A lo largo de este análisis se han identificado diversos patrones y tendencias en el comportamiento del tráfico vehicular que atraviesa los peajes de la Ciudad de Buenos Aires. Los hallazgos más significativos pueden agruparse en dos categorías principales: patrones de circulación y comportamiento en los métodos de pago.

En cuanto a los patrones de circulación, se observan diferencias significativas entre días laborables y fines de semana, con una notable reducción del tráfico durante los domingos. La Autopista Perito Moreno (AVE) se destaca como la vía más transitada, concentrando el 35,20% del total de pasadas, lo cual refleja su importancia como conexión entre el conurbano y CABA. También se destaca la variación de volumen de tráfico según la época del año. Por otro lado, el análisis del sentido de circulación revela patrones horarios distintivos, con una tendencia hacia horarios más tardíos en el sentido provincia, lo cual podría relacionarse con diferentes perfiles de uso entre días laborables y fines de semana.

Estas observaciones son importantes para la correcta gestión y planificación del tránsito vehicular. Usando estos datos se puede obtener un criterio para el precio de las tarifas de acuerdo al horario y a la época del año. También pueden utilizarse en conjunto con más datos para modelar el tiempo de llegada estimado (ETA) a futuro.

Quizás el hallazgo más relevante surge del análisis de los métodos de pago y las infracciones. Los peajes que no aceptan efectivo muestran, en promedio, una tasa de infracciones significativamente mayor (23,6%) comparada con aquellos que sí lo aceptan (5%). Esta diferencia es particularmente notable considerando que los peajes sin opción de pago en efectivo representan solo el 33,07% del volumen total de tráfico. Además, se identificó que el uso de efectivo aumenta durante los fines de semana, pasando de un 7,21% en días laborables a un 10,72%. Esto, junto a la variación en el uso de otros métodos de pago, sugiere un cambio en el perfil de usuarios.

El análisis temporal de las infracciones revela otro patrón significativo: el 21,54% de estas ocurre en horario nocturno (20-7hs), período que no registra un volumen significativo de tráfico. Esto, combinado con casos extremos como el del peaje PB3 que registra un 47,12% de infracciones, sugiere la necesidad de revisar las políticas actuales de métodos de pago y control.

---

# Apéndice

El procesamiento de los datos se encuentra disponible para verificar junto a este informe.

### Zonas con peajes para mayor claridad
**Zona 1**  
![[mapa inf 1.png]](https://i.postimg.cc/vTdkyNNk/mapa-inf-1.png)  

**Zona 2**  
![[mapa inf 2.png]](https://i.postimg.cc/yxX58Tqd/mapa-inf-2.png)  

**Zona 3**  
![[mapa inf 3.png]](https://i.postimg.cc/QNpvmjB3/mapa-inf-3.png) 

